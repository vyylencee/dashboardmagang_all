import streamlit as st
import pandas as pd
from pathlib import Path
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

bulan = st.session_state.get("bulan", "Semua")

credential = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=['https://www.googleapis.com/auth/spreadsheets'])

SPREADSHEETS_ID = '1NZHkw-o3S708dd9Ng_Gwd_lj-VB4bPDVhjqrwySV8lg'

service = build('sheets', 'v4', credentials=credential)
credential.refresh(Request())
sheet = service.spreadsheets()

BASE_DIR = Path(__file__).resolve().parent
file_path_oil_gas = BASE_DIR / "data" / f"oilngas.csv"
file_path_wip = BASE_DIR / "data" / f"wip.csv"
file_path_well = BASE_DIR / "data" / f"well.csv"

bulan_map = {
    "Januari": 1,
    "Februari": 2,
    "Maret": 3,
    "April": 4,
    "Mei": 5,
    "Juni": 6,
    "Juli": 7,
    "Agustus": 8,
    "September": 9,
    "Oktober": 10,
    "November": 11,
    "Desember": 12
}


@st.cache_data
def pull_data(sheet_table) :
    result = sheet.values().get(
        spreadsheetId=SPREADSHEETS_ID,
        range=f"{sheet_table}!A1:ZZ"
    ).execute()

    values = result.get('values', [])

    if not values :
        return pd.DataFrame()

    df = pd.DataFrame(values[1:], columns=values[0])

    return df

def read_data() :
    tabelOilGas = pull_data("tabelOilGas")
    tabelWip = pull_data("tabelWip")
    tabelWell = pull_data("tabelWell")

    return tabelOilGas, tabelWip, tabelWell

def transform_data (month, year):
    tabelOilGas, tabelWip, tabelWell = read_data()

    tabelOilGas["DATE"] = pd.to_datetime(tabelOilGas["DATE"],format="%Y-%m-%d")
    tabelWip["DATE"] = pd.to_datetime(tabelWip["DATE"],format="%Y-%m-%d")
    tabelWell["Date"] = pd.to_datetime(tabelWell["Date"],format="%Y-%m-%d")

    tabelWip["Flowrate (BWPD)"] = pd.to_numeric(tabelWip["Flowrate (BWPD)"].str.replace(",", "."), errors="coerce").fillna(0)
    tabelWip["Tekanan (PSI)"] = pd.to_numeric(tabelWip["Tekanan (PSI)"].str.replace(",", "."), errors="coerce").fillna(0)

    tabelOilGas["SALES PLN Bunyu"] = pd.to_numeric(tabelOilGas["SALES PLN Bunyu"].str.replace(",", "."), errors="coerce")
    tabelOilGas["SALES City Gas Bunyu"] = pd.to_numeric(tabelOilGas["SALES City Gas Bunyu"].str.replace(",", "."), errors="coerce")
    tabelOilGas["SALES City Gas Tarakan"] = pd.to_numeric(tabelOilGas["SALES City Gas Tarakan"].str.replace(",", "."), errors="coerce")
    tabelOilGas["G-8"] = pd.to_numeric(tabelOilGas["G-8"].str.replace(",", "."), errors="coerce")
    tabelOilGas["Binalatung"] = pd.to_numeric(tabelOilGas["Binalatung"].str.replace(",", "."), errors="coerce")
    tabelOilGas["Kampung 1"] = pd.to_numeric(tabelOilGas["Kampung 1"].str.replace(",", "."), errors="coerce")
    tabelOilGas["City Gas Tarakan"] = pd.to_numeric(tabelOilGas["City Gas Tarakan"].str.replace(",", "."), errors="coerce")


    tabelWell["Prod Act Oil"] = pd.to_numeric(tabelWell["Prod Act Oil"].str.replace(",", "."), errors="coerce")
    tabelWell["Prod Act Gross"] = pd.to_numeric(tabelWell["Prod Act Gross"].str.replace(",", "."), errors="coerce")
    tabelWell["Gas Own (Mscfd)"] = pd.to_numeric(tabelWell["Gas Own (Mscfd)"].str.replace(",", "."), errors="coerce")
    tabelWell["Gas Inj (Mscfd)"] = pd.to_numeric(tabelWell["Gas Inj (Mscfd)"].str.replace(",", "."), errors="coerce")
    tabelWell["Prod Act WC"] = pd.to_numeric(tabelWell["Prod Act WC"].str.replace(",", "."), errors="coerce")

    tabelWell["P.csg"] = pd.to_numeric(tabelWell["P.csg"].str.replace(",", "."), errors="coerce")
    tabelWell["P.tbg"] = pd.to_numeric(tabelWell["P.tbg"].str.replace(",", "."), errors="coerce")
    tabelWell["P.fl"] = pd.to_numeric(tabelWell["P.fl"].str.replace(",", "."), errors="coerce")
    tabelWell["P.sep"] = pd.to_numeric(tabelWell["P.sep"].str.replace(",", "."), errors="coerce")

    # Medco to City Gas,Medco to PLN
    tabelOilGas["Medco to City Gas"] = pd.to_numeric(tabelOilGas["Medco to City Gas"].str.replace(",", "."), errors="coerce")
    tabelOilGas["Medco to PLN"] = pd.to_numeric(tabelOilGas["Medco to PLN"].str.replace(",", "."), errors="coerce")

    tabelOilGas["PROD OIL (SOT)"] = pd.to_numeric(tabelOilGas["PROD OIL (SOT)"].str.replace(",", "."), errors="coerce")
    tabelOilGas["PROD GAS (MSCFD)"] = pd.to_numeric(tabelOilGas["PROD GAS (MSCFD)"].str.replace(",", "."), errors="coerce")
    tabelOilGas["TOTAL SALES"] = pd.to_numeric(tabelOilGas["TOTAL SALES"].str.replace(",", "."), errors="coerce")
    tabelOilGas["PROD WATER"] = pd.to_numeric(tabelOilGas["PROD WATER"].str.replace(",", "."), errors="coerce")
    tabelOilGas["INJECTION WATER"] = pd.to_numeric(tabelOilGas["INJECTION WATER"].str.replace(",", "."), errors="coerce")
    tabelOilGas["TARGET PRODUKSI OIL (RKAP)"] = pd.to_numeric(tabelOilGas["TARGET PRODUKSI OIL (RKAP)"].str.replace(",", "."), errors="coerce")
    tabelOilGas["TARGET PRODUKSI OIL (WP&B)"] = pd.to_numeric(tabelOilGas["TARGET PRODUKSI OIL (WP&B)"].str.replace(",", "."), errors="coerce")
    tabelOilGas["TARGET RKAP GAS"] = pd.to_numeric(tabelOilGas["TARGET RKAP GAS"].str.replace(",", "."), errors="coerce")
    tabelOilGas["TARGET WP&B GAS"] = pd.to_numeric(tabelOilGas["TARGET WP&B GAS"].str.replace(",", "."), errors="coerce")


    if year == "Semua" :
        tabelOilGas = tabelOilGas.sort_values("DATE", ascending=True)
        tabelWip = tabelWip.sort_values("DATE", ascending=True)
        tabelWell = tabelWell.sort_values("Date", ascending=True)
        if month == "Semua":
            tabelOilGas = tabelOilGas.sort_values("DATE", ascending=True)
            tabelWip = tabelWip.sort_values("DATE", ascending=True)
            tabelWell = tabelWell.sort_values("Date", ascending=True)
        else :
            tabelOilGas = tabelOilGas[tabelOilGas["DATE"].dt.month == bulan_map[month]]
            tabelWip = tabelWip[tabelWip["DATE"].dt.month == bulan_map[month]]
            tabelWell = tabelWell[tabelWell["Date"].dt.month == bulan_map[month]]

            tabelOilGas = tabelOilGas.sort_values("DATE", ascending=True)
            tabelWip = tabelWip.sort_values("DATE", ascending=True)
            tabelWell = tabelWell.sort_values("Date", ascending=True)
    else :
        tabelOilGas = tabelOilGas[tabelOilGas["DATE"].dt.year == int(year)]
        tabelWip = tabelWip[tabelWip["DATE"].dt.year == int(year)]
        tabelWell = tabelWell[tabelWell["Date"].dt.year == int(year)]

        if month == "Semua":
            tabelOilGas = tabelOilGas.sort_values("DATE", ascending=True)
            tabelWip = tabelWip.sort_values("DATE", ascending=True)
            tabelWell = tabelWell.sort_values("Date", ascending=True)
        else :
            tabelOilGas = tabelOilGas[tabelOilGas["DATE"].dt.month == bulan_map[month]]
            tabelWip = tabelWip[tabelWip["DATE"].dt.month == bulan_map[month]]
            tabelWell = tabelWell[tabelWell["Date"].dt.month == bulan_map[month]]

            tabelOilGas = tabelOilGas.sort_values("DATE", ascending=True)
            tabelWip = tabelWip.sort_values("DATE", ascending=True)
            tabelWell = tabelWell.sort_values("Date", ascending=True)
        
        
    return tabelOilGas, tabelWip, tabelWell