from decimal import Decimal
from pathlib import Path
from datetime import date

import pandas as pd

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.constants import mkys_columns as COL

class MKYSCsvParser:

    _MONTHS = {
        "OCA": 1,
        "SUB": 2,
        "ŞUB": 2,

        "MAR": 3,

        "NIS": 4,
        "NİS": 4,

        "MAY": 5,

        "HAZ": 6,

        "TEM": 7,

        "AGU": 8,
        "AĞU": 8,

        "EYL": 9,

        "EKI": 10,
        "EKİ": 10,

        "KAS": 11,

        "ARA": 12,
    }

    def parse(self, file_path: Path) -> list[Movement]:
        df = self._read_csv(file_path)

        self._validate_columns(df)

        return self._create_movements(df)

    def _create_movements(
        self,
        df: pd.DataFrame,
    ) -> list[Movement]:
        return [
            self._row_to_movement(row)
            for _, row in df.iterrows()
        ]

    def _row_to_movement(
        self,
        row: pd.Series,
    ) -> Movement:

        return Movement(
            source="MKYS",

            movement_type=MovementType.ENTRY,

            movement_date=self._parse_date(
                str(row[COL.DATE])
        ),

            tif_no=str(row[COL.TIF_NO]),

            invoice_no=str(row[COL.INVOICE_NO]),

            amount=self._parse_decimal(
                row[COL.TOTAL_AMOUNT]
            ),

            warehouse=str(row[COL.WAREHOUSE]),

            budget_type=str(row[COL.BUDGET]),

            stock_code=str(row[COL.ITEM_CODE]),

            stock_name=str(row[COL.ITEM_NAME]),

            supplier=str(row[COL.SUPPLIER]),

            quantity=self._parse_decimal(
                row[COL.QUANTITY]
            ),
        )
    
    def _read_csv(
        self,
        file_path: Path,
    ) -> pd.DataFrame:
        """CSV dosyasını pandas ile okur."""

        df = pd.read_csv(
            file_path,
            sep=";",
            encoding="cp1254",
        )

        # Boş kolonları temizle
        df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

        return df
    
    def _validate_columns(
        self,
        df: pd.DataFrame,
    ) -> None:

        missing = [
            column
            for column in COL.REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Eksik MKYS sütunları: {', '.join(missing)}"
            )
    
    def _parse_date(self, value: str) -> date:
        day, month, year = value.strip().split("-")

        month = month.upper()

        try:
            month_number = self._MONTHS[month]
        except KeyError:
            raise ValueError(f"Desteklenmeyen ay değeri: {month!r}")

        return date(
            year=int(year),
            month=month_number,
            day=int(day),
        )

    def _parse_decimal(self, value: object) -> Decimal:
        text = str(value).strip()

        if not text:
            return Decimal("0")

        text = text.replace(".", "")
        text = text.replace(",", ".")

        return Decimal(text)