from __future__ import annotations

from pathlib import Path

import pandas as pd

from analyzer.constants import tdms_columns as COL


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
    ) -> pd.DataFrame:

        df = self._read_xls(file_path)

        self._validate_columns(df)

        return df

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