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

    st.title("💹 Gas Sales Performance")

    col1,col2 = st.columns(2)

    with col1 :
        locbny = st.selectbox("Pilih Lokasi", ["Semua", "Jargas Bunyu", "PLN Bunyu"], key="locBNY")

        st.subheader("Gas Sales to Bunyu")
        data = tabelOilGas[["DATE", "SALES City Gas Bunyu", "SALES PLN Bunyu"]].copy()
        data["SALES City Gas Bunyu"] = data["SALES City Gas Bunyu"] / 1000
        data["SALES PLN Bunyu"] = data["SALES PLN Bunyu"] / 1000

        if month != "Semua":
            if locbny == "Jargas Bunyu":
                st.area_chart(x="DATE", x_label="Tanggal",
                            y=["SALES City Gas Bunyu"], y_label="Total Sales (MMSCFD)",
                            data=data,
                            color="#FBFF90",
                            use_container_width=True)
            elif locbny == "PLN Bunyu":
                st.area_chart(x="DATE", x_label="Tanggal",
                            y=["SALES PLN Bunyu"], y_label="Total Sales (MMSCFD)",
                            data=data,
                            color="#4273AF",
                            use_container_width=True)
            else :
                st.area_chart(x="DATE", x_label="Tanggal",
                            y=["SALES PLN Bunyu"] + ["SALES City Gas Bunyu"], y_label="Total Sales (MMSCFD)",
                            data=data,
                            color=["#4273AF", "#FBFF90"],
                            use_container_width=True)
        else :
            if locbny == "Jargas Bunyu":
                st.area_chart(x="DATE", x_label="Bulan",
                            y=["SALES City Gas Bunyu"], y_label="Total Sales (MMSCFD)",
                            data=data,
                            color="#FBFF90",
                            use_container_width=True)
            elif locbny == "PLN Bunyu":
                st.area_chart(x="DATE", x_label="Bulan",
                            y=["SALES PLN Bunyu"], y_label="Total Sales (MMSCFD)",
                            data=data,
                            color="#4273AF",
                            use_container_width=True)
            else :
                st.area_chart(x="DATE", x_label="Bulan",
                            y=["SALES PLN Bunyu"] + ["SALES City Gas Bunyu"], y_label="Total Sales (MMSCFD)",
                            data=data,
                            color=["#4273AF", "#FBFF90"],
                            use_container_width=True)
    with col2 :
        loctrk = st.selectbox("Pilih Lokasi", ["Semua", "G-8", "Binalatung", "Kampung 1", "Jargas Tarakan"], key="locTRK")

        st.subheader("Gas Sales to Tarakan")
        if month != "Semua":
            if loctrk == "G-8":
                st.area_chart(x="DATE", x_label="Tanggal",
                            y=["G-8"], y_label="Total Sales (MMSCFD)",
                            data=tabelOilGas,
                            color="#FFD758",
                            use_container_width=True)
            elif loctrk == "Binalatung":
                st.area_chart(x="DATE", x_label="Tanggal",
                            y=["City Gas Tarakan"], y_label="Total Sales (MMSCFD)",
                            data=tabelOilGas,
                            color="#FCE59A",
                            use_container_width=True)
            elif loctrk == "Kampung 1":
                st.area_chart(x="DATE", x_label="Tanggal",
                            y=["Kampung 1"], y_label="Total Sales (MMSCFD)",
                            data=tabelOilGas,
                            color="#195B6F",
                            use_container_width=True)
            elif loctrk == "Jargas Tarakan":
                st.area_chart(x="DATE", x_label="Tanggal",
                            y=["Binalatung"], y_label="Total Sales (MMSCFD)",
                            data=tabelOilGas,
                            color="#90E5FF",
                            use_container_width=True)
            else :
                st.area_chart(x="DATE", x_label="Tanggal",
                            y=["Kampung 1"] + ["Binalatung"] + ["G-8"] + ["City Gas Tarakan"], y_label="Total Sales (MMSCFD)",
                            data=tabelOilGas,
                            color=["#195B6F","#90E5FF", "#FFD758", "#FCE59A"],
                            use_container_width=True)
        else :
            if loctrk == "G-8":
                st.area_chart(x="DATE", x_label="Bulan",
                            y=["G-8"], y_label="Total Sales (MMSCFD)",
                            data=tabelOilGas,
                            color="#FFD758",
                            use_container_width=True)
            elif loctrk == "Binalatung":
                st.area_chart(x="DATE", x_label="Bulan",
                            y=["City Gas Tarakan"], y_label="Total Sales (MMSCFD)",
                            data=tabelOilGas,
                            color="#FCE59A",
                            use_container_width=True)
            elif loctrk == "Kampung 1":
                st.area_chart(x="DATE", x_label="Bulan",
                            y=["Kampung 1"], y_label="Total Sales (MMSCFD)",
                            data=tabelOilGas,
                            color="#195B6F",
                            use_container_width=True)
            elif loctrk == "Jargas Tarakan":
                st.area_chart(x="DATE", x_label="Bulan",
                            y=["Binalatung"], y_label="Total Sales (MMSCFD)",
                            data=tabelOilGas,
                            color="#90E5FF",
                            use_container_width=True)
            else :
                st.area_chart(x="DATE", x_label="Bulan",
                            y=["Kampung 1"] + ["Binalatung"] + ["G-8"] + ["City Gas Tarakan"], y_label="Total Sales (MMSCFD)",
                            data=tabelOilGas,
                            color=["#195B6F","#90E5FF", "#FFD758", "#FCE59A"],
                            use_container_width=True)

    st.divider()
    locMedco = st.selectbox("Pilih Lokasi", ["Semua", "City Gas", "PLN"], key="locMedco")

    st.subheader("Sales Medco")
    if locMedco == "City Gas" :
        st.area_chart(x="DATE", x_label="Tanggal",
                    y="Medco to City Gas", y_label ="Total Sales (MMSCFD)",
                    data=tabelOilGas,
                    use_container_width=True)
    elif locMedco == "PLN" :
        st.area_chart(x="DATE", x_label="Tanggal",
                        y="Medco to PLN", y_label ="Total Sales (MMSCFD)",
                        data=tabelOilGas,
                        use_container_width=True)
    else :
        st.area_chart(x="DATE", x_label="Tanggal",
                    y=["Medco to City Gas"] + ["Medco to PLN"], y_label ="Total Sales (MMSCFD)",
                    data=tabelOilGas,
                    use_container_width=True)
except KeyError as e :
    st.error("Data tidak tersedia pada Database.")