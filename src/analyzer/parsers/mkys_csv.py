from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pandas as pd

from analyzer.constants import mkys_columns as COL
from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.utils import parse_date
from analyzer.utils import parse_decimal


class MKYSCsvParser:
    """
    MKYS CSV Parser

    v3.5

    - CSV okur
    - Encoding'i otomatik bulur
    - Ayırıcıyı otomatik dener
    - Sütunları doğrular
    - Movement nesneleri üretir
    """

    def parse(
        self,
        file_path: Path,
    ) -> list[Movement]:

        df = self._read_csv(file_path)

        self._validate_columns(df)

        return self._create_movements(df)

    # ---------------------------------------------------------

    def _read_csv(
        self,
        file_path: Path,
    ) -> pd.DataFrame:

        encodings = (
            "utf-8-sig",
            "utf-8",
            "cp1254",
            "latin5",
        )

        separators = (
            ";",
            ",",
        )

        last_error = None

        for encoding in encodings:
            for separator in separators:

                try:

                    df = pd.read_csv(
                        file_path,
                        sep=separator,
                        encoding=encoding,
                        low_memory=False,
                    )

                    if len(df.columns) <= 1:
                        continue

                    if df.empty:
                        continue

                    unnamed = [
                        c
                        for c in df.columns
                        if str(c).startswith("Unnamed")
                    ]

                    if unnamed:
                        df = df.drop(columns=unnamed)

                    df.columns = (
                        df.columns.astype(str)
                        .str.replace("\ufeff", "", regex=False)
                        .str.strip()
                    )

                    df = (
                        df.dropna(axis=0, how="all")
                        .reset_index(drop=True)
                    )

                    print(df.columns.tolist())

                    return df

                except Exception as exc:
                    last_error = exc

        raise ValueError(
            "MKYS CSV okunamadı."
        ) from last_error
    
    # ---------------------------------------------------------

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
                "Eksik MKYS sütunları: "
                + ", ".join(missing)
            )

    # ---------------------------------------------------------

    def _create_movements(
        self,
        df: pd.DataFrame,
    ) -> list[Movement]:

        return [
            self._row_to_movement(row)
            for _, row in df.iterrows()
        ]

    # ---------------------------------------------------------

    def _row_to_movement(
        self,
        row: pd.Series,
    ) -> Movement:
        
        print("ITEM_CODE :", repr(row.get(COL.ITEM_CODE)))
        print("ITEM_NAME :", repr(row.get(COL.ITEM_NAME)))
        print("QUANTITY  :", repr(row.get(COL.QUANTITY)))
        print("ROW INDEX :", row.index.tolist())
        print("-" * 50)

        return Movement(

            source="MKYS",

            movement_type=self._movement_type(),

            movement_date=parse_date(
                row[COL.DATE]
            ),

            tif_no=self._optional_str(
                row,
                COL.TIF_NO,
            ),

            invoice_no=self._optional_str(
                row,
                COL.INVOICE_NO,
            ),

            amount=self._optional_decimal(
                row,
                COL.TOTAL_AMOUNT,
            ),

            description=self._optional_str(
                row,
                COL.ITEM_DESCRIPTION,
            ),

            warehouse=self._optional_str(
                row,
                COL.WAREHOUSE,
            ),

            budget_type=self._optional_str(
                row,
                COL.BUDGET,
            ),

            stock_code=self._optional_str(
                row,
                COL.ITEM_CODE,
            ),

            stock_name=self._optional_str(
                row,
                COL.ITEM_NAME,
            ),

            supplier=self._optional_str(
                row,
                COL.SUPPLIER,
            ),

            quantity=self._optional_decimal(
                row,
                COL.QUANTITY,
            ),
            
        )
        

    # ---------------------------------------------------------

    def _movement_type(
        self,
    ) -> MovementType:
        """
        Bu parser yalnızca giriş dosyalarını okur.
        """

        return MovementType.ENTRY

    # ---------------------------------------------------------

    def _optional_str(
        self,
        row: pd.Series,
        column: str,
    ) -> str:

        if column not in row.index:
            return ""

        value = row[column]

        if pd.isna(value):
            return ""

        return str(value).strip()

    # ---------------------------------------------------------

    def _optional_decimal(
        self,
        row: pd.Series,
        column: str,
    ) -> Decimal:

        if column not in row.index:
            return Decimal("0")

        return parse_decimal(row[column])