from __future__ import annotations

from pathlib import Path
from analyzer.constants.mkys_columns import REQUIRED_COLUMNS

import pandas as pd


class MKYSCsvParser:
    """
    MKYS CSV dışa aktarımlarını okur.

    Bu sürümde sadece dosya okunur ve DataFrame döndürülür.
    """

    def parse(self, file_path: Path) -> pd.DataFrame:
        """CSV dosyasını okuyup DataFrame olarak döndürür."""
        df = self._read_csv(file_path)

        self._validate_columns(df)

        return df

    def _read_csv(self, file_path: Path) -> pd.DataFrame:
        """CSV dosyasını pandas ile okur."""
        df = pd.read_csv(
            file_path,
            sep=";",
            encoding="cp1254",
        )

        df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

        return df
    
    def _validate_columns(self, df: pd.DataFrame) -> None:
        missing = [
            column
            for column in REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Eksik MKYS sütunları: {', '.join(missing)}"
            )