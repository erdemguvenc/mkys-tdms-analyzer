from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path

from analyzer.reconciliation.result import ReconciliationResult


class ReportBuilder(ABC):
    """
    Uzlaştırma sonuçlarından rapor üreten sınıfların temel arayüzü.
    """

    @abstractmethod
    def build(
        self,
        result: ReconciliationResult,
        output_file: Path,
    ) -> None:
        """
        Uzlaştırma sonucundan bir rapor üretir.

        Parameters
        ----------
        result:
            Uzlaştırma sonucu.

        output_file:
            Oluşturulacak rapor dosyasının yolu.
        """
        raise NotImplementedError