from __future__ import annotations

from pathlib import Path

import pandas as pd


class MKYSCsvParser:
    """
    MKYS CSV dışa aktarımlarını okur.

    Bu sürümde sadece dosya okunur ve DataFrame döndürülür.
    """

    def parse(self, file_path: Path) -> pd.DataFrame:
        """CSV dosyasını okuyup DataFrame olarak döndürür."""
        return self._read_csv(file_path)

    def _read_csv(self, file_path: Path) -> pd.DataFrame:
        """CSV dosyasını pandas ile okur."""
        return pd.read_csv(
            file_path,
            sep=";",
            encoding="cp1254",
        )