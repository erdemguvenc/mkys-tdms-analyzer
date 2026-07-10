from __future__ import annotations

from pathlib import Path

from analyzer.models.movement import Movement


class MKYSCsvParser:
    """
    MKYS CSV dosyalarını okur ve Movement nesnelerine dönüştürür.
    """

    def read(self, file_path: str | Path) -> list[Movement]:
        raise NotImplementedError