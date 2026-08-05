from analyzer.reports.executive_summary import ExecutiveSummary
from analyzer.reports.report_status import ReportStatus

from .helpers.dashboard_summary_factory import create_dashboard_summary


def test_executive_summary_good_status() -> None:
    summary = create_dashboard_summary(
        total_records=100,
        matched_records=100,
        missing_in_mkys=0,
        missing_in_tdms=0,
        amount_difference_count=0,
        consumption_difference_count=0,
    )

    result = ExecutiveSummary().build(summary)

    assert result.status is ReportStatus.GOOD

    assert "Uzlaştırma Oranı: %100.0" in result.lines[0]

    assert "100 kayıt başarıyla eşleşti." in result.lines[1]

    assert "✔ Uzlaştırma başarıyla tamamlandı." in result.lines[-1]


def test_executive_summary_warning_status() -> None:
    summary = create_dashboard_summary(
        total_records=10,
        matched_records=9,
        missing_in_mkys=1,
        missing_in_tdms=0,
        amount_difference_count=2,
        consumption_difference_count=1,
    )

    result = ExecutiveSummary().build(summary)

    assert result.status is ReportStatus.WARNING

    assert "⚠ Birkaç kayıt manuel kontrol gerektiriyor." in result.lines[-1]


def test_executive_summary_critical_status() -> None:
    summary = create_dashboard_summary(
        total_records=10,
        matched_records=5,
        missing_in_mkys=3,
        missing_in_tdms=2,
        amount_difference_count=12,
        consumption_difference_count=5,
    )

    result = ExecutiveSummary().build(summary)

    assert result.status is ReportStatus.CRITICAL

    assert "✖ Çok sayıda farklılık tespit edildi." in result.lines[-1]
