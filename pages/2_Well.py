import streamlit as st
import pandas as pd
from datetime import date
from transform import read_data, transform_data

st.set_page_config(
    page_title="Dashboard Team PO PT PEP Bunyu Field",
    layout="wide",
    initial_sidebar_state="expanded"
)

try :
    st.title("Well Performance")

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

    tabelOilGas, tabelWip, tabelWell = transform_data(month, year)

    st.divider()

    col1,col2 = st.columns(2)
    with col1 :
        st.subheader("Oil Production")
        nilai = tabelWell.groupby("Date").agg({"Prod Act Oil" : "sum"}).reset_index()
        st.area_chart(x="Date", x_label="Tanggal",
                    y="Prod Act Oil", y_label="Production Oil (Bbl)",
                    data=nilai,
                    use_container_width=True)

    with col2 :
        st.subheader("Production Performance")
        nilai = tabelWell.groupby("Date").agg({"Prod Act Gross" : "sum", "Prod Act Oil" : "sum", "Gas Own (Mscfd)" : "sum", "Prod Act WC" : "sum"}).reset_index()
        st.line_chart(x="Date", x_label="Tanggal",
                    y=["Prod Act Gross"] + ["Prod Act Oil"] + ["Gas Own (Mscfd)"] + ["Prod Act WC"], y_label="Gross, Oil, Gas Own, WC",
                    data=nilai,
                    use_container_width=True)

    st.divider()

    col3, col4 = st.columns(2)
    with col3 :
        st.subheader("Parameter Operasi")
        nilai = tabelWell.groupby("Date").agg({"P.csg" : "sum", "P.tbg" : "sum", "P.fl" : "sum", "P.sep" : "sum"}).reset_index()
        st.line_chart(x="Date", x_label="Tanggal",
                    y=["P.csg"] + ["P.tbg"] + ["P.fl"] + ["P.sep"], y_label="P. Casing vs P. Tubing vs P. Flowline vs P. Separator",
                    data=nilai,
                    use_container_width=True)

    with col4 :
        st.subheader("Gross vs Gas Inj")
        nilai = tabelWell.groupby("Date").agg({"Prod Act Gross" : "sum", "Gas Inj (Mscfd)" : "sum"}).reset_index()
        st.line_chart(x="Date", x_label="Tanggal",
                    y=["Prod Act Gross"] + ["Gas Inj (Mscfd)"], y_label="Gross vs Gas Inj",
                    data=nilai,
                    use_container_width=True)
except KeyError as e :
    st.error("Data tidak tersedia pada Database.")