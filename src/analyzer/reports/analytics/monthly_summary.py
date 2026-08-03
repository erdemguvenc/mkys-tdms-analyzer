from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MonthlySummary:
    """
    Tek bir aya ait uzlaştırma özeti.
    """

    month: str

    total_records: int

    matched_records: int

    missing_in_mkys: int

    missing_in_tdms: int

    amount_difference_count: int

    consumption_difference_count: int

    @property
    def match_rate(self) -> float:
        """
        Uzlaştırma oranı (%).
        """

        if self.total_records == 0:
            return 0.0

        return self.matched_records / self.total_records * 100

    @property
    def difference_count(self) -> int:
        """
        Toplam farklılık sayısı.
        """

        return (
            self.missing_in_mkys
            + self.missing_in_tdms
            + self.amount_difference_count
            + self.consumption_difference_count
        )

    @property
    def label(self) -> str:
        """
        Grafikte gösterilecek ay etiketi.
        """

        year, month = self.month.split("-")

        month_names = {
            "01": "Oca",
            "02": "Şub",
            "03": "Mar",
            "04": "Nis",
            "05": "May",
            "06": "Haz",
            "07": "Tem",
            "08": "Ağu",
            "09": "Eyl",
            "10": "Eki",
            "11": "Kas",
            "12": "Ara",
        }

        return f"{month_names[month]} {year}"
