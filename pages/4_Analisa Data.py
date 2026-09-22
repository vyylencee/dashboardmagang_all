import streamlit as st
from transform import read_data, transform_data
import pandas as pd
from datetime import date

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

    opsi = ["Semua"] + listYear
    year = st.sidebar.selectbox("Pilih Tahun", options=opsi, key="year")

    month = st.sidebar.selectbox("Pilih Bulan", 
                                ["Semua", "Januari", "Februari",
                                "Maret", "April", "Mei",
                                "Juni", "Juli", "Agustus",
                                "September", "Oktober",
                                "November", "Desember"], key="month")

    tabelOilGas, tabelWip, tabelWell = transform_data("Semua","Semua")

    listYear = tabelOilGas["DATE"].dt.year.astype(str).unique().tolist()

    list_bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

    bulan_map = {
        1 : "Januari",
        2 : "Februari",
        3 : "Maret",
        4 : "April",
        5 : "Mei",
        6 : "Juni",
        7 : "Juli",
        8 : "Agustus",
        9 : "September",
        10 : "Oktober",
        11 : "November",
        12 : "Desember"
    }

    st.title("Analisa Data")
    st.divider()

    col1, col2 = st.columns(2)
    with col1 :
        st.subheader("Hasil Produksi Minyak")
        oil = tabelOilGas.groupby(tabelOilGas["DATE"].dt.year, observed=True)["PROD OIL (SOT)"].sum()
        bulananTertinggiOil = oil.idxmax()
        produksiTertinggiOil = oil.max()
        st.bar_chart(oil)     

    with col2 :
        st.subheader("Hasil Produksi Gas")
        gas = tabelOilGas.groupby(tabelOilGas["DATE"].dt.year, observed=True)["PROD GAS (MSCFD)"].sum()
        bulananTertinggiGas = gas.idxmax()
        produksiTertinggiGas = gas.max()
        st.bar_chart(gas)

    col3, col4 = st.columns(2)

    with col3 :
        st.subheader("Target Produksi vs Pencapaian Produksi Minyak")
        st.line_chart(x="DATE", x_label="Tanggal", 
                    y=["PROD OIL (SOT)"] + ["TARGET PRODUKSI OIL (RKAP)"] + ["TARGET PRODUKSI OIL (WP&B)"], y_label="Produksi Minyak (Bbl)",                    
                    data=tabelOilGas,
                    width="stretch")

    with col4 :
        st.subheader("Target Produksi vs Pencapaian Produksi Gas")
        st.line_chart(x="DATE", x_label="Tanggal",
                    y=["PROD GAS (MSCFD)"] + ["TARGET RKAP GAS"] + ["TARGET WP&B GAS"], y_label="Produksi Gas (MSCFD)",
                    data=tabelOilGas,
                    width="stretch")

    st.divider()

    # st.subheader("Total Gas Sales Performance Tertinggi PEP Bunyu")

    # tabelOilGas["Tahun"] = tabelOilGas["DATE"].dt.year
    # tabelOilGas["Tahun"] = pd.Categorical(tabelOilGas["Tahun"], categories=listYear, ordered=True)

    # plnbny = tabelOilGas.groupby("Tahun")["SALES PLN Bunyu"].sum()
    # gasbny = tabelOilGas.groupby("Tahun")["SALES City Gas Bunyu"].sum()
    # gastrk = tabelOilGas.groupby("Tahun")["SALES City Gas Tarakan"].sum()
    # g8trk = tabelOilGas.groupby("Tahun")["G-8"].sum()
    # bintrk = tabelOilGas.groupby("Tahun")["Binalatung"].sum()
    # kmpg1trk = tabelOilGas.groupby("Tahun")["Kampung 1"].sum()

    # bulanplnbny = plnbny.idxmax()
    # bulangasbny = gasbny.idxmax()
    # bulangastrk = gastrk.idxmax()
    # bulang8trk = g8trk.idxmax()
    # bulanbintrk = bintrk.idxmax()
    # bulankmpg1trk = kmpg1trk.idxmax()

    # totalplnbny = plnbny.max()
    # totalgasbny = gasbny.max()
    # totalgastrk = gastrk.max()
    # totalg8trk = g8trk.max()
    # totalbintrk = bintrk.max()
    # totalkmpg1trk = kmpg1trk.max()

    # penjualan = pd.DataFrame({"PLN BUNYU (MMSCF)" : [bulanplnbny, totalplnbny],
    #                    "CITY GAS BUNYU (MMSCF)" : [bulangasbny, totalgasbny],
    #                    "CITY GAS TARAKAN (MMSCF)" : [bulangastrk, totalgastrk],
    #                    "G-8 TARAKAN (MMSCF)" : [bulang8trk, totalg8trk],
    #                    "BINALATUNG - TRK (MMSCF)" : [bulanbintrk, totalbintrk],
    #                    "KAMPUNG 1 (MMSCF)" : [bulankmpg1trk, totalkmpg1trk]},
    #                    index = ["Bulan", "Total"])

    # st.dataframe(penjualan)

    st.subheader("Sumur dengan Produksi Tertinggi")
    col1, col2, col3 = st.columns(3)
    nilaiOil = tabelWell.groupby("Well").agg({"Prod Act Oil" : "sum", "GS" : "first"}).reset_index().sort_values("Prod Act Oil", ascending=False)
    nilaiGas = tabelWell.groupby("Well").agg({"Gas Own (Mscfd)" : "sum", "GS" : "first"}).reset_index().sort_values("Gas Own (Mscfd)", ascending=False)
    nilaiKA = tabelWell.groupby("Well").agg({"Prod Act WC" : "sum", "GS" : "first"}).reset_index().sort_values("Prod Act WC", ascending=False)

    with col1 :
        st.subheader("Produksi Minyak")
        st.dataframe(nilaiOil.style.format({"Prod Act Oil" : "{:,.0f}"}), hide_index=True)

    with col2 :
        st.subheader("Gas Own")
        st.dataframe(nilaiGas.style.format({"Gas Own (Mscfd)" : "{:,.2f}"}), hide_index=True)

    with col3 :
        st.subheader("Produksi Kadar Air")
        st.dataframe(nilaiKA.style.format({"Prod Act WC" : "{:,.2f}"}), hide_index=True)
except KeyError as e :
    st.error("Data tidak tersedia pada Database.")