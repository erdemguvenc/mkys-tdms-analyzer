from __future__ import annotations

from openpyxl.formatting.rule import DataBarRule
from openpyxl.worksheet.worksheet import Worksheet

from analyzer.reports.dashboard_summary import DashboardSummary

from analyzer.reports.executive_summary import ExecutiveSummary
from analyzer.reports.executive_summary import (
    ExecutiveSummary,
    ExecutiveSummaryResult,
)
from analyzer.reports.report_status import ReportStatus

from .dashboard_charts import DashboardCharts

from .page_setup import prepare_worksheet
from .theme import THEME_CHART_PRIMARY
from .styles import (
    apply_kpi_card,
    apply_kpi_title,
    apply_kpi_value,
    apply_summary_box,
    apply_summary_text,
    apply_summary_title,
    apply_summary_success,
    apply_summary_warning,
    apply_summary_critical,
    apply_status_badge,
    apply_title,    
)


class DashboardWriter:

    def write_dashboard(
        self,
        worksheet: Worksheet,
        summary: DashboardSummary,
    ) -> None:

        self._write_dashboard_title(
            worksheet,
        )

        summary_builder = ExecutiveSummary()

        result = summary_builder.build(
            summary,
        )

        self._write_executive_summary(
            worksheet,
            result,
        )

        self._write_status_badge(
            worksheet,
            result,
        )

        self._write_quality_progress(
            worksheet,
            summary,
        )

        self._write_kpis(
            worksheet,
            summary,
        )

        DashboardCharts.add_match_pie_chart(
            worksheet,
            summary,
        )

        DashboardCharts.add_consumption_bar_chart(
            worksheet,
            summary,
        )

        DashboardCharts.add_trend_chart(
            worksheet,
            summary,
        )

        DashboardCharts.add_supplier_chart(
            worksheet,
            summary,
        )

        DashboardCharts.add_warehouse_chart(
            worksheet,
            summary,
        )

        DashboardCharts.add_top_difference_chart(
            worksheet,
            summary,
        )

        self._write_match_pie_chart(
            worksheet,
            summary,
        )

        self._write_consumption_chart(
            worksheet,
            summary,
        )

        prepare_worksheet(
            worksheet,
        )


    def _write_dashboard_title(
        self,
        worksheet: Worksheet,
    ) -> None:
        """
        Dashboard başlığını yazar.
        """

        title = worksheet.cell(
            row=1,
            column=1,
        )

        title.value = "MKYS - TDMS Uzlaştırma Dashboard"

        apply_title(title)

        worksheet.merge_cells(
            start_row=1,
            start_column=1,
            end_row=1,
            end_column=12,
        )


    def _write_kpi_card(
        self,
        worksheet: Worksheet,
        icon: str,
        title: str,
        value: int,
        row: int,
        column: int,
    ) -> None:
        """
        Tek bir KPI kartı oluşturur.
        """

        apply_kpi_card(
            worksheet,
            first_row=row,
            last_row=row + 2,
            first_column=column,
            last_column=column + 1,
        )

        worksheet.merge_cells(
            start_row=row,
            start_column=column,
            end_row=row,
            end_column=column + 1,
        )

        worksheet.merge_cells(
            start_row=row + 1,
            start_column=column,
            end_row=row + 2,
            end_column=column + 1,
        )

        title_cell = worksheet.cell(
            row=row,
            column=column,
        )   

        title_cell.value = f"{icon} {title}"

        apply_kpi_title(
            title_cell,
        )

        value_cell = worksheet.cell(
            row=row + 1,
            column=column,
        )

        value_cell.value = value

        apply_kpi_value(
            value_cell,
        )


    def _write_kpis(
        self,
        worksheet: Worksheet,
        summary: DashboardSummary,
    ) -> None:
        """
        KPI kartlarını oluşturur.
        """

        cards = [
            (
                "📊",
                "Toplam Kayıt",
                summary.total_records,
                8,
                1,
            ),
            (
                "✔",
                "Eşleşen Kayıt",
                summary.matched_records,
                8,
                4,
            ),
            (
                "⚠",
                "MKYS Eksik",
                summary.missing_in_mkys,
                8,
                7,
            ),
            (
                "⚠",
                "TDMS Eksik",
                summary.missing_in_tdms,
                8,
                10,
            ),
            (
                "💰",
                "Tutar Farkı",
                summary.amount_difference_count,
                12,
                1,
            ),
            (
                "📦",
                "Tüketim Farkı",
                summary.consumption_difference_count,
                12,
                4,
            ),
        ]

        for icon, title, value, row, column in cards:

            self._write_kpi_card(
                worksheet,
                icon,
                title,
                value,
                row,
                column,
            )


    def _write_match_pie_chart(
        self,
        worksheet: Worksheet,
        summary: DashboardSummary,
    ) -> None:
        """
        Eşleşme durumunu gösteren pasta grafiği oluşturur.
        """

        # Sprint 4.3.3
        pass


    def _write_consumption_chart(
        self,
        worksheet: Worksheet,
        summary: DashboardSummary,
    ) -> None:
        """
        Aylık tüketim karşılaştırma grafiğini oluşturur.
        """

        # Sprint 4.3.4
        pass


    def _write_executive_summary(
        self,
        worksheet: Worksheet,
        result: ExecutiveSummaryResult,
    ) -> None:
        """
        Dashboard'a yönetici özetini yazar.
        """

        #
        # Summary kutusu
        #
        if result.status is ReportStatus.GOOD:

            apply_summary_success(
            worksheet,
            first_row=2,
            last_row=6,
            first_column=1,
            last_column=12,
        )

        elif result.status is ReportStatus.WARNING:

            apply_summary_warning(
            worksheet,
            first_row=2,
            last_row=6,
            first_column=1,
            last_column=12,
        )

        else:

            apply_summary_critical(
                worksheet,
                first_row=2,
                last_row=6,
                first_column=1,
                last_column=12,
            )

        #
        # Başlık
        #
        title = worksheet.cell(
            row=2,
            column=1,
        )

        if result.status is ReportStatus.GOOD:

            title_text = "✔ Executive Summary"

        elif result.status is ReportStatus.WARNING:

            title_text = "⚠ Executive Summary"

        else:

            title_text = "✖ Executive Summary"

        title.value = title_text

        apply_summary_title(
            title,
        )

        #
        # Özet satırları
        #
        for index, line in enumerate(result.lines):

            cell = worksheet.cell(
                row=3 + index,
                column=1,
            )

            cell.value = line

            apply_summary_text(
                cell,
            )


    def _write_status_badge(
        self,
        worksheet: Worksheet,
        result: ExecutiveSummaryResult,
    ) -> None:

        badge = worksheet.cell(
            row=2,
            column=12,
        )

        if result.status is ReportStatus.GOOD:

            badge.value = "GOOD"

        elif result.status is ReportStatus.WARNING:

            badge.value = "WARNING"

        else:

            badge.value = "CRITICAL"

        apply_status_badge(
            badge,
            result.status,
        )


    def _write_quality_progress(
        self,
        worksheet: Worksheet,
        summary: DashboardSummary,
    ) -> None:
        """
        Dashboard kalite yüzdesini yazar ve progress bar uygular.
        """

        quality = 0.0

        if summary.total_records:

            quality = (
                summary.matched_records
                / summary.total_records
                * 100
            )

        title = worksheet["J7"]
        title.value = "Kalite"

        value = worksheet["K7"]
        value.value = quality / 100
        value.number_format = "0%"

        worksheet.conditional_formatting.add(
            "K7",
            DataBarRule(
                start_type="num",
                start_value=0,
                end_type="num",
                end_value=1,
                color=THEME_CHART_PRIMARY,
            ),
        )