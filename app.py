import streamlit as st
import pandas as pd
import dropbox
from io import BytesIO

# ---------- ورود ----------
USERS = {"hossein": "1234", "admin": "admin123", "mahdi": "pass456"}

# ---------- Dropbox ----------
ACCESS_TOKEN = "اینجا_توکن_واقعی"
FILE_PATH = "/taraz_web/mali1405.xlsx"

def load_excel():
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    _, res = dbx.files_download(FILE_PATH)
    xls = pd.ExcelFile(BytesIO(res.content), engine="openpyxl")
    return {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

def save_sheet(sheet_name, df):
    data = load_excel()
    data[sheet_name] = df
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for sheet, content in data.items():
            content.to_excel(writer, sheet_name=sheet, index=False)
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    dbx.files_upload(buffer.getvalue(), FILE_PATH, mode=dropbox.files.WriteMode.overwrite)

# ---------- فرم ورود ----------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 ورود به سیستم")
    user = st.text_input("نام کاربری")
    pwd = st.text_input("رمز عبور", type="password")
    if st.button("ورود"):
        if USERS.get(user) == pwd:
            st.session_state.auth = True
        else:
            st.error("❌ اطلاعات ورود اشتباه است")
else:
    data = load_excel()
    st.title("📂 مدیریت همه شیت‌ها")
    
    for sheet_name, df in data.items():
        st.subheader(f"📝 شیت: {sheet_name}")
        if df.empty:
            df = pd.DataFrame(columns=["ستون1", "ستون2", "ستون3"])  # ستون پیش‌فرض

        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key=f"editor_{sheet_name}")

        if st.button(f"💾 ذخیره تغییرات در {sheet_name}", key=f"save_{sheet_name}"):
            save_sheet(sheet_name, edited_df)
            st.success(f"✅ تغییرات در '{sheet_name}' ذخیره شد. برای مشاهده کامل، صفحه را Refresh کنید.")

    if st.button("🚪 خروج"):
        st.session_state.auth = False
