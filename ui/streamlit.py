import streamlit as st
import requests

st.title("MailBot")

# User inputs
uploaded_file = st.file_uploader("Please upload a .txt file containing the list of email IDs", type=["txt"])
subject = st.text_input("Subject")
body = st.text_area("Body")

if "creds" not in st.session_state:
    st.session_state.creds = ""

# API Endpoint
api_url = "http://localhost:8000/trs/api/email/send_email"

if st.button("Send Email"):
    if uploaded_file is None:
        st.error("Please upload a file.")
    else:
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), 'text/plain')
        }
        data = {
            "subject": subject or "",
            "body": body or "",
            "creds": st.session_state.creds or ""
        }

        response = requests.post(api_url, files=files, data=data)

        if response.status_code == 200:
            try:
                response_json = response.json()
                st.session_state.creds = response_json.get("creds", "")
                st.success("Email sent successfully!")
            except Exception:
                st.success("Email sent! But couldn't parse credentials.")
        else:
            st.error(f"Failed to send email. Status code: {response.status_code}")
            st.text(response.text)