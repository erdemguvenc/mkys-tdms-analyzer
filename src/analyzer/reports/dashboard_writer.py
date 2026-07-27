from __future__ import annotations

from openpyxl.worksheet.worksheet import Worksheet

from analyzer.reports.dashboard_summary import DashboardSummary

from .dashboard_charts import DashboardCharts

from .page_setup import prepare_worksheet
from .styles import (
    apply_kpi_card,
    apply_kpi_title,
    apply_kpi_value,
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

        self._write_kpis(
            worksheet,
            summary,
        )

        DashboardCharts.add_match_pie_chart(
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

        title.value = (
            "MKYS - TDMS Uzlaştırma Dashboard"
        )

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

        title_cell.value = title

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
                "Toplam Kayıt",
                summary.total_records,
                3,
                1,
            ),
            (
                "Eşleşen Kayıt",
                summary.matched_records,
                3,
                4,
            ),
            (
                "MKYS Eksik",
                summary.missing_in_mkys,
                3,
                7,
            ),
            (
                "TDMS Eksik",
                summary.missing_in_tdms,
                3,
                10,
            ),
            (
                "Tutar Farkı",
                summary.amount_difference_count,
                7,
                1,
            ),
            (
                "Tüketim Farkı",
                summary.consumption_difference_count,
                7,
                4,
            ),
        ]

        for title, value, row, column in cards:

            self._write_kpi_card(
                worksheet,
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


    