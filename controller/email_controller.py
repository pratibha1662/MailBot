from fastapi import APIRouter, status, File, Form, UploadFile
from fastapi.responses import JSONResponse
from services import email_service, oauth_service

email_router=APIRouter()
@email_router.post("/send_email",operation_id="send_email")
async def send_email(
    file: UploadFile = File(...),
    subject: str = Form(...),
    body: str = Form(...)
):
    try:
        file_content = await file.read()
        email_addresses = file_content.decode("utf-8").splitlines() 
        
        email_addresses = [email.strip() for email in email_addresses if email.strip()]
        creds = oauth_service.get_oauth_creds()
        send_email = email_service.send_gmail(creds, email_addresses, subject, body)
        response={"status":"Success","message":"EMAIL SENT SUCCESSFULLY"}
        return JSONResponse(status_code=status.HTTP_200_OK, content=response, media_type="application/json")
    except Exception as e:
        print("Error decoding JSON:", e)
        response={"status":"ERROR","message":"ERROR OCCURRED"}
        return JSONResponse(status_code=status.HTTP_200_OK, content=response, media_type="application/json")
    