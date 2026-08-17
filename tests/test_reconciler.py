from datetime import date
from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.reconciler import Reconciler


def make_movement(
    *,
    tif_no: str | None = "TIF-001",
    movement_type: MovementType = MovementType.ENTRY,
    movement_date: date = date(2026, 1, 1),
    amount: str = "100.00",
    supplier: str = "Test Supplier",
    quantity: str = "1",
) -> Movement:
    """Testlerde kullanılacak kontrollü Movement nesnesi oluşturur."""
    return Movement(
        source="test",
        movement_type=movement_type,
        movement_date=movement_date,
        tif_no=tif_no,
        voucher_no=None,
        document_no=None,
        invoice_no=None,
        amount=Decimal(amount),
        description="test movement",
        warehouse="",
        budget_type="",
        stock_code="",
        stock_name="",
        supplier=supplier,
        quantity=Decimal(quantity),
    )


def test_entry_one_to_one_match():
    """Aynı TİF ve aynı tutar birebir eşleşmelidir."""

    mkys = [
        make_movement(
            tif_no="TIF-001",
            movement_type=MovementType.ENTRY,
            amount="100.00",
        )
    ]

    tdms = [
        make_movement(
            tif_no="TIF-001",
            movement_type=MovementType.ENTRY,
            amount="100.00",
        )
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert len(result.matched) == 1
    assert result.matched[0].tif_no == "TIF-001"

    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []


def test_entry_missing_in_tdms():
    """MKYS'deki giriş TDMS'de yoksa missing_in_tdms'e gitmelidir."""

    mkys = [
        make_movement(
            tif_no="TIF-001",
            movement_type=MovementType.ENTRY,
            amount="100.00",
        )
    ]

    tdms = []

    result = Reconciler().reconcile(mkys, tdms)

    assert result.matched == []

    assert len(result.missing_in_tdms) == 1
    assert result.missing_in_tdms[0].tif_no == "TIF-001"

    assert result.missing_in_mkys == []
    assert result.amount_differences == []


def test_entry_missing_in_mkys():
    """TDMS'deki giriş MKYS'de yoksa missing_in_mkys'e gitmelidir."""

    mkys = []

    tdms = [
        make_movement(
            tif_no="TIF-001",
            movement_type=MovementType.ENTRY,
            amount="100.00",
        )
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert result.matched == []
    assert result.missing_in_tdms == []

    assert len(result.missing_in_mkys) == 1
    assert result.missing_in_mkys[0].tif_no == "TIF-001"

    assert result.amount_differences == []


def test_entry_amount_difference():
    """Aynı TİF'in tutarı farklıysa amount_differences oluşmalıdır."""

    mkys = [
        make_movement(
            tif_no="TIF-001",
            movement_type=MovementType.ENTRY,
            amount="100.00",
        )
    ]

    tdms = [
        make_movement(
            tif_no="TIF-001",
            movement_type=MovementType.ENTRY,
            amount="120.00",
        )
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert result.matched == []
    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []

    assert len(result.amount_differences) == 1

    difference = result.amount_differences[0]

    assert difference.mkys.amount == Decimal("100.00")
    assert difference.tdms.amount == Decimal("120.00")


def test_consumption_monthly_many_to_one():
    """
    CONSUMPTION hareketleri aylık toplam üzerinden N:1 eşleşmelidir.

    MKYS:
        05.01 → 100 TL
        12.01 → 150 TL
        25.01 → 250 TL

    Ocak toplamı:
        500 TL

    TDMS:
        Ocak → 500 TL
    """

    mkys = [
        make_movement(
            tif_no="TIF-001",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 1, 5),
            amount="100.00",
        ),
        make_movement(
            tif_no="TIF-002",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 1, 12),
            amount="150.00",
        ),
        make_movement(
            tif_no="TIF-003",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 1, 25),
            amount="250.00",
        ),
    ]

    tdms = [
        make_movement(
            tif_no=None,
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 1, 31),
            amount="500.00",
        )
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert result.matched == []

    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []

    assert result.amount_differences == []
    assert result.consumption_differences == []

    assert len(result.consumption_matched) == 1

    match = result.consumption_matched[0]

    assert match.year == 2026
    assert match.month == 1
    assert match.mkys_amount == Decimal("500.00")
    assert match.tdms_amount == Decimal("500.00")


def test_consumption_monthly_amount_difference():
    """
    Aynı ayın MKYS ve TDMS tüketim toplamları farklıysa
    consumption_differences oluşmalıdır.
    """

    mkys = [
        make_movement(
            tif_no="TIF-001",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 1, 5),
            amount="100.00",
        ),
        make_movement(
            tif_no="TIF-002",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 1, 20),
            amount="150.00",
        ),
    ]

    tdms = [
        make_movement(
            tif_no=None,
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 1, 31),
            amount="200.00",
        )
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert result.matched == []
    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []

    assert result.consumption_matched == []

    assert len(result.consumption_differences) == 1

    difference = result.consumption_differences[0]

    assert difference.year == 2026
    assert difference.month == 1
    assert difference.mkys_amount == Decimal("250.00")
    assert difference.tdms_amount == Decimal("200.00")


def test_consumption_missing_in_tdms_month():
    """
    MKYS'de tüketim olduğu halde ilgili ayda TDMS kaydı yoksa
    ilgili ay consumption_differences olarak raporlanmalıdır.
    """

    mkys = [
        make_movement(
            tif_no="TIF-001",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 2, 5),
            amount="100.00",
        ),
        make_movement(
            tif_no="TIF-002",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 2, 15),
            amount="150.00",
        ),
    ]

    tdms = []

    result = Reconciler().reconcile(mkys, tdms)

    assert result.matched == []
    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []

    assert result.consumption_matched == []

    assert len(result.consumption_differences) == 1

    difference = result.consumption_differences[0]

    assert difference.year == 2026
    assert difference.month == 2
    assert difference.mkys_amount == Decimal("250.00")
    assert difference.tdms_amount == Decimal("0")


def test_consumption_missing_in_mkys_month():
    """
    TDMS'de tüketim olduğu halde ilgili ayda MKYS kaydı yoksa
    ilgili ay consumption_differences olarak raporlanmalıdır.
    """

    mkys = []

    tdms = [
        make_movement(
            tif_no=None,
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 3, 31),
            amount="350.00",
        )
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert result.matched == []
    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []

    assert result.consumption_matched == []

    assert len(result.consumption_differences) == 1

    difference = result.consumption_differences[0]

    assert difference.year == 2026
    assert difference.month == 3
    assert difference.mkys_amount == Decimal("0")
    assert difference.tdms_amount == Decimal("350.00")


def test_consumption_multiple_months_are_reconciled_independently():
    """
    Farklı aylar birbirinden bağımsız değerlendirilmelidir.

    Ocak:
        MKYS = 300
        TDMS = 300
        → matched

    Şubat:
        MKYS = 400
        TDMS = 350
        → difference

    Mart:
        MKYS = 500
        TDMS = 500
        → matched
    """

    mkys = [
        # Ocak
        make_movement(
            tif_no="TIF-001",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 1, 5),
            amount="100.00",
        ),
        make_movement(
            tif_no="TIF-002",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 1, 20),
            amount="200.00",
        ),
        # Şubat
        make_movement(
            tif_no="TIF-003",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 2, 10),
            amount="400.00",
        ),
        # Mart
        make_movement(
            tif_no="TIF-004",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 3, 15),
            amount="500.00",
        ),
    ]

    tdms = [
        # Ocak
        make_movement(
            tif_no=None,
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 1, 31),
            amount="300.00",
        ),
        # Şubat
        make_movement(
            tif_no=None,
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 2, 28),
            amount="350.00",
        ),
        # Mart
        make_movement(
            tif_no=None,
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 3, 31),
            amount="500.00",
        ),
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert result.matched == []
    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []

    assert len(result.consumption_matched) == 2
    assert len(result.consumption_differences) == 1

    matched_months = {(match.year, match.month) for match in result.consumption_matched}

    assert matched_months == {
        (2026, 1),
        (2026, 3),
    }

    difference = result.consumption_differences[0]

    assert difference.year == 2026
    assert difference.month == 2
    assert difference.mkys_amount == Decimal("400.00")
    assert difference.tdms_amount == Decimal("350.00")


def test_transfer_one_to_one_match():
    """TRANSFER hareketleri aynı TİF üzerinden birebir eşleşmelidir."""
    mkys = [
        make_movement(
            tif_no="TIF-TRANSFER-001",
            movement_type=MovementType.TRANSFER,
            movement_date=date(2026, 2, 5),
            amount="500.00",
        )
    ]

    tdms = [
        make_movement(
            tif_no="TIF-TRANSFER-001",
            movement_type=MovementType.TRANSFER,
            movement_date=date(2026, 2, 5),
            amount="500.00",
        )
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert len(result.matched) == 1
    assert result.matched[0] == mkys[0]

    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []


def test_scrap_one_to_one_match():
    """SCRAP hareketleri aynı TİF üzerinden birebir eşleşmelidir."""
    mkys = [
        make_movement(
            tif_no="TIF-SCRAP-001",
            movement_type=MovementType.SCRAP,
            movement_date=date(2026, 3, 5),
            amount="750.00",
        )
    ]

    tdms = [
        make_movement(
            tif_no="TIF-SCRAP-001",
            movement_type=MovementType.SCRAP,
            movement_date=date(2026, 3, 5),
            amount="750.00",
        )
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert len(result.matched) == 1
    assert result.matched[0] == mkys[0]

    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []


def test_count_surplus_one_to_one_match():
    """
    COUNT_SURPLUS hareketleri TİF numarası üzerinden
    birebir (ONE_TO_ONE) eşleşmelidir.
    """
    mkys = [
        make_movement(
            tif_no="TIF-COUNT-SURPLUS-001",
            movement_type=MovementType.COUNT_SURPLUS,
            movement_date=date(2026, 1, 31),
            amount="100.00",
        )
    ]

    tdms = [
        make_movement(
            tif_no="TIF-COUNT-SURPLUS-001",
            movement_type=MovementType.COUNT_SURPLUS,
            movement_date=date(2026, 1, 31),
            amount="100.00",
        )
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert len(result.matched) == 1
    assert result.matched[0].tif_no == "TIF-COUNT-SURPLUS-001"

    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []


def test_count_deficit_one_to_one_match():
    """
    COUNT_DEFICIT hareketleri TİF numarası üzerinden
    birebir (ONE_TO_ONE) eşleşmelidir.
    """
    mkys = [
        make_movement(
            tif_no="TIF-COUNT-DEFICIT-001",
            movement_type=MovementType.COUNT_DEFICIT,
            movement_date=date(2026, 1, 31),
            amount="150.00",
        )
    ]

    tdms = [
        make_movement(
            tif_no="TIF-COUNT-DEFICIT-001",
            movement_type=MovementType.COUNT_DEFICIT,
            movement_date=date(2026, 1, 31),
            amount="150.00",
        )
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert len(result.matched) == 1
    assert result.matched[0].tif_no == "TIF-COUNT-DEFICIT-001"

    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []


def test_same_tif_with_different_movement_type_does_not_match():
    """
    Aynı TİF numarası farklı MovementType'a aitse eşleşmemelidir.

    Örneğin:
        MKYS   -> ENTRY / TIF-001
        TDMS   -> TRANSFER / TIF-001

    Bunlar aynı reconciliation grubu içinde değildir.
    """
    mkys = [
        make_movement(
            tif_no="TIF-SAME-001",
            movement_type=MovementType.ENTRY,
            movement_date=date(2026, 5, 5),
            amount="100.00",
        )
    ]

    tdms = [
        make_movement(
            tif_no="TIF-SAME-001",
            movement_type=MovementType.TRANSFER,
            movement_date=date(2026, 5, 5),
            amount="100.00",
        )
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert result.matched == []
    assert result.amount_differences == []

    assert len(result.missing_in_tdms) == 1
    assert result.missing_in_tdms[0] == mkys[0]

    assert len(result.missing_in_mkys) == 1
    assert result.missing_in_mkys[0] == tdms[0]


def test_entry_with_none_tif_is_not_reconciled():
    """
    TİF numarası olmayan ONE_TO_ONE kaydı mevcut stratejide
    reconciliation dışında bırakılmalıdır.

    Çünkü TIF reconciliation key'i oluşturulamaz.
    """
    mkys = [
        make_movement(
            tif_no=None,
            movement_type=MovementType.ENTRY,
            movement_date=date(2026, 6, 5),
            amount="100.00",
        )
    ]

    tdms = [
        make_movement(
            tif_no=None,
            movement_type=MovementType.ENTRY,
            movement_date=date(2026, 6, 5),
            amount="100.00",
        )
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert result.matched == []
    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []


def test_donation_one_to_one_match():
    """
    DONATION hareketleri TİF üzerinden birebir eşleşmelidir.
    """
    mkys = [
        make_movement(
            tif_no="DON-001",
            movement_type=MovementType.DONATION,
            movement_date=date(2026, 2, 10),
            amount="1500.00",
        )
    ]

    tdms = [
        make_movement(
            tif_no="DON-001",
            movement_type=MovementType.DONATION,
            movement_date=date(2026, 2, 10),
            amount="1500.00",
        )
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert result.matched == [mkys[0]]
    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []


def test_other_movement_type_is_not_reconciled():
    """
    OTHER hareket türü için reconciliation kuralı olmadığı için
    Reconciler bu kayıtları mevcut sonuç alanlarına taşımamalıdır.
    """
    mkys = [
        make_movement(
            tif_no="OTHER-001",
            movement_type=MovementType.OTHER,
            movement_date=date(2026, 6, 15),
            amount="100.00",
        )
    ]

    tdms = [
        make_movement(
            tif_no="OTHER-001",
            movement_type=MovementType.OTHER,
            movement_date=date(2026, 6, 15),
            amount="100.00",
        )
    ]

    result = Reconciler().reconcile(mkys, tdms)

    assert result.matched == []
    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []
    assert result.consumption_matched == []
    assert result.consumption_differences == []


def test_duplicate_tif_in_mkys_uses_last_record():
    """
    Aynı TİF MKYS'de iki kez bulunduğunda mevcut ONE_TO_ONE
    implementasyonunda son kayıt dictionary'de kalır.
    """
    first = make_movement(
        tif_no="TIF-DUP-001",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 1, 10),
        amount="100.00",
    )

    second = make_movement(
        tif_no="TIF-DUP-001",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 1, 11),
        amount="200.00",
    )

    tdms = [
        make_movement(
            tif_no="TIF-DUP-001",
            movement_type=MovementType.ENTRY,
            movement_date=date(2026, 1, 11),
            amount="200.00",
        )
    ]

    result = Reconciler().reconcile(
        [first, second],
        tdms,
    )

    assert result.matched == [second]
    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []


def test_duplicate_tif_in_tdms_uses_last_record():
    """
    Aynı TİF TDMS'de iki kez bulunduğunda mevcut ONE_TO_ONE
    implementasyonunda son kayıt dictionary'de kalır.
    """
    mkys = [
        make_movement(
            tif_no="TIF-DUP-002",
            movement_type=MovementType.ENTRY,
            movement_date=date(2026, 2, 10),
            amount="300.00",
        )
    ]

    first = make_movement(
        tif_no="TIF-DUP-002",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 2, 10),
        amount="100.00",
    )

    second = make_movement(
        tif_no="TIF-DUP-002",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 2, 11),
        amount="300.00",
    )

    result = Reconciler().reconcile(
        mkys,
        [first, second],
    )

    assert result.matched == [mkys[0]]
    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []


def test_one_to_one_movement_with_none_tif_is_ignored():
    """
    TIF numarası olmayan ONE_TO_ONE hareketi mevcut implementasyonda
    reconciliation dışında kalır.
    """
    mkys = [
        make_movement(
            tif_no=None,
            movement_type=MovementType.ENTRY,
            movement_date=date(2026, 3, 5),
            amount="100.00",
        )
    ]

    tdms = []

    result = Reconciler().reconcile(
        mkys,
        tdms,
    )

    assert result.matched == []
    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []


def test_tdms_one_to_one_movement_with_none_tif_is_ignored():
    """
    TDMS tarafında TIF numarası olmayan ONE_TO_ONE hareketi
    mevcut implementasyonda reconciliation dışında kalır.
    """
    mkys = []

    tdms = [
        make_movement(
            tif_no=None,
            movement_type=MovementType.ENTRY,
            movement_date=date(2026, 3, 5),
            amount="100.00",
        )
    ]

    result = Reconciler().reconcile(
        mkys,
        tdms,
    )

    assert result.matched == []
    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []


def test_consumption_same_month_multiple_tdms_records_are_summed():
    """
    Aynı ayda birden fazla TDMS tüketim kaydı varsa,
    kayıtlar aylık toplam üzerinden birlikte değerlendirilmelidir.
    """
    mkys = [
        make_movement(
            tif_no="TIF-C-001",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 4, 5),
            amount="100.00",
        ),
        make_movement(
            tif_no="TIF-C-002",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 4, 12),
            amount="150.00",
        ),
        make_movement(
            tif_no="TIF-C-003",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 4, 25),
            amount="250.00",
        ),
    ]

    tdms = [
        make_movement(
            tif_no=None,
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 4, 15),
            amount="200.00",
        ),
        make_movement(
            tif_no=None,
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 4, 30),
            amount="300.00",
        ),
    ]

    result = Reconciler().reconcile(
        mkys,
        tdms,
    )

    assert result.matched == []
    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []
    assert result.consumption_differences == []

    assert len(result.consumption_matched) == 1

    match = result.consumption_matched[0]

    assert match.year == 2026
    assert match.month == 4
    assert match.mkys_amount == Decimal("500.00")
    assert match.tdms_amount == Decimal("500.00")
