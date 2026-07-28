from __future__ import annotations

from openpyxl import Workbook

from analyzer.reconciliation.result import ReconciliationResult
from analyzer.reports.dashboard_summary import DashboardSummary
from analyzer.reports.dashboard_writer import DashboardWriter

from openpyxl.chart import PieChart ,BarChart



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

    assert worksheet["A8"].value == "📊 Toplam Kayıt"
    assert worksheet["D8"].value == "✔ Eşleşen Kayıt"
    assert worksheet["G8"].value == "⚠ MKYS Eksik"
    assert worksheet["J8"].value == "⚠ TDMS Eksik"
    assert worksheet["A12"].value == "💰 Tutar Farkı"
    assert worksheet["D12"].value == "📦 Tüketim Farkı" 


def test_dashboard_kpi_values() -> None:

    workbook = Workbook()

    worksheet = workbook.active

    writer = DashboardWriter()

    writer.write_dashboard(
        worksheet,
        build_summary(),
    )

    summary = build_summary()

    assert worksheet["A9"].value == summary.total_records
    assert worksheet["D9"].value == summary.matched_records
    assert worksheet["G9"].value == summary.missing_in_mkys
    assert worksheet["J9"].value == summary.missing_in_tdms

    assert worksheet["A13"].value == summary.amount_difference_count
    assert worksheet["D13"].value == summary.consumption_difference_count


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

    # Dashboard'da 2 grafik olmalı
    assert len(worksheet._charts) == 2

    chart = worksheet._charts[0]

    assert isinstance(
        chart,
        PieChart,
    )

    assert chart.title is not None


def test_dashboard_contains_bar_chart() -> None:

    workbook = Workbook()

    worksheet = workbook.active

    writer = DashboardWriter()

    writer.write_dashboard(
        worksheet,
        build_summary(),
    )

    chart = worksheet._charts[1]

    assert isinstance(
        chart,
        BarChart,
    )

    assert chart.title is not None


def test_dashboard_chart_types() -> None:

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

    assert isinstance(
        worksheet._charts[1],
        BarChart,
    )


def test_dashboard_chart_titles() -> None:

    workbook = Workbook()

    worksheet = workbook.active

    writer = DashboardWriter()

    writer.write_dashboard(
        worksheet,
        build_summary(),
    )

    assert len(worksheet._charts) == 2

    assert worksheet._charts[0].title is not None
    assert worksheet._charts[1].title is not None


def test_dashboard_executive_summary() -> None:

    workbook = Workbook()
    worksheet = workbook.active

    writer = DashboardWriter()

    writer.write_dashboard(
        worksheet,
        build_summary(),
    )

    # Başlıkta durum ikonu olmalı
    assert worksheet["A2"].value.endswith("Executive Summary")

    # İlk satır uzlaştırma oranını göstermeli
    assert worksheet["A3"].value.startswith("Uzlaştırma Oranı")

    # İkinci satır eşleşen kayıt bilgisini göstermeli
    assert "kayıt başarıyla eşleşti" in worksheet["A4"].value


def test_dashboard_quality_progress() -> None:

    workbook = Workbook()

    worksheet = workbook.active

    writer = DashboardWriter()

    writer.write_dashboard(
        worksheet,
        build_summary(),
    )

    assert worksheet["J7"].value == "Kalite"

    assert worksheet["K7"].value is not None

    assert worksheet["K7"].number_format == "0%"

    assert len(
        worksheet.conditional_formatting
    ) == 1