from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.result import ReconciliationResult
from analyzer.reports.excel_report_builder import ExcelReportBuilder


def movement() -> Movement:

    return Movement(
        source="MKYS",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 1, 1),
        tif_no="1",
        voucher_no="",
        document_no="",
        invoice_no="",
        amount=Decimal("100"),
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