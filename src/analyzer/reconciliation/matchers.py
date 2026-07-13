from __future__ import annotations

from collections import defaultdict

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType

from .difference import AmountDifference


class EntryMatcher:
    """
    ENTRY hareketlerini eşleştirir.

    Eşleştirme önceliği:

        1. TİF No
        2. Tutar

    Sonuçlar:

        matched
        missing_in_tdms
        missing_in_mkys
        amount_differences
    """

    def match(
        self,
        mkys: list[Movement],
        tdms: list[Movement],
    ) -> tuple[
        list[Movement],
        list[Movement],
        list[Movement],
        list[AmountDifference],
    ]:

        lookup = self._build_lookup(tdms)

        matched: list[Movement] = []
        missing_tdms: list[Movement] = []
        amount_differences: list[AmountDifference] = []

        for mkys_item in mkys:

            if mkys_item.movement_type != MovementType.ENTRY:
                continue

            key = (
                mkys_item.tif_no,
                MovementType.ENTRY,
            )

            candidates = lookup.get(key)

            if not candidates:

                missing_tdms.append(mkys_item)
                continue

            tdms_item = candidates.pop(0)

            if not candidates:
                lookup.pop(key)

            if mkys_item.amount == tdms_item.amount:

                matched.append(mkys_item)

            else:

                amount_differences.append(
                    AmountDifference(
                        mkys=mkys_item,
                        tdms=tdms_item,
                    )
                )

        missing_mkys: list[Movement] = []

        for candidates in lookup.values():
            missing_mkys.extend(candidates)

        return (
            matched,
            missing_tdms,
            missing_mkys,
            amount_differences,
        )

    def _build_lookup(
        self,
        movements: list[Movement],
    ) -> dict[
        tuple[str | None, MovementType],
        list[Movement],
    ]:
        """
        TDMS hareketlerini hızlı arama için indeksler.

        Aynı TİF numarasına sahip birden fazla kayıt
        bulunabileceği için her anahtar bir liste tutar.
        """

        lookup: dict[
            tuple[str | None, MovementType],
            list[Movement],
        ] = defaultdict(list)

        for movement in movements:

            if movement.movement_type != MovementType.ENTRY:
                continue

            key = (
                movement.tif_no,
                movement.movement_type,
            )

            lookup[key].append(movement)

        return lookup