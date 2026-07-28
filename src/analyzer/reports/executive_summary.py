from __future__ import annotations

from dataclasses import dataclass

from analyzer.reports.dashboard_summary import DashboardSummary


@dataclass(slots=True)
class ExecutiveSummary:
    """
    Dashboard'da gösterilecek yönetici özetini oluşturur.
    """

    def build(
        self,
        summary: DashboardSummary,
    ) -> list[str]:

        lines: list[str] = []

        total = summary.total_records

        if total == 0:

            lines.append(
                "İşlenecek kayıt bulunamadı."
            )

            return lines

        match_rate = (
            summary.matched_records
            / total
            * 100
        )

        lines.append(
            f"Uzlaştırma Oranı: %{match_rate:.1f}"
        )

        lines.append(
            f"{summary.matched_records} kayıt başarıyla eşleşti."
        )

        if summary.amount_difference_count:

            lines.append(
                f"{summary.amount_difference_count} tutar farkı tespit edildi."
            )

        if summary.consumption_difference_count:

            lines.append(
                f"{summary.consumption_difference_count} tüketim farkı tespit edildi."
            )

        if (
            summary.amount_difference_count == 0
            and summary.consumption_difference_count == 0
        ):

            lines.append(
                "Herhangi bir fark bulunmadı."
            )

        return lines