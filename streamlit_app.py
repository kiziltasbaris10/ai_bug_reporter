import streamlit as st
import requests
from config import BACKEND_URL

# Sayfa başlığı
st.set_page_config(page_title="AI Bug Reporter MVP")
st.title("AI Bug Reporter")

st.write("Upload your log file and let AI analyze it.")

# Log dosyası yükleme
uploaded_file = st.file_uploader("Upload Log File", type=["txt", "log", "json"])

if uploaded_file is not None:
    # Dosya içeriğini oku
    log_content = uploaded_file.getvalue().decode("utf-8")
    st.subheader("Uploaded Log Content:")
    st.code(log_content, language="text")

    if st.button("Send to Backend"):
        try:
            # Backend'e POST isteği gönder
            response = requests.post(BACKEND_URL, json={"log_content": log_content})

            if response.status_code == 200:
                st.success("Log successfully sent and processed!")
                st.subheader("AI Bug Report:")
                st.json(response.json())
            else:
                st.error(f"Backend Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend. Make sure backend is running.")
        except Exception as e:
            st.error(f"Error: {e}")

st.info("After uploading the log file, AI will generate a bug report.")
