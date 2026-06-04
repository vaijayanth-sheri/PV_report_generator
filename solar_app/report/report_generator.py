"""
PDF report generator using ReportLab.

Produces a professional multi-page PDF including:
  - Cover page
  - Executive summary with KPIs
  - Monthly production table
  - Monthly production chart (embedded PNG)
  - System configuration summary
  - Methodology section
  - Assumptions & limitations
"""

from __future__ import annotations

import io
import logging
import tempfile
from datetime import datetime
from typing import Optional

import plotly.graph_objects as go
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from config.translations import get_text
from models.assumptions import QuickConfig, ProConfig, SimulationResult

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def _build_styles():
    """Create custom paragraph styles for the report."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontSize=26,
        leading=32,
        alignment=TA_CENTER,
        spaceAfter=12,
        textColor=colors.HexColor("#1A237E"),
    ))
    styles.add(ParagraphStyle(
        name="CoverSubtitle",
        parent=styles["Normal"],
        fontSize=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#455A64"),
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading1"],
        fontSize=16,
        leading=20,
        spaceBefore=16,
        spaceAfter=8,
        textColor=colors.HexColor("#1565C0"),
    ))
    styles.add(ParagraphStyle(
        name="BodyText2",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    ))
    return styles


# ---------------------------------------------------------------------------
# Chart rendering
# ---------------------------------------------------------------------------
def _render_monthly_chart(
    monthly_kwh: list[float],
    month_names: list[str],
    title: str,
) -> Optional[str]:
    """Render the monthly bar chart as a temporary PNG file.

    Returns the file path, or None on failure.
    """
    try:
        fig = go.Figure(
            data=[
                go.Bar(
                    x=month_names,
                    y=monthly_kwh,
                    marker_color="#FF8F00",
                    text=[f"{v:,.0f}" for v in monthly_kwh],
                    textposition="outside",
                )
            ]
        )
        fig.update_layout(
            title=title,
            xaxis_title="",
            yaxis_title="kWh",
            height=350,
            width=700,
            margin=dict(t=50, b=30, l=50, r=20),
            plot_bgcolor="rgba(0,0,0,0)",
        )
        fig.update_yaxes(gridcolor="rgba(200,200,200,0.3)")

        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        fig.write_image(tmp.name, scale=2)
        tmp.close()
        return tmp.name
    except Exception as exc:
        logger.warning("Could not render chart image: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def generate_report(
    result: SimulationResult,
    config: QuickConfig,
    latitude: float,
    longitude: float,
    location_name: str,
    lang: str = "en",
) -> bytes:
    """Generate the PDF report and return raw bytes.

    Parameters
    ----------
    result : SimulationResult
        Computed simulation output.
    config : QuickConfig | ProConfig
        System configuration used.
    latitude, longitude : float
        Site coordinates.
    location_name : str
        Human-readable site name.
    lang : str
        Language code ("en" or "de").

    Returns
    -------
    bytes
        The PDF file content as bytes, ready for download.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = _build_styles()
    story: list = []
    month_names = get_text("month_names", lang)

    # ── Cover page ──────────────────────────────────────────────────────
    story.append(Spacer(1, 6 * cm))
    story.append(Paragraph(get_text("rpt_cover_title", lang), styles["CoverTitle"]))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(get_text("rpt_cover_subtitle", lang), styles["CoverSubtitle"]))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(
        f"{location_name}<br/>"
        f"({latitude:.4f}°N, {longitude:.4f}°E)",
        styles["CoverSubtitle"],
    ))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(
        datetime.now().strftime("%Y-%m-%d"),
        styles["CoverSubtitle"],
    ))
    story.append(PageBreak())

    # ── Executive summary ───────────────────────────────────────────────
    story.append(Paragraph(get_text("rpt_exec_summary", lang), styles["SectionHeading"]))
    summary_data = [
        [get_text("res_annual_yield", lang), f"{result.annual_yield_kwh:,.0f} kWh"],
        [get_text("res_specific_yield", lang), f"{result.specific_yield_kwh_kwp:,.0f} kWh/kWp"],
        [get_text("res_capacity_factor", lang), f"{result.capacity_factor_pct:.1f}%"],
        [get_text("res_performance_ratio", lang), f"{result.performance_ratio_pct:.1f}%"],
    ]
    summary_table = Table(summary_data, colWidths=[10 * cm, 5 * cm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F5F5")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BDBDBD")),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 1 * cm))

    # ── Monthly production table ────────────────────────────────────────
    story.append(Paragraph(get_text("rpt_monthly_table", lang), styles["SectionHeading"]))
    table_data = [
        [get_text("res_month", lang), get_text("res_energy_kwh", lang)]
    ]
    for i, name in enumerate(month_names):
        table_data.append([name, f"{result.monthly_yield_kwh[i]:,.1f}"])
    table_data.append(["Total", f"{result.annual_yield_kwh:,.1f}"])

    monthly_table = Table(table_data, colWidths=[8 * cm, 5 * cm])
    monthly_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565C0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#E3F2FD")),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BDBDBD")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#FAFAFA")]),
    ]))
    story.append(monthly_table)
    story.append(Spacer(1, 0.5 * cm))

    # ── Monthly chart ───────────────────────────────────────────────────
    chart_path = _render_monthly_chart(
        result.monthly_yield_kwh,
        month_names,
        get_text("res_monthly_chart_title", lang),
    )
    if chart_path:
        story.append(Image(chart_path, width=16 * cm, height=8 * cm))
    story.append(PageBreak())

    # ── Configuration summary ───────────────────────────────────────────
    story.append(Paragraph(get_text("rpt_config_summary", lang), styles["SectionHeading"]))
    is_pro = isinstance(config, ProConfig)
    config_rows = [
        [get_text("sidebar_lat", lang), f"{latitude:.4f}°"],
        [get_text("sidebar_lon", lang), f"{longitude:.4f}°"],
        [get_text("sys_kwp", lang), f"{config.kwp} kWp"],
        [get_text("sys_tilt", lang), f"{config.tilt_deg}°"],
        [get_text("sys_azimuth", lang), f"{config.azimuth_deg}°"],
        [get_text("sys_inv_eff", lang), f"{config.inverter_efficiency_pct}%"],
    ]
    if is_pro:
        config_rows.extend([
            [get_text("sys_dc_ac", lang), f"{config.dc_ac_ratio}"],
            [get_text("sys_albedo", lang), f"{config.albedo}"],
            [get_text("sys_transposition", lang), config.transposition_model.title()],
            [get_text("sys_module_type", lang), config.module_type.replace("_", " ").title()],
        ])
    else:
        config_rows.append(
            [get_text("sys_losses", lang), f"{config.system_losses_pct}%"]
        )

    config_table = Table(config_rows, colWidths=[8 * cm, 7 * cm])
    config_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F5F5")),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BDBDBD")),
    ]))
    story.append(config_table)
    story.append(Spacer(1, 1 * cm))

    # ── Methodology ─────────────────────────────────────────────────────
    story.append(Paragraph(get_text("rpt_methodology", lang), styles["SectionHeading"]))
    for line in get_text("rpt_methodology_text", lang).split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["BodyText2"]))
    story.append(Spacer(1, 0.5 * cm))

    # ── Assumptions & limitations ───────────────────────────────────────
    story.append(Paragraph(get_text("rpt_assumptions", lang), styles["SectionHeading"]))
    for line in get_text("rpt_assumptions_text", lang).split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["BodyText2"]))

    # ── Build PDF ───────────────────────────────────────────────────────
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    logger.info("PDF report generated — %d bytes", len(pdf_bytes))
    return pdf_bytes
