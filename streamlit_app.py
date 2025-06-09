import streamlit as st
import requests
from config import BACKEND_URL



st.set_page_config(page_title="AI Bug Reporter MVP")

# Backend Health Check (Function haline getiriyoruz)
def check_backend():
    try:
        health_response = requests.get("http://localhost:8001/health", timeout=5)
        if health_response.status_code == 200:
            st.sidebar.success("Backend Connection: OK ✅")
        else:
            st.sidebar.warning("Backend Connection: WARNING ⚠️")
    except requests.exceptions.ConnectionError:
        st.sidebar.error("Cannot connect to backend. Make sure backend is running.")
    except Exception as e:
        st.sidebar.error(f"Health check error: {e}")

check_backend()

st.title("AI Bug Reporter")
st.write("Upload your log file and let AI analyze it.")

uploaded_file = st.file_uploader("Upload Log File", type=["txt", "log", "json"])

if uploaded_file is not None:
    log_content = uploaded_file.getvalue().decode("utf-8")
    st.subheader("Uploaded Log Content (Editable):")
    
    # Display the log content in a text area so user can edit it before submission
    edited_log_content = st.text_area("You can edit your log before submitting:", value=log_content, height=300)

    if st.button("Send to Backend"):
        try:
            with st.spinner("Log is being analyzed..."):
                response = requests.post(BACKEND_URL, json={"log_content": edited_log_content})

            if response.status_code == 200:
                st.success("Log successfully sent! AI is processing the report.")
                st.subheader("AI Bug Report:")
                st.json(response.json())
            else:
                st.error(f"Backend Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend. Make sure backend is running.")
        except Exception as e:
            st.error(f"Error: {e}")


st.info("After uploading the log file, AI will generate a bug report.")
