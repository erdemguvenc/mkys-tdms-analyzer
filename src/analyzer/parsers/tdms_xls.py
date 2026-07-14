from __future__ import annotations

from pathlib import Path

import pandas as pd

from analyzer.constants import tdms_columns as COL
from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.utils import parse_date
from analyzer.utils import parse_decimal


class TDMSXlsParser:
    """
    TDMS XLS Parser

    v3.5

    Özellikler
    ----------
    - XLS dosyasını okur.
    - Başlık satırını otomatik bulur.
    - Alt bilgi / imza satırlarını temizler.
    - Zorunlu sütunları doğrular.
    - Hareketleri ortak Movement modeline dönüştürür.
    """

    def parse(
        self,
        file_path: Path,
    ) -> list[Movement]:

        df = self._read_xls(file_path)

        self._validate_columns(df)

        return self._create_movements(df)

    # ---------------------------------------------------------

    def _read_xls(
        self,
        file_path: Path,
    ) -> pd.DataFrame:

        df = pd.read_excel(
            file_path,
            engine="xlrd",
            header=None,
        )

        header_row = self._find_header_row(df)

        df.columns = (
            df.iloc[header_row]
            .astype(str)
            .str.strip()
        )

        df = (
            df.iloc[header_row + 1 :]
            .reset_index(drop=True)
        )

        return self._cleanup_dataframe(df)

    # ---------------------------------------------------------

    def _find_header_row(
        self,
        df: pd.DataFrame,
    ) -> int:
        """
        Gerçek sütun başlığının bulunduğu satırı bulur.
        """

        for index in range(len(df)):

            row = (
                df.iloc[index]
                .astype(str)
                .str.strip()
            )

            if (
                COL.DATE in row.values
                and COL.VOUCHER_NO in row.values
                and COL.DEBIT in row.values
            ):
                return index

        raise ValueError(
            "TDMS başlık satırı bulunamadı."
        )
    

        # ---------------------------------------------------------

    def _cleanup_dataframe(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Veri çerçevesini temizler.

        - Tamamen boş sütunları kaldırır.
        - Tamamen boş satırları kaldırır.
        - Sütun adlarını normalize eder.
        - TDMS raporunun sonundaki imza ve açıklama satırlarını temizler.
        """

        # Boş sütunlar
        df = df.dropna(axis=1, how="all")

        # Sütun adlarını temizle
        df.columns = (
            df.columns.astype(str)
            .str.replace("\ufeff", "", regex=False)
            .str.strip()
        )

        cleaned_rows = []

        for _, row in df.iterrows():

            date_value = row.get(COL.DATE)

            if pd.isna(date_value):
                continue

            text = str(date_value).strip()

            if text == "":
                continue

            # İmza satırları
            if text.startswith("DÜZENLEYEN"):
                break

            if "Kayıt ve Mevcutlara Uygundur" in text:
                break

            # Tarih olmayan satırları alma
            try:
                parse_date(text)
            except Exception:
                continue

            cleaned_rows.append(row)

        df = pd.DataFrame(
            cleaned_rows,
            columns=df.columns,
        )

        return df.reset_index(drop=True)

    # ---------------------------------------------------------

    def _validate_columns(
        self,
        df: pd.DataFrame,
    ) -> None:
        """
        Zorunlu TDMS sütunlarını doğrular.
        """

        missing = [
            column
            for column in COL.REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing:
            raise ValueError(
                "Eksik TDMS sütunları: "
                + ", ".join(missing)
            )

    # ---------------------------------------------------------

    def _create_movements(
        self,
        df: pd.DataFrame,
    ) -> list[Movement]:
        """
        DataFrame'i Movement listesine dönüştürür.
        """

        return [
            self._row_to_movement(row)
            for _, row in df.iterrows()
        ]
    

        # ---------------------------------------------------------

    def _row_to_movement(
        self,
        row: pd.Series,
    ) -> Movement:
        """
        TDMS satırını ortak Movement modeline dönüştürür.
        """

        debit = self._optional_decimal(
            row,
            COL.DEBIT,
        )

        credit = self._optional_decimal(
            row,
            COL.CREDIT,
        )

        amount = (
            debit
            if debit > 0
            else credit
        )

        return Movement(

            source="TDMS",

            movement_type=MovementType.ENTRY,

            movement_date=parse_date(
                row[COL.DATE]
            ),

            tif_no=self._optional_str(
                row,
                COL.TIF_NO,
            ),

            voucher_no=self._optional_str(
                row,
                COL.VOUCHER_NO,
            ),

            invoice_no=self._optional_str(
                row,
                COL.INVOICE_NO,
            ),

            amount=amount,

            description=self._optional_str(
                row,
                COL.DESCRIPTION,
            ),

            supplier=self._optional_str(
                row,
                COL.SUPPLIER,
            ),
        )

    # ---------------------------------------------------------

    def _optional_str(
        self,
        row: pd.Series,
        column: str,
    ) -> str:
        """
        Opsiyonel metin alanını güvenli şekilde döndürür.
        """

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
    ):
        """
        Opsiyonel sayısal alanı güvenli şekilde döndürür.
        """

        if column not in row.index:
            return parse_decimal(0)

        return parse_decimal(
            row[column]
        )