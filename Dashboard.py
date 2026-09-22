import streamlit as st
from transform import read_data, transform_data
import pandas as pd
from datetime import date, timedelta
from io import BytesIO

st.set_page_config(
    page_title="Dashboard Team PO PT PEP Bunyu Field",
    layout="wide",
    initial_sidebar_state="expanded"
)

try :
    tabelOilGas, tabelWip, tabelWell = read_data()

    tabelOilGas["DATE"] = pd.to_datetime(tabelOilGas["DATE"])
    minDate = tabelOilGas["DATE"].min()
    maxDate = tabelOilGas["DATE"].max()
    thisMonth = date.today().month

    listYear = tabelOilGas["DATE"].dt.year.astype(str).unique().tolist()

    st.title("Dashboard Production Operations PT Pertamina EP Asset 5 Bunyu Field")
    st.subheader(f"Periode tahun {tabelOilGas['DATE'].min().year} - {tabelOilGas['DATE'].max().year}")


    opsi = ["Semua"] + listYear
    year = st.sidebar.selectbox("Pilih Tahun", options=opsi, key="year")

    month = st.sidebar.selectbox("Pilih Bulan", 
                                ["Semua", "Januari", "Februari",
                                "Maret", "April", "Mei",
                                "Juni", "Juli", "Agustus",
                                "September", "Oktober",
                                "November", "Desember"], key="month")
        

    st.session_state["bulan"] = month
    st.session_state["tahun"] = year
    tabelOilGas, tabelWip, tabelWell = transform_data(month, year)

    hariIni = date.today()
    h_1 = hariIni - timedelta(days=1)
    bulanIni = date.today().month

    data_bulanIni = tabelOilGas["DATE"].dt.month == bulanIni

    st.divider()

    st.subheader("📊 Oil & Gas Production")

    col1, col2 = st.columns(2)


    # GRAFIK & CARDS OIL PRODUCTION #

    with col1:
        st.subheader("Oil Production")
        card1, card2, card3, card4 = st.columns(4)

        with card1 :
            try :
                nilai = tabelOilGas["PROD OIL (SOT)"].sum()
                st.metric(label=f"Total Produksi Minyak"
                        ,value=f"{nilai:,.0f}"
                        ,border=True)
            except IndexError :
                st.metric(label=f"Total Produksi Minyak"
                        ,value="-"
                        ,border=True)

        with card2 :
            nilai = tabelOilGas[tabelOilGas["DATE"].dt.date == h_1]["PROD OIL (SOT)"].sum()
            st.metric(label=f"Produksi Hari Ini"
                        ,value=f"{nilai:,.0f}"
                        ,border=True)
            
        with card3 :
            nilai = tabelOilGas["TARGET PRODUKSI OIL (RKAP)"].iloc[0]
            if month != "Semua" :
                st.metric(label="Target RKAP"
                        ,value=f"{nilai:,.0f}"
                        ,border=True)
            else :
                st.metric(label="Target RKAP"
                        ,value="-"
                        ,border=True)

        with card4 :
            nilai = tabelOilGas["TARGET PRODUKSI OIL (WP&B)"].iloc[0]
            if len(tabelOilGas["TARGET PRODUKSI OIL (WP&B)"]) > 0 and month != "Semua":
                st.metric(label="Target WP&B"
                        ,value=f"{nilai:,.0f}"
                        ,border=True)
            else :
                st.metric(label="Target WP&B"
                        ,value="-"
                        ,help="Data pada bulan ini belum tersedia."
                        ,border=True)


        
        if month != "Semua":
            st.line_chart(x="DATE", x_label="Tanggal", 
                        y="PROD OIL (SOT)", y_label="Produksi Minyak (Bbl)",                    
                        data=tabelOilGas,
                        width="stretch")
        else :
            st.line_chart(x="DATE", x_label="Bulan", 
                        y="PROD OIL (SOT)", y_label="Produksi Minyak (Bbl)",
                        data=tabelOilGas,
                        width="stretch")


    # GRAFIK & CARDS GAS PRODUCTION #
    with col2:
        st.subheader("Gas Production")
        card1, card2, card3, card4 = st.columns(4)
        
        with card1 :
            nilai = (tabelOilGas["PROD GAS (MSCFD)"].sum())/1000
            if len(tabelOilGas["PROD GAS (MSCFD)"]) > 0 :
                st.metric(label=f"Total Produksi Gas"
                            ,value=f"{nilai:,.4f}"
                            ,border=True)
            else :
                st.metric(label=f"Total Produksi Gas"
                            ,value=0
                            ,border=True)

        with card2 :
            nilai = tabelOilGas[tabelOilGas["DATE"].dt.date == h_1]["PROD GAS (MSCFD)"].sum()
            st.metric(label=f"Produksi Hari Ini"
                        ,value=f"{nilai:,.0f}"
                        ,border=True)

        with card3 :
            nilai = tabelOilGas["TARGET RKAP GAS"].iloc[0]
            if len(tabelOilGas["TARGET RKAP GAS"]) > 0 and month != "Semua" :
                st.metric(label="Target RKAP"
                        ,value=f"{nilai:,.0f}"
                        ,border=True)
            else :
                st.metric(label="Target RKAP"
                        ,value="-"
                        ,help="Data pada bulan ini belum tersedia."
                        ,border=True)

        with card4 :
            nilai = tabelOilGas["TARGET WP&B GAS"].iloc[0]
            if len(tabelOilGas["TARGET WP&B GAS"]) > 0 and month != "Semua" :
                st.metric(label="Target WP&B"
                        ,value=f"{nilai:,.0f}"
                        ,border=True)
            else :
                st.metric(label="Target WP&B"
                        ,value="-"
                        ,help="Data pada bulan ini belum tersedia."
                        ,border=True)
        
        if month != "Semua":
            chart = tabelOilGas[["DATE", "PROD GAS (MSCFD)"]].copy()
            chart["PROD GAS (MSCFD)"] = chart["PROD GAS (MSCFD)"] / 1000

            st.line_chart(x="DATE", x_label="Tanggal",
                        y="PROD GAS (MSCFD)", y_label="Produksi Gas (MMSCFD)",
                        data=chart,
                        width="stretch")
        else :
            chart = tabelOilGas[["DATE", "PROD GAS (MSCFD)"]].copy()
            chart["PROD GAS (MSCFD)"] = chart["PROD GAS (MSCFD)"] / 1000

            st.line_chart(x="DATE", x_label="Bulan",
                        y="PROD GAS (MSCFD)", y_label="Produksi Gas (MMSCFD)",
                        data=chart,
                        width="stretch")

    st.divider()
    st.subheader("💧 Water Injection")

    graph1, graph2 = st.columns(2)

    with graph1 :
        st.write("Water Injection vs Water Production")
        st.line_chart(x="DATE", x_label="Tanggal",
                    y=["PROD WATER"] + ["INJECTION WATER"],y_label="Injection Water vs Production Water",
                    data=tabelOilGas,
                    width="stretch")

    with graph2 :
        st.write("Injection Well")
        wipDaily = tabelWip.groupby("DATE").agg({"Flowrate (BWPD)" : "sum", "Tekanan (PSI)" : "sum"}).reset_index()
        st.line_chart(x="DATE", x_label="Tanggal",
                    y=["Flowrate (BWPD)"] + ["Tekanan (PSI)"], y_label="Flowrate (BWPD)",
                    data=wipDaily,
                    width="stretch")

    st.divider()

    table, graph = st.columns(2)

    with table :
        st.subheader("Keterangan Low/Gain/Off")
        hariIni = date.today()
        h_1 = hariIni - timedelta(days=1)
        tanggal = tabelOilGas["DATE"].dt.date == h_1
        st.dataframe(tabelOilGas.loc[tanggal, ["DATE", "KETERANGAN LOW/GAIN/OFF"]], hide_index=True)

    with graph :
        st.subheader("💹 Gas Sales Field Bunyu")

        nilai = tabelOilGas[["DATE", "TOTAL SALES"]].copy()
        nilai["TOTAL SALES"] = nilai["TOTAL SALES"] / 1000
        
        st.area_chart(x="DATE", x_label="Tanggal",
                    y="TOTAL SALES", y_label="Total Sales (MMSCF)",
                    data=nilai,
                    color="#65cf75",
                    width="stretch")

    col1, col2 = st.columns([14,1])
    with col2:
        if st.button("More Details") :
            st.switch_page("pages/3_Sales Performance.py")
except KeyError as e :
    st.error("Data tidak tersedia pada Database.")