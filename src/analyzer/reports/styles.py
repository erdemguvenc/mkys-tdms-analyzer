from __future__ import annotations

from openpyxl.cell import Cell
from openpyxl.styles import (
    Alignment,
    Border,
    Font,
    PatternFill,
    Side,
)
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill

#
# Fonts
#

TITLE_FONT = Font(
    bold=True,
    size=16,
)

HEADER_FONT = Font(
    bold=True,
    color="FFFFFF",
)

NORMAL_FONT = Font(
    bold=False,
)

#
# Fill
#

HEADER_FILL = PatternFill(
    fill_type="solid",
    fgColor="4472C4",
)

#
# Borders
#

THIN_SIDE = Side(
    border_style="thin",
    color="000000",
)

THIN_BORDER = Border(
    left=THIN_SIDE,
    right=THIN_SIDE,
    top=THIN_SIDE,
    bottom=THIN_SIDE,
)

#
# Alignments
#

CENTER_ALIGNMENT = Alignment(
    horizontal="center",
    vertical="center",
)

LEFT_ALIGNMENT = Alignment(
    horizontal="left",
    vertical="center",
)

RIGHT_ALIGNMENT = Alignment(
    horizontal="right",
    vertical="center",
)

#
# Number formats
#

DATE_FORMAT = "DD.MM.YYYY"

DECIMAL_FORMAT = "#,##0.00"

INTEGER_FORMAT = "#,##0"

#
# Difference fills
#

GREEN_FILL = PatternFill(
    fill_type="solid",
    fgColor="C6EFCE",
)

YELLOW_FILL = PatternFill(
    fill_type="solid",
    fgColor="FFEB9C",
)

RED_FILL = PatternFill(
    fill_type="solid",
    fgColor="FFC7CE",
)


def apply_title(
    cell: Cell,
) -> None:
    """
    Başlık hücresini biçimlendirir.
    """

    cell.font = TITLE_FONT
    cell.alignment = LEFT_ALIGNMENT


def apply_header(
    cell: Cell,
) -> None:
    """
    Tablo başlıklarını biçimlendirir.
    """

    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.border = THIN_BORDER
    cell.alignment = CENTER_ALIGNMENT


def apply_text(
    cell: Cell,
) -> None:
    """
    Normal metin hücresi.
    """

    cell.font = NORMAL_FONT
    cell.border = THIN_BORDER
    cell.alignment = LEFT_ALIGNMENT


def apply_date(
    cell: Cell,
) -> None:
    """
    Tarih hücresi.
    """

    cell.font = NORMAL_FONT
    cell.border = THIN_BORDER
    cell.alignment = CENTER_ALIGNMENT
    cell.number_format = DATE_FORMAT


def apply_decimal(
    cell: Cell,
) -> None:
    """
    Ondalıklı sayı hücresi.
    """

    cell.font = NORMAL_FONT
    cell.border = THIN_BORDER
    cell.alignment = RIGHT_ALIGNMENT
    cell.number_format = DECIMAL_FORMAT


def apply_integer(
    cell: Cell,
) -> None:
    """
    Tam sayı hücresi.
    """

    cell.font = NORMAL_FONT
    cell.border = THIN_BORDER
    cell.alignment = RIGHT_ALIGNMENT
    cell.number_format = INTEGER_FORMAT


def apply_currency(
    cell: Cell,
) -> None:
    """
    Para tutarı hücresi.
    """

    cell.font = NORMAL_FONT
    cell.border = THIN_BORDER
    cell.alignment = RIGHT_ALIGNMENT
    cell.number_format = '#,##0.00'


def format_worksheet(
    worksheet: Worksheet,
) -> None:
    """
    Sayfa genel ayarlarını uygular.
    """

    worksheet.freeze_panes = "A4"

    worksheet.auto_filter.ref = worksheet.dimensions

    for column_cells in worksheet.columns:

        length = 0

        column_letter = column_cells[0].column_letter

        for cell in column_cells:

            if cell.value is None:
                continue

            length = max(
                length,
                len(str(cell.value)),
            )

        worksheet.column_dimensions[
            column_letter
        ].width = min(
            max(length + 2, 12),
            50,
        )


def apply_difference_rules(
    worksheet,
    first_row: int,
    last_row: int,
    column: int,
) -> None:
    """
    Difference sütununa koşullu biçimlendirme uygular.

    0      -> Yeşil
    >0     -> Sarı
    <0     -> Kırmızı
    """

    if last_row < first_row:
        return

    from openpyxl.utils import get_column_letter

    column_letter = get_column_letter(column)

    cell_range = (
        f"{column_letter}{first_row}:"
        f"{column_letter}{last_row}"
    )

    worksheet.conditional_formatting.add(
        cell_range,
        CellIsRule(
            operator="equal",
            formula=["0"],
            fill=GREEN_FILL,
        ),
    )

    worksheet.conditional_formatting.add(
        cell_range,
        CellIsRule(
            operator="greaterThan",
            formula=["0"],
            fill=YELLOW_FILL,
        ),
    )

    worksheet.conditional_formatting.add(
        cell_range,
        CellIsRule(
            operator="lessThan",
            formula=["0"],
            fill=RED_FILL,
        ),
    )