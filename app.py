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
ACCESS_TOKEN = "..."  # توکن جدیدت رو اینجا بذار
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
    username = st.text_input("نام کاربری", key="login_user")
    password = st.text_input("رمز عبور", type="password", key="login_pass")
    if st.button("ورود", key="login_btn"):
        if USERS.get(username) == password:
            st.session_state.auth = True
            st.success("ورود موفق ✅")
            st.experimental_rerun()
        else:
            st.error("نام کاربری یا رمز عبور اشتباه است")

else:
    data_dict = load_excel()

    # ---------- data (مخاطبان) ----------
    st.header("📋 جدول مخاطبان")
    df_data = data_dict.get("data", pd.DataFrame())
    st.dataframe(df_data, use_container_width=True)
    with st.expander("➕ افزودن مخاطب جدید"):
        new_data = {col: st.text_input(f"{col}", key=f"data_{col}") for col in df_data.columns}
        if st.button("ثبت مخاطب", key="btn_data"):
            df_data = df_data._append(new_data, ignore_index=True)
            data_dict["data"] = df_data
            save_excel(data_dict)
            st.success("مخاطب جدید اضافه شد ✅")
            st.experimental_rerun()

    # ---------- mali1 ----------
    st.header("💰 جدول امور مالی")
    df_mali1 = data_dict.get("mali1", pd.DataFrame())
    st.dataframe(df_mali1, use_container_width=True)
    with st.expander("➕ ثبت خدمات/هزینه"):
        mali1_data = {col: st.text_input(f"{col}", key=f"mali1_{col}") for col in df_mali1.columns}
        if st.button("ثبت خدمات", key="btn_mali1"):
            df_mali1 = df_mali1._append(mali1_data, ignore_index=True)
            data_dict["mali1"] = df_mali1
            save_excel(data_dict)
            st.success("خدمات جدید ثبت شد ✅")
            st.experimental_rerun()

    # ---------- mali2 ----------
    st.header("💳 جدول پرداخت‌ها و سررسیدها")
    df_mali2 = data_dict.get("mali2", pd.DataFrame())
    st.dataframe(df_mali2, use_container_width=True)
    with st.expander("➕ ثبت پرداختی/سررسید"):
        mali2_data = {col: st.text_input(f"{col}", key=f"mali2_{col}") for col in df_mali2.columns}
        if st.button("ثبت پرداختی", key="btn_mali2"):
            df_mali2 = df_mali2._append(mali2_data, ignore_index=True)
            data_dict["mali2"] = df_mali2
            save_excel(data_dict)
            st.success("پرداختی جدید ثبت شد ✅")
            st.experimental_rerun()

    # ---------- chik ----------
    st.header("📦 جدول chik")
    df_chik = data_dict.get("chik", pd.DataFrame())
    st.dataframe(df_chik, use_container_width=True)
    with st.expander("➕ افزودن رکورد جدید به chik"):
        chik_data = {col: st.text_input(f"{col}", key=f"chik_{col}") for col in df_chik.columns}
        if st.button("ثبت chik", key="btn_chik"):
            df_chik = df_chik._append(chik_data, ignore_index=True)
            data_dict["chik"] = df_chik
            save_excel(data_dict)
            st.success("رکورد جدید به chik اضافه شد ✅")
            st.experimental_rerun()

    # ---------- moshawre ----------
    st.header("📑 جدول moshawre")
    df_moshawre = data_dict.get("moshawre", pd.DataFrame())
    st.dataframe(df_moshawre, use_container_width=True)
    with st.expander("➕ افزودن رکورد جدید به moshawre"):
        moshawre_data = {col: st.text_input(f"{col}", key=f"moshawre_{col}") for col in df_moshawre.columns}
        if st.button("ثبت moshawre", key="btn_moshawre"):
            df_moshawre = df_moshawre._append(moshawre_data, ignore_index=True)
            data_dict["moshawre"] = df_moshawre
            save_excel(data_dict)
            st.success("رکورد جدید به moshawre اضافه شد ✅")
            st.experimental_rerun()

    # ---------- خروج ----------
    if st.button("🚪 خروج", key="btn_logout"):
        st.session_state.auth = False
        st.experimental_rerun()
