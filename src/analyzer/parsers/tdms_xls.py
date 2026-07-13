from __future__ import annotations

from pathlib import Path
from datetime import date,datetime
from decimal import Decimal

import pandas as pd

from analyzer.constants import tdms_columns as COL

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType


class TDMSXlsParser:
    """
    TDMS XLS parser.

    v2.2
    - XLS dosyasını okur.
    - Gerçek başlık satırını otomatik bulur.
    - Başlıkları doğrular.
    """

    def parse(
        self,
        file_path: Path,
    ) -> list[Movement]:

        df = self._read_xls(file_path)

        self._validate_columns(df)

        return self._create_movements(df)

    def _read_xls(
        self,
        file_path: Path,
    ) -> pd.DataFrame:

        # Dosyayı başlıksız oku
        df = pd.read_excel(
            file_path,
            engine="xlrd",
            header=None,
        )

        # Gerçek başlık satırını bul
        header_row = None

        for i in range(len(df)):
            value = str(df.iloc[i, 2]).strip()

            if value == COL.DATE:
                header_row = i
                break

        if header_row is None:
            raise ValueError(
                "TDMS başlık satırı bulunamadı."
            )

        # Başlığı ayarla
        df.columns = (
            df.iloc[header_row]
            .astype(str)
            .str.strip()
        )

        # Başlık satırını kaldır
        df = (
            df.iloc[header_row + 1 :]
            .reset_index(drop=True)
        )

        # Tamamen boş sütunları kaldır
        df = df.dropna(axis=1, how="all")

        # Sütun isimlerini temizle
        df.columns = (
            df.columns.astype(str)
            .str.strip()
        )

        # Tarihi olmayan veya geçersiz satırları kaldır
        df = df[
            df[COL.DATE]
            .astype(str)
            .str.match(r"\d{2}\.\d{2}\.\d{4}", na=False)
        ]

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
                f"Eksik TDMS sütunları: {', '.join(missing)}"
            )
        

    def _create_movements(
        self,
        df: pd.DataFrame,
    ) -> list[Movement]:
        
        for index, row in df.iterrows():
            print(index, repr(row[COL.DATE]))

        return [
            self._row_to_movement(row)
            for _, row in df.iterrows()
        ]
       

    def _row_to_movement(
        self,
        row: pd.Series,
    ) -> Movement:

        debit = Decimal(str(row[COL.DEBIT] or 0))
        credit = Decimal(str(row[COL.CREDIT] or 0))

        amount = debit if debit > 0 else credit

        return Movement(
            source="TDMS",

            movement_type=MovementType.ENTRY,

            movement_date=self._parse_date(
                row[COL.DATE]
            ),

            tif_no=str(row[COL.TIF_NO]),

            voucher_no=str(row[COL.VOUCHER_NO]),

            invoice_no=str(row[COL.INVOICE_NO]),

            amount=amount,

            description=str(row[COL.DESCRIPTION]),

            supplier=str(row[COL.SUPPLIER]),
        )   
    

    def _parse_date(
        self,
        value: str,
    ) -> date:

        return datetime.strptime(
            str(value).strip(),
            "%d.%m.%Y",
        ).date()
    

    def _parse_decimal(
        self,
        value: object,
    ) -> Decimal:

        text = str(value).strip()

        if (
            not text
            or text.lower() == "nan"
        ):
            return Decimal("0")

        text = text.replace(".", "")
        text = text.replace(",", ".")

        return Decimal(text)