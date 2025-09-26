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
ACCESS_TOKEN = "sl.u.AGAXivpwKhIY5hIWD4EEKapN8tF6ri0gHC_QaVogr0vSOcwkOBnaneZwrRhj0dVJTjY2b7-TaSVHK8_c_rHaSyoptSpk5itlIxsh_B-IVg4tZwQFbcoW83ngHXO7AUmexlDIgfRx-9cZa2YhchtmYCIWiEKpisHKPCRx1_IKifbYe_RN0IwhSrm0SKaR0V5aLRF6Nmrkql97BuOlUE2hvU1xFk1U6Wdr8XInis95VcFsrzb4PgB8_pgFwdLGkdnUrKfpOXGKp72NsXO3km4kgoa-I_G1KH9mpleakO3vDaiuLUTnBSjDKFigFnt535PhzJ4snB7PN_QgBeIQHRXQiOfbxzzDu8taX8vlxJBYokXFQ76MlPNsYHVid6aTXRauc5376XoYLFrKYafDogIsCuFs5iuQbnDrlecbPMf18XWebcZQnNHyi64tFq5giwT8ky1beiIzGSDDv5Ur-EwEf-r5V-TLs-XcTA4oECCh76wfJ2qd5p7U-GF9Y4__zwjT-htWxn0OidFnGOLPUpjPFVEdWk7LIyPbrf-A38Ytjxtb09PEv7GAxAJrj0EN6kP-evSnKgnw6Xtfi4fpOIUSIfYNaRA259CExefAGNAgzOIrBgkC6yFgMWAYRTfSHUPkfqv0KzbYOhqvJwcl4GN27n37RgToZDobDb293hxjKB07hPVsA3CvkvfcP2Jeb-wy6ida4S-F9nyQiPThDLzW5O8rFBf8P-DBWZmnmQtqD63an8HrSVxYp-Xi8qzqFqOu8fBwdnp1goNcVpQvdgUR47sgF13J7kLS1IRjz0d6vDHJNeogm85He7lEnUjCLqGzYTa-x5dT30_zD0ajokpUVQ5pQfRXsnkP6NITaJzKrOhgRLDfDo5l8R9HWK0C6c5r0aH-3oLKraE-_IH91e7XgawxwtxRQ-zjPlbDkHhzHELrS3ED6DsblCDe5REYcHMrHFdx3ISbIg1tIC2KZ0TZKFN2klgtnLgwXtjwm1pnDZuiftT5R9h-6meavCcTJT3mQNwWHktfSylIKElFh9czNFavrUPTk1VlThzeNV8fqds7Q1njg8c6uSMOAhyF5OLBTzbUL3jzaqGl-9bYfLfFG4BdOiA7AQjrEcHuXePRwgKZ24KrL-CqsDGI7jg_OzslQmEa83Z_zCl6FgtbVkaPtCvZguQch-nWgfTv_7q4JM05hUY4g6r6SwrEcyadpA08ZyRMI-X9I3DBisjquIhVji61YnbyTnV39R14vUgTEaUVE72HXyScJi43T6gKks9rt2cf"
FILE_PATH = "/taraz_web/mali1405.xlsx"

# ---------- توابع Dropbox ----------
def load_excel():
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    _, res = dbx.files_download(FILE_PATH)
    xls = pd.ExcelFile(BytesIO(res.content), engine="openpyxl")
    return {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

def save_excel(dfs_dict):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for sheet, df in dfs_dict.items():
            df.to_excel(writer, sheet_name=sheet, index=False)
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    dbx.files_upload(buffer.getvalue(), FILE_PATH, mode=dropbox.files.WriteMode.overwrite)

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
    data = load_excel()

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

    st.header("💰 جدول امور مالی")
    df_mali1 = data.get("mali1", pd.DataFrame())
    st.dataframe(df_mali1, use_container_width=True)
    with st.expander("➕ ثبت خدمات/هزینه"):
        mali1_data = {col: st.text_input(f"{col}") for col in df_mali1.columns}
        if st.button("ثبت خدمات"):
            df_mali1 = df_mali1._append(mali1_data, ignore_index=True)
            data["mali1"] = df_mali1
            save_excel(data)
            st.success("خدمات جدید ثبت شد ✅")
            st.rerun()

    st.header("💳 جدول پرداخت‌ها و سررسیدها")
    df_mali2 = data.get("mali2", pd.DataFrame())
    st.dataframe(df_mali2, use_container_width=True)
    with st.expander("➕ ثبت پرداختی/سررسید"):
        mali2_data = {col: st.text_input(f"{col}") for col in df_mali2.columns}
        if st.button("ثبت پرداختی"):
            df_mali2 = df_mali2._append(mali2_data, ignore_index=True)
            data["mali2"] = df_mali2
            save_excel(data)
            st.success("پرداختی جدید ثبت شد ✅")
            st.rerun()

    if st.button("🚪 خروج"):
        st.session_state.auth = False
        st.rerun()
