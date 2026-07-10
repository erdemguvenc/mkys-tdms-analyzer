from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional
from analyzer.models.movement_type import MovementType

@dataclass(slots=True)
class Movement:
    """
    Ortak hareket modeli.

    MKYS ve TDMS kayıtları önce bu modele dönüştürülür.
    Böylece uzlaştırma motoru veri kaynağını bilmek zorunda kalmaz.
    """

    # Veri kaynağı
    source: str

    # ENTRY / CONSUMPTION / TRANSFER / SCRAP / COUNT vb.
    movement_type: MovementType

    # Hareket tarihi
    movement_date: date

    # TİF Bilgileri
    tif_no: Optional[str] = None

    # TDMS fiş numarası
    voucher_no: Optional[str] = None

    # Belge numarası
    document_no: Optional[str] = None

    # Fatura numarası
    invoice_no: Optional[str] = None

    # Muhasebe tutarı (KDV Dahil)
    amount: Decimal = Decimal("0.00")

    # Açıklama
    description: str = ""

    # Depo
    warehouse: str = ""

    # Bütçe Türü
    budget_type: str = ""

    # Taşınır Kodu
    stock_code: str = ""

    # Malzeme Adı
    stock_name: str = ""