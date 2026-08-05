from __future__ import annotations

from analyzer.reports.analytics.supplier_summary import SupplierSummary
from analyzer.reports.analytics.top_difference_summary import TopDifferenceSummary
from analyzer.reports.analytics.trend_summary import TrendSummary
from analyzer.reports.analytics.warehouse_summary import WarehouseSummary
from analyzer.reports.dashboard_summary import DashboardSummary


def create_dashboard_summary(
    *,
    total_records: int = 10,
    matched_records: int = 8,
    missing_in_mkys: int = 1,
    missing_in_tdms: int = 1,
    amount_difference_count: int = 1,
    consumption_difference_count: int = 1,
    trend: TrendSummary | None = None,
    suppliers: list[SupplierSummary] | None = None,
    warehouses: list[WarehouseSummary] | None = None,
    top_differences: list[TopDifferenceSummary] | None = None,
) -> DashboardSummary:
    if trend is None:
        trend = TrendSummary(
            months=[],
        )

    if suppliers is None:
        suppliers = []

    if warehouses is None:
        warehouses = []

    if top_differences is None:
        top_differences = []

    return DashboardSummary(
        total_records=total_records,
        matched_records=matched_records,
        missing_in_mkys=missing_in_mkys,
        missing_in_tdms=missing_in_tdms,
        amount_difference_count=amount_difference_count,
        consumption_difference_count=consumption_difference_count,
        trend=trend,
        suppliers=suppliers,
        warehouses=warehouses,
        top_differences=top_differences,
    )
