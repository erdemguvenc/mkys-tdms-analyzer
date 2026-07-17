from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.result import ReconciliationResult
from analyzer.reports.excel_report_builder import ExcelReportBuilder
from analyzer.reconciliation.difference import (
    AmountDifference,
    ConsumptionDifference,
)

from openpyxl import load_workbook


def movement(
    *,
    amount: Decimal = Decimal("100"),
) -> Movement:

    return Movement(
        source="MKYS",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 1, 1),
        tif_no="1",
        voucher_no="",
        document_no="",
        invoice_no="",
        amount=amount,
        description="",
        warehouse="",
        budget_type="",
        stock_code="",
        stock_name="",
        supplier="",
        quantity=Decimal("1"),
    )


def test_excel_report_is_created(
    tmp_path: Path,
) -> None:

    result = ReconciliationResult(
        matched=[movement()],
    )

    output = tmp_path / "report.xlsx"

    builder = ExcelReportBuilder()

    builder.build(
        result,
        output,
    )

    assert output.exists()


def test_excel_report_is_not_empty(
    tmp_path: Path,
) -> None:

    output = tmp_path / "report.xlsx"

    builder = ExcelReportBuilder()

    builder.build(
        ReconciliationResult(),
        output,
    )

    assert output.stat().st_size > 0


def test_consumption_difference_sheet_has_conditional_formatting(
    tmp_path: Path,
) -> None:

    difference = ConsumptionDifference(
        year=2026,
        month=1,
        mkys_amount=Decimal("100"),
        tdms_amount=Decimal("80"),
    )

    result = ReconciliationResult(
        consumption_differences=[
            difference,
        ],
    )

    output = tmp_path / "report.xlsx"

    builder = ExcelReportBuilder()

    builder.build(
        result,
        output,
    )

    workbook = load_workbook(output)

    sheet = workbook["6_Tüketim_Farkları"]

    assert len(sheet.conditional_formatting) > 0


def test_worksheet_page_setup(
    tmp_path: Path,
) -> None:

    output = tmp_path / "report.xlsx"

    builder = ExcelReportBuilder()

    builder.build(
        ReconciliationResult(
            matched=[movement()],
        ),
        output,
    )

    workbook = load_workbook(output)

    sheet = workbook["2_Giriş_Eşleşen"]

    #
    # Freeze Panes
    #
    assert sheet.freeze_panes == "A4"

    #
    # AutoFilter
    #
    assert sheet.auto_filter.ref is not None

    #
    # Landscape
    #
    assert (
        sheet.page_setup.orientation
        == sheet.ORIENTATION_LANDSCAPE
    )

    #
    # A4
    #
    assert int(sheet.page_setup.paperSize) == 9

    #
    # Print titles
    #
    assert sheet.print_title_rows.replace("$", "") == "1:3"