import streamlit as st
import requests

st.title("Email Sender UI")

# User inputs
uploaded_file = st.file_uploader("Choose a file to upload")
subject = st.text_input("Subject")
body = st.text_area("Body")

# API Endpoint
api_url = "http://localhost:8000/trs/api/email/send_email"

if st.button("Send Email"):
    if uploaded_file is None:
        st.error("Please upload a file.")
    else:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        data = {"subject": subject, "body": body}
        
        response = requests.post(api_url, files=files, data=data)
        
        if response.status_code == 200:
            st.success("Email sent successfully!")
        else:
            st.error(f"Failed to send email. Status code: {response.status_code}")
