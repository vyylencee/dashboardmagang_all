import streamlit as st
import datetime as dt
import pandas as pd
from zoneinfo import ZoneInfo
from load import save_data_to_google_sheet
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request

st.set_page_config(
    page_title="Dashboard Team PO PT PEP Bunyu Field",
    layout="wide",
    initial_sidebar_state="expanded"
)

waktuUpload = dt.datetime.now(ZoneInfo("Asia/Makassar")).strftime("%Y-%m-%d %H:%M:%S")
PATH_LOG = "data/log upload.csv"

st.title("⬆️ Upload Data Production")
st.divider()

credential = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=["https://www.googleapis.com/auth/spreadsheets"])

SPREADSHEET_ID = '1WwBp8XhrDM7WA-emRpvhDfbbRYVX_nWQtPmrwTmxEhA'

service = build('sheets', 'v4', credentials=credential)
credential.refresh(Request())
sheet = service.spreadsheets()

file = st.file_uploader("Upload Data dengan format .xlsx, .xls", type=["xlsx", "xls"])

bar_progress = st.progress(0)
text_progress = st.empty()

if file is not None :
    text_progress.text("Membaca data dari sheet PROD...")
    OilGasData = pd.read_excel(file, sheet_name="PROD")
    bar_progress.progress(25)

    text_progress.text("Membaca data dari sheet SUMUR INJEKSI...")
    wipData = pd.read_excel(file, sheet_name="SUMUR INJEKSI")
    bar_progress.progress(40)

    text_progress.text("Membaca data dari sheet WELL...")
    wellData = pd.read_excel(file, sheet_name="WELL")
    bar_progress.progress(60)

    text_progress.text("Menyimpan data ke Google Sheet... 80%")
    bar_progress.progress(80)

    try :
        save_data_to_google_sheet(OilGasData, wellData, wipData, "tabelOilGas", "tabelWell", "tabelWip")
        text_progress.text("Data berhasil diupload ke Google Sheet... 100%")
        bar_progress.progress(100)
        st.success("✅ Data berhasil diupload ke Google Sheet.")

    except Exception as e :
        st.error("⚠️ Data gagal diupload ke Google Sheet.")

st.divider()
st.subheader("Log Data Upload")

@st.cache_data(ttl=60)
def pull_data(sheet_table):
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{sheet_table}!A1:ZZ"
    ).execute()

    values = result.get('values', [])

    if not values:
        return pd.DataFrame()

    df = pd.DataFrame(values[1:], columns=values[0])

    return df

def read_data() :
    log_data = pull_data("log")
    return log_data

st.dataframe(read_data(), hide_index=True)