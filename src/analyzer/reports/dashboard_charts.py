from __future__ import annotations

from openpyxl.chart import PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.series import DataPoint
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.worksheet.worksheet import Worksheet

from analyzer.reports.dashboard_summary import DashboardSummary

from openpyxl.chart import (
    BarChart,
    PieChart,
    Reference,
)


class DashboardCharts:
    """
    Dashboard grafiklerini oluşturan yardımcı sınıf.
    """

    @staticmethod
    def add_match_pie_chart(
        worksheet: Worksheet,
        summary: DashboardSummary,
    ) -> None:
        """
        Eşleşme durumunu gösteren pasta grafiği ekler.
        """

        #
        # Grafik veri alanı
        #
        worksheet["N1"] = "Durum"
        worksheet["O1"] = "Adet"

        worksheet["N2"] = "Eşleşen"
        worksheet["O2"] = summary.matched_records

        worksheet["N3"] = "MKYS Eksik"
        worksheet["O3"] = summary.missing_in_mkys

        worksheet["N4"] = "TDMS Eksik"
        worksheet["O4"] = summary.missing_in_tdms

        labels = Reference(
            worksheet,
            min_col=14,
            min_row=2,
            max_row=4,
        )

        data = Reference(
            worksheet,
            min_col=15,
            min_row=1,
            max_row=4,
        )

        chart = PieChart()

        chart.title = "Giriş Hareketleri"

        chart.height = 8

        chart.width = 10

        chart.add_data(
            data,
            titles_from_data=True,
        )

        chart.set_categories(
            labels,
        )

        chart.legend.position = "r"

        chart.firstSliceAng = 45

        #
        # Dilimleri renklendirmeye hazır hale getir
        #
        for i in range(3):

            point = DataPoint(idx=i)

            chart.series[0].data_points.append(
                point,
            )

        worksheet.add_chart(
            chart,
            "H3",
        )


    @staticmethod
    def add_consumption_bar_chart(
        worksheet: Worksheet,
        summary: DashboardSummary,
    ) -> None:
        """
        Tüketim ve tutar farklarını gösteren sütun grafiği ekler.
        """

        worksheet["N7"] = "Kategori"
        worksheet["O7"] = "Adet"

        worksheet["N8"] = "Tutar Farkı"
        worksheet["O8"] = summary.amount_difference_count

        worksheet["N9"] = "Tüketim Farkı"
        worksheet["O9"] = summary.consumption_difference_count

        labels = Reference(
            worksheet,
            min_col=14,
            min_row=8,
            max_row=9,
        )

        data = Reference(
            worksheet,
            min_col=15,
            min_row=7,
            max_row=9,
        )

        chart = BarChart()

        chart.type = "col"
        chart.style = 10

        chart.title = "MKYS - TDMS Fark Analizi"
        chart.y_axis.title = "Kayıt"
        chart.x_axis.title = "Kategori"

        chart.height = 8
        chart.width = 10

        chart.add_data(
            data,
            titles_from_data=True,
        )

        chart.set_categories(
            labels,
        )

        # Kurumsal mavi renk
        chart.series[0].graphicalProperties = GraphicalProperties(
            solidFill="4472C4",
        )

        # Veri etiketleri
        chart.dataLabels = DataLabelList()
        chart.dataLabels.showVal = True

        # Grid çizgilerini kaldır
        chart.y_axis.majorGridlines = None

        worksheet.add_chart(
            chart,
            "H20",
        )