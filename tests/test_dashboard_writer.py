from __future__ import annotations

from openpyxl import Workbook

from analyzer.reconciliation.result import ReconciliationResult
from analyzer.reports.dashboard_summary import DashboardSummary
from analyzer.reports.dashboard_writer import DashboardWriter

from openpyxl.chart import PieChart


def build_summary() -> DashboardSummary:

    result = ReconciliationResult(
        matched=[object(), object()],
        missing_in_tdms=[object()],
        missing_in_mkys=[object(), object(), object()],
        amount_differences=[object()],
        consumption_differences=[object(), object()],
    )

    return DashboardSummary.from_result(result)


def test_dashboard_title() -> None:

    workbook = Workbook()

    worksheet = workbook.active

    writer = DashboardWriter()

    writer.write_dashboard(
        worksheet,
        build_summary(),
    )

    assert worksheet["A1"].value == (
        "MKYS - TDMS Uzlaştırma Dashboard"
    )


def test_dashboard_kpi_titles() -> None:

    workbook = Workbook()

    worksheet = workbook.active

    writer = DashboardWriter()

    writer.write_dashboard(
        worksheet,
        build_summary(),
    )

    assert worksheet["A3"].value == "Toplam Kayıt"
    assert worksheet["D3"].value == "Eşleşen Kayıt"
    assert worksheet["G3"].value == "MKYS Eksik"
    assert worksheet["J3"].value == "TDMS Eksik"
    assert worksheet["A7"].value == "Tutar Farkı"
    assert worksheet["D7"].value == "Tüketim Farkı"


def test_dashboard_kpi_values() -> None:

    workbook = Workbook()

    worksheet = workbook.active

    writer = DashboardWriter()

    writer.write_dashboard(
        worksheet,
        build_summary(),
    )

    assert worksheet["A4"].value == 3
    assert worksheet["D4"].value == 2
    assert worksheet["G4"].value == 3
    assert worksheet["J4"].value == 1
    assert worksheet["A8"].value == 1
    assert worksheet["D8"].value == 2


def test_dashboard_prepared() -> None:

    workbook = Workbook()

    worksheet = workbook.active

    writer = DashboardWriter()

    writer.write_dashboard(
        worksheet,
        build_summary(),
    )

    assert worksheet.freeze_panes == "A4"

    assert worksheet.auto_filter.ref is not None


def test_dashboard_contains_pie_chart() -> None:

    workbook = Workbook()

    worksheet = workbook.active

    writer = DashboardWriter()

    writer.write_dashboard(
        worksheet,
        build_summary(),
    )

    assert len(worksheet._charts) == 2

    assert isinstance(
        worksheet._charts[0],
        PieChart,
    )


def test_dashboard_contains_pie_chart() -> None:
    """
    Dashboard sayfasına PieChart eklendiğini doğrular.
    """

    workbook = Workbook()

    worksheet = workbook.active

    writer = DashboardWriter()

    writer.write_dashboard(
        worksheet,
        build_summary(),
    )

    #
    # Dashboard'da yalnızca bir grafik olmalı
    #
    assert len(worksheet._charts) == 1

    chart = worksheet._charts[0]

    #
    # Grafik tipi PieChart olmalı
    #
    assert isinstance(
        chart,
        PieChart,
    )

    #
    # Grafik başlığı atanmış olmalı
    #
    assert chart.title is not None