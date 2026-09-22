import pandas as pd
import datetime as dt
from datetime import date
import streamlit as st
from zoneinfo import ZoneInfo
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


waktuUpload = dt.datetime.now(ZoneInfo("Asia/Makassar")).strftime("%Y-%m-%d %H:%M:%S")
PATH_LOG = "data/log upload.csv"

SERVICE_ACCOUNT_FILE = "dashboard-magang-all-9de09e4a0ada.json"

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credential = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)

SPREADSHEET_ID = '1NZHkw-o3S708dd9Ng_Gwd_lj-VB4bPDVhjqrwySV8lg'
RANGE_NAME = 'Sheet1'

@st.cache_data(ttl=60)
def save_data_to_google_sheet(data1, data2, data3, sheet1, sheet2, sheet3) :
    try :
        credential.refresh(Request())
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()

        df1 = data1.copy()
        df2 = data2.copy()
        df3 = data3.copy()

        df1 = df1.map(
            lambda x: x.strftime("%Y-%m-%d")
            if isinstance(x, (pd.Timestamp, dt.datetime, dt.date))
            else x
        )
        df2 = df2.map(
            lambda x: x.strftime("%Y-%m-%d")
            if isinstance(x, (pd.Timestamp, dt.datetime, dt.date))
            else x
        )
        df3 = df3.map(
            lambda x: x.strftime("%Y-%m-%d")
            if isinstance(x, (pd.Timestamp, dt.datetime, dt.date))
            else x
        )

        df1 = df1.fillna("")
        df2 = df2.fillna("")
        df3 = df3.fillna("")

        df1 = df1.astype(str)
        df2 = df2.astype(str)
        df3 = df3.astype(str)

        values1 = [df1.columns.tolist()] + df1.values.tolist()
        values2 = [df2.columns.tolist()] + df2.values.tolist()
        values3 = [df3.columns.tolist()]  + df3.values.tolist()

        batch_upload = 1000

        sheet.values().clear(spreadsheetId=SPREADSHEET_ID, range=f"{sheet1}!A1").execute()
        sheet.values().clear(spreadsheetId=SPREADSHEET_ID, range=f"{sheet2}!A1").execute()
        sheet.values().clear(spreadsheetId=SPREADSHEET_ID, range=f"{sheet3}!A1").execute()

        for a in range (0, len(values1), batch_upload):
            batch_values1 = values1[a:a + batch_upload]
            body1 = {
                'values': batch_values1
            }
            sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=f"{sheet1}!A1",
                valueInputOption="RAW",
                body=body1
            ).execute()

        for b in range (0, len(values2), batch_upload):
            batch_values2 = values2[b:b + batch_upload]
            body2 = {
                'values': batch_values2
            }
            sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=f"{sheet2}!A1",
                valueInputOption="RAW",
                body=body2
            ).execute()

        for c in range (0, len(values3), batch_upload):
            batch_values3 = values3[c:c + batch_upload]
            body3 = {
                'values': batch_values3
            }
            sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=f"{sheet3}!A1",
                valueInputOption="RAW",
                body=body3
            ).execute()   

        body = {
                'values': [[waktuUpload, "Sheet Oil Gas", "Sheet WIP", "Sheet Well", "✅ Berhasil"]]
            }
        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="log!A2",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()

        st.cache_data.clear()
        return True
    except Exception as e :
        body = {
                'values': [[waktuUpload, "Sheet Oil Gas", "Sheet WIP", "Sheet Well", "⚠️ Gagal"]]
            }
        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="log!A2",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        st.cache_data.clear()
        return False

# def load_data (oilgas, wip, well) :
#     try :
#         oilgas.to_csv("data/oilngas.csv", index=False)
#         wip.to_csv("data/wip.csv", index=False)
#         well.to_csv("data/well.csv", index=False)

#         dataLog = pd.DataFrame([{
#             "Waktu Upload" : waktuUpload,
#             "File Production Oil & Gas" : "oilngas.csv",
#             "File WIP" : "wip.csv",
#             "File Well" : "well.csv",
#             "Status" : "✅ Berhasil"
#         }])

#         if os.path.exists(PATH_LOG) :
#             dataLog.to_csv("data/log upload.csv", index=False, mode="a", header=False)
#         else :
#             dataLog.to_csv("data/log upload.csv", index=False, mode="w")
#         return True
#     except Exception as e :
#         dataLog = {
#                     "Waktu Upload" : waktuUpload,
#                     "File Production Oil & Gas" : "-",
#                     "File WIP" : "-",
#                     "File Sales" : "-",
#                     "Status" : "⚠️ Gagal"
#                 }
#         if os.path.exists(PATH_LOG) :
#             dataLog.to_csv("data/log upload.csv", index=False, mode="a", header=False)
#         else :
#             dataLog.to_csv("data/log upload.csv", index=False, mode="w")