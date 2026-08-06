from __future__ import annotations

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.difference import AmountDifference
from analyzer.reconciliation.result import ReconciliationResult


class EntryMatcher:
    """
    MKYS ve TDMS giriş hareketlerini TİF numarasına göre eşleştirir.
    """

    def match(
        self,
        mkys: list[Movement],
        tdms: list[Movement],
    ) -> ReconciliationResult:
        mkys_entries = [
            movement
            for movement in mkys
            if movement.movement_type == MovementType.ENTRY
        ]

        tdms_entries = [
            movement
            for movement in tdms
            if movement.movement_type == MovementType.ENTRY
        ]

        tdms_lookup = {
            movement.tif_no: movement
            for movement in tdms_entries
            if movement.tif_no is not None
        }

        matched: list[Movement] = []
        missing_in_tdms: list[Movement] = []
        amount_differences: list[AmountDifference] = []

        matched_tifs: set[str] = set()

        for mkys_movement in mkys_entries:
            if mkys_movement.tif_no is None:
                missing_in_tdms.append(mkys_movement)
                continue

            tdms_movement = tdms_lookup.get(
                mkys_movement.tif_no,
            )

            if tdms_movement is None:
                missing_in_tdms.append(
                    mkys_movement,
                )
                continue

            matched_tifs.add(
                mkys_movement.tif_no,
            )

            if mkys_movement.amount != tdms_movement.amount:
                amount_differences.append(
                    AmountDifference(
                        mkys=mkys_movement,
                        tdms=tdms_movement,
                    )
                )
            else:
                matched.append(
                    mkys_movement,
                )

        missing_in_mkys = [
            movement for movement in tdms_entries if movement.tif_no not in matched_tifs
        ]

        return ReconciliationResult(
            matched=matched,
            missing_in_tdms=missing_in_tdms,
            missing_in_mkys=missing_in_mkys,
            amount_differences=amount_differences,
        )
