import streamlit as st
import pandas as pd
from transform import read_data, transform_data
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


    st.title("📊 Tabel Data Production Operations PT Pertamina EP Asset 5 Bunyu Field")
    st.divider()

    tabelOilGas, tabelWip, tabelWell = transform_data(month, year)
    if year != "Semua":
        if month != "Semua":
            st.subheader(f"Tabel Data Production {month} {year}")
            st.dataframe(tabelOilGas, hide_index=True)
        else :
            st.subheader(f"Tabel Data Production Tahun {year}")
            st.dataframe(tabelOilGas, hide_index=True)
    else :
        if month != "Semua":
            st.subheader(f"Tabel Data Production Setiap Bulan {month}")
            st.dataframe(tabelOilGas, hide_index=True)
        else :
            st.subheader(f"Tabel Data Production")
            st.dataframe(tabelOilGas, hide_index=True)

    st.divider()

    if year != "Semua":
        if month != "Semua":
            st.subheader(f"Tabel Data WIP {month} {year}")
            st.dataframe(tabelWip, hide_index=True)
        else :
            st.subheader(f"Tabel Data WIP Tahun {year}")
            st.dataframe(tabelWip, hide_index=True)
    else :
        if month != "Semua":
            st.subheader(f"Tabel Data WIP Setiap Bulan {month}")
            st.dataframe(tabelWip, hide_index=True)
        else :
            st.subheader(f"Tabel Data WIP")
            st.dataframe(tabelWip, hide_index=True)

    st.divider()

    if year != "Semua":
        if month != "Semua":
            st.subheader(f"Tabel Data Well {month} {year}")
            st.dataframe(tabelWell, hide_index=True)
        else :
            st.subheader(f"Tabel Data Well Tahun {year}")
            st.dataframe(tabelWell, hide_index=True)
    else :
        if month != "Semua":
            st.subheader(f"Tabel Data Well Setiap Bulan {month}")
            st.dataframe(tabelWell, hide_index=True)
        else :
            st.subheader(f"Tabel Data Well")
            st.dataframe(tabelWell, hide_index=True)
except ImportError as e :
    st.error("Data tidak tersedia pada Database.")