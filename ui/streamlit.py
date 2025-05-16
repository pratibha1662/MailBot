import streamlit as st
import requests

# API Endpoints
API_BASE_URL = "http://localhost:8000/trs/api/email"
SEND_EMAIL_URL = f"{API_BASE_URL}/send_email"
GENERATE_MESSAGE_URL = f"{API_BASE_URL}/generate_message"

st.title("📧 MailBot")

# Initialize session state
for key in ("creds", "subject", "body", "user_message", "email_generated"):
    if key not in st.session_state:
        st.session_state[key] = ""

# AI Help Section
with st.expander("💡 Need help writing the email? Get the help of AI now!", expanded=True):
    user_message = st.text_input("What should the email say? (include subject and idea)", key="user_message")

    if st.button("✨ Generate Email"):
        if not user_message.strip():
            st.warning("Please describe what the email should say.")
        else:
            data = {"user_message": user_message}
            response = requests.post(GENERATE_MESSAGE_URL, json=data)

            if response.status_code == 200:
                try:
                    content = response.json().get("content", {})
                    st.session_state.subject = content.get("subject", "")
                    st.session_state.body = content.get("body", "")
                    st.success("Generated subject and body successfully!")
                except Exception as e:
                    st.error(f"Error parsing the generated message: {e}")
            else:
                st.error(f"Failed to generate message: {response.status_code}")
                st.text(response.text)

# Now use updated session state values to prefill inputs
subject = st.session_state.subject
body = st.session_state.body

# File upload
uploaded_file = st.file_uploader("Upload a .txt file with email addresses", type=["txt"])

# Subject and body input widgets
subject = st.text_input("Subject", value=subject)
body = st.text_area("Body", value=body, height=200)

# Keep user edits reflected in session state
st.session_state.subject = subject
st.session_state.body = body

# Send Email
if body and subject:
    if st.button("📤 Send Email"):
        if uploaded_file is None:
            st.error("Please upload a file containing email addresses.")
        elif not subject or not body:
            st.error("Please fill out both subject and body before sending.")
        else:
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), 'text/plain')
            }
            data = {
                "subject": subject,
                "body": body,
                "creds": st.session_state.creds
            }

            response = requests.post(SEND_EMAIL_URL, files=files, data=data)
            if response.status_code == 200:
                try:
                    st.session_state.creds = response.json().get("creds", "")
                    st.success("Emails sent successfully!")
                except Exception:
                    st.warning("Emails sent, but unable to parse credentials.")
            else:
                st.error(f"Failed to send email. Status: {response.status_code}")
                st.text(response.text)
