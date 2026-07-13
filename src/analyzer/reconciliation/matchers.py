from __future__ import annotations

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType


class EntryMatcher:
    """
    ENTRY hareketlerini eşleştirir.
    """

    def match(
        self,
        mkys: list[Movement],
        tdms: list[Movement],
    ) -> tuple[
        list[Movement],
        list[Movement],
        list[Movement],
    ]:

        matched: list[Movement] = []

        missing_tdms: list[Movement] = []

        remaining_tdms = tdms.copy()

        for mkys_item in mkys:

            if mkys_item.movement_type != MovementType.ENTRY:
                continue

            found = None

            for tdms_item in remaining_tdms:

                if tdms_item.movement_type != MovementType.ENTRY:
                    continue

                if (
                    mkys_item.tif_no == tdms_item.tif_no
                    and mkys_item.amount == tdms_item.amount
                ):
                    found = tdms_item
                    break

            if found:

                matched.append(mkys_item)

                remaining_tdms.remove(found)

            else:

                missing_tdms.append(mkys_item)

        missing_mkys = remaining_tdms

        return (
            matched,
            missing_tdms,
            missing_mkys,
        )