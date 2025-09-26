
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
ACCESS_TOKEN = "sl.u.AGB_EZ4uw2zZ-WuWOWyeJHe6_MpOGi1xpzvpi_vrPZIJjhwZzSLmSrO4DLaQPJt4INEojwTx4HG9BjTSZbjgG-GKaNBIOixd7aqHh7jqBg6rg5S2tMYJnHUm_dvcjw5swEfAZfQl_b2SUlnFZFvy6AlqwvXO3AN7gzUmUsbQKLp7AkUIWNRi5sNyTaqNcsnNHeY9WOKqJhgQCLaCzufFOy1iLzCCD5FLpsYuAFVAiSOsCgpsQYcD4mOilpNJ_OP27EgEJZ6POMRG2lx0kXTJHOn8YZ3jgF5L6AhJaOjymr8nYYaCzzAPCxtW3v95sslzZfQxyB1TLt9ItI6ZhC3YXDE0JsdOxEMslAaXVp9gW-cAHDqoTQbvhOEGUD-cpnW6vDVl8FHm4A2EdHGvi-jdPp4VxxykP2V95wGddwT2OUp9ZrVumVworBCLtAET2KOxAL05buacenVYulHgwyM8_BrsNgnECNO5vA3EHceGOmFWk199shwgQNqBry99R70vqduEjqALV9fnIvZfrVaPR56s2o5BAZLCBs5CnFwbLK1L-j98eLIzJMVQj2a_UPWjkQ7QbJfQc7_eWpvPNB6-CrgMTR17-KWgdPxYUsCKLNsCntqhovhRmpr2mPn_jyNiFFvH0nnbCAQOtZlB0F3MQUecqVwesfOvjt2mK7ff-PltqUispBa-OAqk-V_pAj3__jABxx1Js6NeZqh0oiAonR9TX0KYpa1of8zmXFW_jUvmTNLgTivhTSe3uRNml1so2NCaNb36gNqRc4T4q91jJb3hrrbNY3URKBgylhNQrbYknwdjBOhyMECSZ2-gaviRNMUZMFXG1Vv5tw8k8n96wWxTlKJ2FlE4Q6tSnQ_4DQXK9XbbKNUwCY5UABdVAVc71bonSg0aGfMZMWP23gXkQKgNFgUjtDFT82zHOTujQPYUAAmuou9iPdTfJDNs1fHjL4ha3IFNNEjMi0VJxu_twT09zOinOncapOODt3ZD3220lzanhpbaydngvwrTkHxUeqXf1LSiO7YkqvkMkfqK5hCRxuj4GlwvfqfyvsQXy5K8s4SAwziToYgFGD6DbebDKbdyQMUyDQhM_5qoLE8rDdqAXX6-h5_Onw7mQID2jJ2KLsqdWnEAN8ROBo4Q2ajt57X-3qxJXAIJ6tFXGQXvvHEsus-7QraE4qYtyCT9QRlouLbndBBZ95d0YaqbH6EUNQI2nxU4g_tkZIM4rJqyPlJjrt-9MNL98ngjbb69-yYFf9eDFMhxVqVfsDWcyycZhyN59yQMQ-MClVYFAB1dj9VBIAv1_HvNageorrd2G6GgTTXxJcizmBTbor7zfcuzpWF283rTbmw2aa0I-wheVh86hSXKYfUWEbv3docGJA7iRcIKAX8FOFeHzHiG6wEtVCGq0A1boFdJ8oDA04L0I3wEuSYYYRnJV6Q6S3PpMeh_6g"
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
            st.experimental_rerun()
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
            st.experimental_rerun()

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
            st.experimental_rerun()

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
            st.experimental_rerun()

    if st.button("🚪 خروج"):
        st.session_state.auth = False
        st.experimental_rerun()
