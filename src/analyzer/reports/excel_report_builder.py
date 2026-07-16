from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook

from analyzer.reconciliation.result import ReconciliationResult

from .report_builder import ReportBuilder
from .worksheet_writer import WorksheetWriter


class ExcelReportBuilder(ReportBuilder):
    """
    Uzlaştırma sonucunu Excel dosyası olarak oluşturur.
    """

    def __init__(self) -> None:
        self._writer = WorksheetWriter()

    def build(
        self,
        result: ReconciliationResult,
        output_file: Path,
    ) -> None:

        workbook = Workbook()

        #
        # 1_Özet
        #
        summary = workbook.active
        summary.title = "1_Özet"

        self._writer.write_summary(
            summary,
            result,
        )

        #
        # 2_Giriş_Eşleşen
        #
        sheet = workbook.create_sheet(
            "2_Giriş_Eşleşen"
        )

        self._writer.write_movements(
            sheet,
            "Giriş Eşleşen",
            result.matched,
        )

        #
        # 3_MKYS_Eksik
        #
        sheet = workbook.create_sheet(
            "3_MKYS_Eksik"
        )

        self._writer.write_movements(
            sheet,
            "MKYS'de Bulunup TDMS'de Bulunmayan Girişler",
            result.missing_in_tdms,
        )

        #
        # 4_TDMS_Eksik
        #
        sheet = workbook.create_sheet(
            "4_TDMS_Eksik"
        )

        self._writer.write_movements(
            sheet,
            "TDMS'de Bulunup MKYS'de Bulunmayan Girişler",
            result.missing_in_mkys,
        )

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        workbook.save(output_file)