"""
MKYS CSV sütun adları.

Bu modül, MKYS giriş dosyasında kullanılan sütun isimlerini tek
merkezden yönetir.
"""

from __future__ import annotations

# ---------------------------------------------------------
# Temel belge bilgileri
# ---------------------------------------------------------

ROW_NO = "Sıra No"
DETAIL_ROW_NO = "Detay Sıra No"

TIF_NO = "TİF No"
DATE = "Tarih"

# ---------------------------------------------------------
# Depo / Bütçe
# ---------------------------------------------------------

WAREHOUSE = "Depo Tanımı"
BUDGET = "Bütçe"

# ---------------------------------------------------------
# Tedarik bilgileri
# ---------------------------------------------------------

SUPPLY_TYPE = "Tedarik Türü"
PURCHASE_METHOD = "Alım Yöntemi"

SUPPLIER = "Tedarikçi"
SUPPLIER_VKN = "Tedarikçi VKN"

# ---------------------------------------------------------
# Fatura bilgileri
# ---------------------------------------------------------

INVOICE_NO = "Fatura No"
INVOICE_DATE = "Fatura Tarihi"

# ---------------------------------------------------------
# Teslim bilgileri
# ---------------------------------------------------------

DELIVERED_BY = "Teslim Eden"
RECEIVED_BY = "Teslim Alan"

# ---------------------------------------------------------
# Toplamlar
# ---------------------------------------------------------

TOTAL_QUANTITY = "Toplam Miktar"

TOTAL_EXCL_VAT = "KDV Hariç Toplam Tutar"
TOTAL_AMOUNT = "Toplam Tutar"

TDMS_RECEIPT_NO = "TDMS/YBS Fiş No"
TDMS_AMOUNT = "TDMS Fiş Tutarı"

# ---------------------------------------------------------
# Malzeme bilgileri
# ---------------------------------------------------------

ITEM_CODE = "Taşınır Kodu"
ITEM_NAME = "Malzeme Tanımı"
ITEM_DESCRIPTION = "Malzeme Açıklama"

BARCODE = "Barkod"

QUANTITY = "Miktar"

# ---------------------------------------------------------
# Fiyat bilgileri
# ---------------------------------------------------------

UNIT_PRICE_EXCL_VAT = "Vergisiz Birim Fiyat"
LINE_TOTAL_EXCL_VAT = "Vergisiz Toplam"

VAT_RATE = "KDV Oranı"
TRANSFER_RATE = "Devir Oranı"
DISCOUNT_RATE = "İndirim Oranı"

UNIT_PRICE = "Birim Fiyat"
LINE_TOTAL = "Vergili Toplam"

# ---------------------------------------------------------
# Parser için zorunlu sütunlar
# ---------------------------------------------------------

REQUIRED_COLUMNS = [
    DATE,
    TIF_NO,
    TOTAL_AMOUNT,
    ITEM_CODE,
    ITEM_NAME,
    QUANTITY,
    WAREHOUSE,
    BUDGET,
]