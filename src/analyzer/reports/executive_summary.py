from __future__ import annotations

from dataclasses import dataclass

from analyzer.reports.dashboard_summary import DashboardSummary
from analyzer.reports.report_status import ReportStatus

@dataclass(slots=True)
class ExecutiveSummaryResult:
    """
    Dashboard'da gösterilecek yönetici özeti.
    """

    status: ReportStatus
    lines: list[str]

@dataclass(slots=True)
class ExecutiveSummary:
    """
    Dashboard'da gösterilecek yönetici özetini oluşturur.
    """

    def build(
        self,
        summary: DashboardSummary,
    ) -> ExecutiveSummaryResult:

        lines: list[str] = []

        total = summary.total_records

        if total == 0:

            return ExecutiveSummaryResult(
                status=ReportStatus.WARNING,
                lines=[
                    "İşlenecek kayıt bulunamadı.",
                ],
            )

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

        #
        # Durum belirleme
        #
        if (
            summary.amount_difference_count == 0
            and summary.consumption_difference_count == 0
        ):

            status = ReportStatus.GOOD

            lines.append(
                "✔ Uzlaştırma başarıyla tamamlandı."
            )

        elif (
            summary.amount_difference_count <= 5
            and summary.consumption_difference_count <= 2
        ):

            status = ReportStatus.WARNING

            lines.append(
                "⚠ Birkaç kayıt manuel kontrol gerektiriyor."
            )

        else:

            status = ReportStatus.CRITICAL

            lines.append(
                "✖ Çok sayıda farklılık tespit edildi."
            )

        return ExecutiveSummaryResult(
            status=status,
            lines=lines,
        )        
