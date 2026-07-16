from __future__ import annotations

from datetime import date
from decimal import Decimal

from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

from analyzer.reconciliation.difference import (
    AmountDifference,
    ConsumptionDifference,
)
from analyzer.models.movement import Movement
from analyzer.reports.styles import (
    apply_currency,
    apply_date,
    apply_decimal,
    apply_header,
    apply_integer,
    apply_text,
    apply_title,
    format_worksheet,
)


class WorksheetWriter:
    """
    Excel çalışma sayfalarını doldurur.
    """

    #
    # ------------------------------------------------------------------
    # Yardımcı metodlar
    # ------------------------------------------------------------------
    #

    def _write_title(
        self,
        worksheet: Worksheet,
        title: str,
    ) -> None:
        """
        Sayfa başlığını yazar.
        """

        cell = worksheet["A1"]

        cell.value = title

        apply_title(cell)

    def _write_headers(
        self,
        worksheet: Worksheet,
        headers: list[str],
        row: int = 3,
    ) -> None:
        """
        Tablo başlıklarını yazar.
        """

        for column, header in enumerate(
            headers,
            start=1,
        ):

            cell = worksheet.cell(
                row=row,
                column=column,
            )

            cell.value = header

            apply_header(cell)

    def _movement_row(
        self,
        movement: Movement,
    ) -> list[object]:
        """
        Movement nesnesini Excel satırına dönüştürür.
        """

        return [
            movement.tif_no,
            movement.movement_date,
            movement.warehouse,
            movement.budget_type,
            movement.stock_code,
            movement.stock_name,
            movement.supplier,
            movement.quantity,
            movement.amount,
        ]

    def _write_cell(
        self,
        cell: Cell,
        value: object,
    ) -> None:
        """
        Hücreyi veri tipine göre yazar ve biçimlendirir.
        """

        cell.value = value

        if value is None:

            apply_text(cell)

            return

        if isinstance(
            value,
            date,
        ):

            apply_date(cell)

            return

        if isinstance(
            value,
            Decimal,
        ):

            apply_decimal(cell)

            return

        if isinstance(
            value,
            int,
        ):

            apply_integer(cell)

            return

        if isinstance(
            value,
            float,
        ):

            apply_currency(cell)

            return

        apply_text(cell)

    def _write_table(
        self,
        worksheet: Worksheet,
        headers: list[str],
        rows: list[list[object]],
    ) -> None:
        """
        Ortak tablo yazıcısı.
        """

        self._write_headers(
            worksheet,
            headers,
        )

        current_row = 4

        for row in rows:

            for column, value in enumerate(
                row,
                start=1,
            ):

                cell = worksheet.cell(
                    row=current_row,
                    column=column,
                )

                self._write_cell(
                    cell,
                    value,
                )

            current_row += 1

        format_worksheet(
            worksheet,
        )

            #
    # ------------------------------------------------------------------
    # Public metodlar
    # ------------------------------------------------------------------
    #

    def write_summary(
        self,
        worksheet: Worksheet,
        result,
    ) -> None:
        """
        Uzlaştırma özet sayfasını oluşturur.
        """

        self._write_title(
            worksheet,
            "MKYS - TDMS Uzlaştırma Özeti",
        )

        headers = [
            "Kategori",
            "Adet",
        ]

        rows = [
            [
                "Eşleşen Giriş Hareketleri",
                len(result.matched),
            ],
            [
                "TDMS'de Bulunmayan Girişler",
                len(result.missing_in_tdms),
            ],
            [
                "MKYS'de Bulunmayan Girişler",
                len(result.missing_in_mkys),
            ],
            [
                "Tutar Farkları",
                len(result.amount_differences),
            ],
            [
                "Tüketim Farkları",
                len(result.consumption_differences),
            ],
            [
                "Açılış Eşleşmeleri",
                len(result.opening_matched),
            ],
            [
                "TDMS'de Bulunmayan Açılışlar",
                len(result.opening_missing_in_tdms),
            ],
            [
                "MKYS'de Bulunmayan Açılışlar",
                len(result.opening_missing_in_mkys),
            ],
        ]

        self._write_table(
            worksheet,
            headers,
            rows,
        )

    def write_movements(
        self,
        worksheet: Worksheet,
        title: str,
        movements: list[Movement],
    ) -> None:
        """
        Movement listesini çalışma sayfasına yazar.
        """

        self._write_title(
            worksheet,
            title,
        )

        headers = [
            "TİF No",
            "Tarih",
            "Depo",
            "Bütçe",
            "Taşınır Kodu",
            "Malzeme",
            "Tedarikçi",
            "Miktar",
            "Tutar",
        ]

        rows: list[list[object]] = []

        for movement in movements:

            rows.append(
                self._movement_row(
                    movement,
                )
            )

        self._write_table(
            worksheet,
            headers,
            rows,
        )


    def write_amount_differences(
        self,
        worksheet: Worksheet,
        differences: list[AmountDifference],
    ) -> None:
        """
        Tutar farklılıklarını yazar.
        """

        self._write_title(
            worksheet,
            "Tutar Farkları",
        )

        headers = [
            "TİF No",
            "MKYS Tutarı",
            "TDMS Tutarı",
            "Fark",
        ]

        rows: list[list[object]] = []

        for difference in differences:

            rows.append(
                [
                    difference.mkys.tif_no,
                    difference.mkys.amount,
                    difference.tdms.amount,
                    difference.difference
                ]
            )

        self._write_table(
            worksheet,
            headers,
            rows,
        )

    def write_consumption_differences(
        self,
        worksheet: Worksheet,
        differences: list[ConsumptionDifference],
    ) -> None:
        """
        Aylık tüketim farklarını yazar.
        """

        self._write_title(
            worksheet,
            "Tüketim Farkları",
        )

        headers = [
            "Yıl",
            "Ay",
            "MKYS",
            "TDMS",
            "Fark",
        ]

        rows: list[list[object]] = []

        for difference in differences:

            rows.append(
                [
                    difference.year,
                    difference.month,
                    difference.mkys_amount,
                    difference.tdms_amount,
                    difference.difference,
                ]
            )

        self._write_table(
            worksheet,
            headers,
            rows,
        )