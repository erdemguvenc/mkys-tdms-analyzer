from __future__ import annotations

from collections import defaultdict
from decimal import Decimal
from typing import Iterable

from analyzer.models.movement import Movement

from .consumption import ConsumptionMatch
from .difference import AmountDifference, ConsumptionDifference
from .result import ReconciliationResult
from .rules import (
    RECONCILIATION_RULES,
    Cardinality,
    ReconciliationKey,
)


class Reconciler:
    """
    MKYS ve TDMS hareketlerini reconciliation kurallarına göre uzlaştırır.

    Bu ilk implementasyon yalnızca iki temel stratejiyi destekler:

    - TIF + ONE_TO_ONE
    - MONTH + MANY_TO_ONE

    Hareket türünün hangi stratejiye tabi olduğu
    RECONCILIATION_RULES üzerinden belirlenir.
    """

    def reconcile(
        self,
        mkys_movements: Iterable[Movement],
        tdms_movements: Iterable[Movement],
    ) -> ReconciliationResult:
        """
        MKYS ve TDMS hareketlerini uzlaştırır.

        Parameters
        ----------
        mkys_movements:
            MKYS hareketleri.

        tdms_movements:
            TDMS hareketleri.

        Returns
        -------
        ReconciliationResult
            Uzlaştırma sonucu.
        """

        mkys = list(mkys_movements)
        tdms = list(tdms_movements)

        result = ReconciliationResult()

        movement_types = {movement.movement_type for movement in mkys} | {
            movement.movement_type for movement in tdms
        }

        for movement_type in movement_types:
            rule = RECONCILIATION_RULES.get(movement_type)

            if rule is None:
                continue

            mkys_group = [
                movement for movement in mkys if movement.movement_type == movement_type
            ]

            tdms_group = [
                movement for movement in tdms if movement.movement_type == movement_type
            ]

            if rule.cardinality is Cardinality.ONE_TO_ONE:
                self._reconcile_one_to_one(
                    mkys_group,
                    tdms_group,
                    rule.key,
                    result,
                )

            elif rule.cardinality is Cardinality.MANY_TO_ONE:
                self._reconcile_many_to_one(
                    mkys_group,
                    tdms_group,
                    rule.key,
                    result,
                )

        return result

    def _reconcile_one_to_one(
        self,
        mkys_movements: list[Movement],
        tdms_movements: list[Movement],
        key: ReconciliationKey,
        result: ReconciliationResult,
    ) -> None:
        """
        ONE_TO_ONE reconciliation uygular.

        Aynı reconciliation key'e sahip MKYS ve TDMS kayıtları
        birebir eşleştirilir.

        Eşleşen kayıtların tutarları farklıysa
        AmountDifference oluşturulur.
        """

        if key is not ReconciliationKey.TIF:
            raise ValueError(
                "ONE_TO_ONE reconciliation yalnızca ReconciliationKey.TIF destekliyor."
            )

        mkys_by_tif = {
            movement.tif_no: movement
            for movement in mkys_movements
            if movement.tif_no is not None
        }

        tdms_by_tif = {
            movement.tif_no: movement
            for movement in tdms_movements
            if movement.tif_no is not None
        }

        all_tifs = set(mkys_by_tif) | set(tdms_by_tif)

        for tif_no in all_tifs:
            mkys_movement = mkys_by_tif.get(tif_no)
            tdms_movement = tdms_by_tif.get(tif_no)

            if mkys_movement is None:
                if tdms_movement is not None:
                    result.missing_in_mkys.append(tdms_movement)
                continue

            if tdms_movement is None:
                result.missing_in_tdms.append(mkys_movement)
                continue

            if mkys_movement.amount != tdms_movement.amount:
                result.amount_differences.append(
                    AmountDifference(
                        mkys=mkys_movement,
                        tdms=tdms_movement,
                    )
                )
                continue

            result.matched.append(mkys_movement)

    def _reconcile_many_to_one(
        self,
        mkys_movements: list[Movement],
        tdms_movements: list[Movement],
        key: ReconciliationKey,
        result: ReconciliationResult,
    ) -> None:
        """
        MANY_TO_ONE reconciliation uygular.

        CONSUMPTION hareketleri aylık toplam üzerinden karşılaştırılır.

        Örneğin:

            MKYS:
                05.01 → 100 TL
                12.01 → 150 TL
                25.01 → 250 TL

            TDMS:
                Ocak → 500 TL

        sonucunda tek bir ConsumptionMatch oluşturulur.
        """

        if key is not ReconciliationKey.MONTH:
            raise ValueError(
                "MANY_TO_ONE reconciliation yalnızca "
                "ReconciliationKey.MONTH destekliyor."
            )

        mkys_by_month: dict[tuple[int, int], list[Movement]] = defaultdict(list)
        tdms_by_month: dict[tuple[int, int], list[Movement]] = defaultdict(list)

        for movement in mkys_movements:
            month_key = (
                movement.movement_date.year,
                movement.movement_date.month,
            )
            mkys_by_month[month_key].append(movement)

        for movement in tdms_movements:
            month_key = (
                movement.movement_date.year,
                movement.movement_date.month,
            )
            tdms_by_month[month_key].append(movement)

        all_months = set(mkys_by_month) | set(tdms_by_month)

        for year, month in sorted(all_months):
            mkys_month_movements = mkys_by_month.get(
                (year, month),
                [],
            )

            tdms_month_movements = tdms_by_month.get(
                (year, month),
                [],
            )

            mkys_amount = sum(
                (movement.amount for movement in mkys_month_movements),
                Decimal("0"),
            )

            tdms_amount = sum(
                (movement.amount for movement in tdms_month_movements),
                Decimal("0"),
            )

            if mkys_amount == tdms_amount:
                result.consumption_matched.append(
                    ConsumptionMatch(
                        year=year,
                        month=month,
                        mkys_amount=mkys_amount,
                        tdms_amount=tdms_amount,
                    )
                )
                continue

            result.consumption_differences.append(
                ConsumptionDifference(
                    year=year,
                    month=month,
                    mkys_amount=mkys_amount,
                    tdms_amount=tdms_amount,
                )
            )
