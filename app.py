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
ACCESS_TOKEN = "sl.u.AGAXsQ2UXNMbFK2Rkzor_Vh7gJcEpB5PGXeRs7RM-h0D2fd5goRdS8mjTpacfDVUM9U8O4bLoHF72lYbTtXrWrP7DVx_f7j0diVp_zyUFMDuiXIMyzo3IzZjXFP1NeL_gRWBhh3Kn0Il2D-YV3Wh8pW1ZZJlyaw1VLnGERB8dRFjB89MdjS75CTOSAilwlfo6fUhwPMoRYOb8p3CIL9WKlkGXU0D0KirZPQicKEG6iO7acrf1mrnVpy0jKea0hnTPZ9tr_T5ukl29A9PXmK3PdvLXIZGEevBO3XvWR_h0umI7oyPzPXoHZm34BCJDjNle-Xrg_fMyM39ytl1vSmf2RklW4HDkVStPZN2q8Qp0QVWyzeWmx-dKYHjIe6zfFzhr6W3QEMHS3RPNxhbd6NOq6xGR1yqpcjo0XkP6kPECYJ5eJZC8hq-L0R8QrYMLQ8bSVy_-qJUPQBqqP9skDHBcAGWFz2S6pz-S3JmbtHVgvQPldg_Gqnk-aN03VVn1ISYVM2bygos5AGBwgb8ee61qarSk2uUN9usAB0Ur7QJ_qwCydgNyqp1t86dBRd7fzYLfDHPMhS1L_X3hMFPtoZgirUrWyBBAMYasbQsoKr04NHkj7CdOhndnPn6JOzDDJ69WaJowwj4L-qsk-UKTgtBsSWa5jJie4fJoZslnqnoeEW-n0ZAo_iDgP_D0pkg-R7Z4thWvb3ZazKZGdNWzNi4x9gZxP1iZXxwjVCssF4ssaSvuLOXbTPfResziKrDVV2YeInyKJ-zAjclEMiCD1a24ydGRXcN6COjw6-8pWIBUD21RT1To3v737SUYSmmdeVO-lQvY7AxPK_Q9Djive2O4spXYWEKH8rtgr0gE_BjMQ72_AQbDURGIxrTxbbgLjFM91XnOHwvwnNtRzS5MQtb0bgGACuMtJ31ls_r32rctSFU_KbIilk0s17GQCXzQPc1UPzxAS03ADluMPllBuAig_lZ3XsL28IPgspTQksLk6tQdIIZ416TevgI0KCLBYJMXdoGoVwNAFjsZZgbf-2bJ0AGim5NZlkLtocbIVI1Qg_H6kBhQJJDN2l9ubEcC6oP6cPpQplARria4LZM_KC3orYe0hyHGQlx31V_PneQZkQcmwNBXnCwCBHuJAOgMKQ6oLmWOBYwTCRsAi25t-o8Hwa35AExNqGUNWgbbPTI8vpBX4wRsNO3NdD3tUaJRwxeu5OqWZjKtg5RgLr3B467XmN98xiBA9DHqgxiGVz0GJLfgkOFAUBs5jYUPVS0vXfxIqycR_5ah9XhmiQI_wFI1KNDq6vT07IELhbuVWErswIOxjkteVPpeZla1w3HNZq1VidbqNBHu6zRHgWNuV2VW2l4lLopaDhG2HLtsyRqobeD2hJxPa7cXQLEr2RAlv0bWba78saeXQWgb-xnoy9umI1pjBx6pUJbtzyaWftm4Yn1bw"
FILE_PATH = "/taraz_web/mali1405.xlsx"

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
