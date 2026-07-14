from __future__ import annotations

from openpyxl.worksheet.worksheet import Worksheet

from analyzer.reconciliation.result import ReconciliationResult


class WorksheetWriter:
    """
    Excel çalışma sayfalarını doldurur.
    """

    def write_summary(
        self,
        worksheet: Worksheet,
        result: ReconciliationResult,
    ) -> None:

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