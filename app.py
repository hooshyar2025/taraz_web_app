import streamlit as st
import pandas as pd
import dropbox
from io import BytesIO

# ---------- تنظیمات ورود ----------
USERS = {
    "hossein": "1234",
    "admin": "admin123",
    "mahdi": "pass456"
}

# ---------- تنظیمات Dropbox ----------
ACCESS_TOKEN = "<<<توکن واقعی شما>>>"
FILE_PATH = "/taraz_web/mali1405.xlsx"

# ---------- تابع تست ASCII ----------
def find_non_ascii(label, text):
    bad_chars = [(i, ch, ord(ch)) for i, ch in enumerate(text) if ord(ch) > 127]
    if bad_chars:
        st.warning(f"{label} contains non-ASCII characters:")
        for pos, char, code in bad_chars:
            st.write(f"Position {pos}: '{char}' (code {code})")
    else:
        st.success(f"{label} is clean ASCII ✅")

# ---------- توابع Dropbox ----------
def load_excel():
    try:
        dbx = dropbox.Dropbox(ACCESS_TOKEN)
        _, res = dbx.files_download(FILE_PATH)
        xls = pd.ExcelFile(BytesIO(res.content), engine="openpyxl")
        return {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}
    except UnicodeEncodeError as e:
        st.error(f"Dropbox UnicodeEncodeError: {e}")
        return {}

def save_excel(dfs_dict):
    try:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            for sheet, df in dfs_dict.items():
                df.to_excel(writer, sheet_name=sheet, index=False)
        dbx = dropbox.Dropbox(ACCESS_TOKEN)
        dbx.files_upload(buffer.getvalue(), FILE_PATH, mode=dropbox.files.WriteMode.overwrite)
    except UnicodeEncodeError as e:
        st.error(f"Dropbox UnicodeEncodeError while saving: {e}")

# ---------- فرم ورود ----------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 ورود به سیستم")
    username = st.text_input("نام کاربری")
    password = st.text_input("رمز عبور", type="password")
    if st.button("ورود"):
        if USERS.get(username) == password:
            st.session_state.auth = True
            st.success("ورود موفق ✅")
            st.rerun()
        else:
            st.error("نام کاربری یا رمز عبور اشتباه است")
else:
    st.subheader("🔍 تست توکن و مسیر Dropbox")
    find_non_ascii("ACCESS_TOKEN", ACCESS_TOKEN)
    find_non_ascii("FILE_PATH", FILE_PATH)

    data = load_excel()
    if data:
        st.header("📋 جدول مخاطبان جدید")
        df_customers = data.get("Sheet1", pd.DataFrame())
        st.dataframe(df_customers, use_container_width=True)
        with st.expander("➕ افزودن مخاطب جدید"):
            new_data = {col: st.text_input(f"{col}") for col in df_customers.columns}
            if st.button("ثبت مخاطب"):
                df_customers = df_customers._append(new_data, ignore_index=True)
                data["Sheet1"] = df_customers
                save_excel(data)
                st.success("مخاطب جدید اضافه شد ✅")
                st.rerun()
