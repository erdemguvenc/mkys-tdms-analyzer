from __future__ import annotations

from analyzer.models.movement import Movement


class OpeningMatcher:
    """
    MKYS ve TDMS açılış kayıtlarını uzlaştırır.

    İlk sürümde:

    - MKYS açılışı:
        tif_no == "0"

    - TDMS açılışı:
        description içerisinde
        "MUHASEBE AÇILIŞ FİŞİ"
        geçen kayıt.

    Eşleştirme anahtarı:

        amount
    """

    OPENING_DESCRIPTION = "MUHASEBE AÇILIŞ FİŞİ"

    def match(
        self,
        mkys: list[Movement],
        tdms: list[Movement],
    ) -> tuple[
        list[Movement],
        list[Movement],
        list[Movement],
    ]:

        mkys_openings = self._mkys_openings(
            mkys,
        )

        tdms_openings = self._tdms_openings(
            tdms,
        )

        matched: list[Movement] = []

        missing_in_tdms: list[Movement] = []

        missing_in_mkys: list[Movement] = []

        remaining_tdms = tdms_openings.copy()

        for mkys_movement in mkys_openings:

            tdms_match = self._find_match(
                mkys_movement,
                remaining_tdms,
            )

            if tdms_match is None:

                missing_in_tdms.append(
                    mkys_movement,
                )

                continue

            matched.append(
                mkys_movement,
            )

            remaining_tdms.remove(
                tdms_match,
            )

        missing_in_mkys.extend(
            remaining_tdms,
        )

        return (
            matched,
            missing_in_tdms,
            missing_in_mkys,
        )

    def _mkys_openings(
        self,
        movements: list[Movement],
    ) -> list[Movement]:

        return [
            movement
            for movement in movements
            if str(
                movement.tif_no,
            ).strip() == "0"
        ]

    def _tdms_openings(
        self,
        movements: list[Movement],
    ) -> list[Movement]:

        return [
            movement
            for movement in movements
            if self.OPENING_DESCRIPTION
            in str(
                movement.description,
            ).upper()
        ]

    def _find_match(
        self,
        mkys: Movement,
        tdms_movements: list[Movement],
    ) -> Movement | None:

        for tdms in tdms_movements:

            if (
                tdms.amount == mkys.amount
                and tdms.movement_date.year == mkys.movement_date.year
            ):
                return tdms

        return None