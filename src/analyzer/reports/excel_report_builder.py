from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook

from analyzer.reconciliation.result import ReconciliationResult

from .report_builder import ReportBuilder


class ExcelReportBuilder(ReportBuilder):
    """
    Uzlaştırma sonucunu Excel dosyası olarak oluşturur.
    """

    def build(
        self,
        result: ReconciliationResult,
        output_file: Path,
    ) -> None:
        """
        Excel raporunu oluşturur.
        """

        workbook = Workbook()

        worksheet = workbook.active
        worksheet.title = "Özet"

        worksheet["A1"] = "MKYS - TDMS Uzlaştırma Raporu"

        worksheet["A3"] = "Eşleşen Giriş Hareketleri"
        worksheet["B3"] = len(result.matched)

        worksheet["A4"] = "TDMS'de Eksik"
        worksheet["B4"] = len(result.missing_in_tdms)

        worksheet["A5"] = "MKYS'de Eksik"
        worksheet["B5"] = len(result.missing_in_mkys)

        worksheet["A6"] = "Tutar Farkları"
        worksheet["B6"] = len(result.amount_differences)

        worksheet["A7"] = "Tüketim Farkları"
        worksheet["B7"] = len(result.consumption_differences)

        worksheet["A8"] = "Açılış Eşleşmeleri"
        worksheet["B8"] = len(result.opening_matched)

        worksheet["A9"] = "TDMS'de Eksik Açılış"
        worksheet["B9"] = len(result.opening_missing_in_tdms)

        worksheet["A10"] = "MKYS'de Eksik Açılış"
        worksheet["B10"] = len(result.opening_missing_in_mkys)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        workbook.save(output_file)