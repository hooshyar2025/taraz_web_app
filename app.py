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
ACCESS_TOKEN = "sl.u.AGBdyAP2uB98Z66CQRyudZdvqY-Y08Q5Tt8tDk10Lh78bgRDFszwzV021qi5f_PFo7a7SDAO84cZHaZfGlyJqnEFtP4NZ5--E3dbv4r1E_4j2uynZoi1VkgqwTo_-PqOKf8JB22I52FpbCqB7PScZ08oqV-VIcalHr7KKPgp3Ex6rf4fP0fIAaRpIklQ1z_uMFrm1gH56F8q8ZRHVzqkxNDG6GkZCbsjhjZRwGJNqsQ-697-swVrjnnaPLLGBGPRrvbafLEFBPpH8L4zZkPsHosqSjbSITqDPozuY_P8slfsiutx-MHndeBwdFQnCN1svtZu2XM6UnfmZMHrZTLSh7zoMnJjuOf0joMi_LVJq_lD8oN4-kG_Bh5q5l0NV4s_sjclKEAB73YGwJXytBzCL6tcpxWpr8HTRDLAdpZua5J_1R7jFiQfMu8-458UTHYHChVhS4WxbC-0bHR8nw26Woyvw-9FbBK2UNBGXl_JJVykiaDVekHVJmpppj73H-RF0Dy9sARiv0dvcpzoRrZdUsAAs2ARUlf67O5Db6U9S6IXWyp1x9bwujDHKFQeHImUb6zn8kq8IGTEKsK4-2blT9q52A-EH34glBy9wl6taoBeAM4xrh7VCSzoSiOkh1Q7Luy1TLPcOKDVRFFVjmiqoE_KssqIHVpRXMMFTOxd5idindZNIhAcpTje7BreeGaNu7N4LGMiPPPTPqkWztfj38CkbjGHyuES2QJDpIz4dgbskvCSEKfdNL6MgbHViHnU2K-KLPQPPcCxon8aXsB_hkOUEQDsFKpHxf0NO1VyzU9gmsnRco-W2Hs9JUCidAXw4mpCeRoDP1PWnjRY37OeAlMzlTwAN09uSw4LhOcBA2HmGHt1ibKVHVLXe8SZ5NNv82jfpJDgrK8dUTuZWwkYZWcYVvjj0mU1ZRLZacmUiz-eA2vuc_gqvjA2cIE_qeKatLC58cAfkOliOQVOD7QwUTBczidoouZg7oTH9dMC_oMFpXSED_QnUdn5fLQQ0_Lfhdg2WJwknoItbELx3sFq600JKPbpLiJKmHdwVqy1e67RL3uzLIeqB-xd33AwE1GGKl8KJiJPB-yk0LAbdcU5w4gMpDSf1c6yt4j7sEP5F3H_Ob6VNN6BS6ZPw-0DTCl79NE7NzQmV2Y2G4Aoytyze2nu8ugbnYMNRt98vOlG1zlfUtwWRLb2_Qf2S2VFtjFY3QARGPOHLSTXlK_-qWYyt8mNsYh1McFrw8tgWYhi3LNb3lvDAIbsn2N3G_-XzXnK9UjsR4ICLcPPzJJ_in64GngffoFTtiPcgpYi6VrPdB4fD4GXJbVGR3_lOqLA_fV4CYCvtyJs8fzBk75b7Wtaz6V3wNBDFb58NDKWTfIQ-Ful7MzF48ZYM2NjXK1L66E9C9dlUJPR6YdS7ZmfPIksq8GafKTgF44FDhMNEuOMRl-H8g"
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
    except Exception as e:
        st.error(f"Dropbox Error: {e}")
        return {}

def save_excel(dfs_dict):
    try:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            for sheet, df in dfs_dict.items():
                df.to_excel(writer, sheet_name=sheet, index=False)
        dbx = dropbox.Dropbox(ACCESS_TOKEN)
        dbx.files_upload(buffer.getvalue(), FILE_PATH, mode=dropbox.files.WriteMode.overwrite)
    except Exception as e:
        st.error(f"Dropbox Error while saving: {e}")

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
    st.subheader("🔍 تست ASCII روی توکن و مسیر فایل")
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
