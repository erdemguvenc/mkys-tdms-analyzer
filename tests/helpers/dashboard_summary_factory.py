from analyzer.reports.analytics.supplier_summary import SupplierSummary
from analyzer.reports.analytics.trend_summary import TrendSummary
from analyzer.reports.dashboard_summary import DashboardSummary


def dashboard_summary(
    *,
    total_records: int = 10,
    matched_records: int = 8,
    missing_in_mkys: int = 1,
    missing_in_tdms: int = 1,
    amount_difference_count: int = 1,
    consumption_difference_count: int = 1,
    trend: TrendSummary | None = None,
    suppliers: list[SupplierSummary] | None = None,
) -> DashboardSummary:

    if trend is None:
        trend = TrendSummary(
            months=[],
        )

    if suppliers is None:
        suppliers = []

    return DashboardSummary(
        total_records=total_records,
        matched_records=matched_records,
        missing_in_mkys=missing_in_mkys,
        missing_in_tdms=missing_in_tdms,
        amount_difference_count=amount_difference_count,
        consumption_difference_count=consumption_difference_count,
        trend=trend,
        suppliers=suppliers,
    )