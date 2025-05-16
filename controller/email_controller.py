from typing import Optional, Mapping
from fastapi import APIRouter, Request, status, File, Form, UploadFile
from fastapi.responses import JSONResponse
from services import email_service, oauth_service
import json
from infrastructure.langgraph_agent import workflow
from langchain_core.messages import HumanMessage

email_router=APIRouter()
@email_router.post("/send_email",operation_id="send_email")
async def send_email(
    file: UploadFile = File(...),
    subject: str = Form(...),
    body: str = Form(...),
    creds: Optional[str] = Form(...)
):
    try:
        mapping = None
        file_content = await file.read()
        email_addresses = file_content.decode("utf-8").splitlines() 
        email_addresses = [email.strip() for email in email_addresses if email.strip()]
        if creds:
            creds_data = json.loads(creds)

            # Ensure all values are strings
            mapping: Mapping[str, str] = {key: str(value) for key, value in creds_data.items()}
        creds = oauth_service.get_oauth_creds(mapping)
        send_email = email_service.send_gmail(creds, email_addresses, subject, body)
        response={"status":"SUCCESS","message":"EMAIL SENT SUCCESSFULLY", "creds":creds.to_json()}
        return JSONResponse(status_code=status.HTTP_200_OK, content=response, media_type="application/json")
    except Exception as e:
        print("Error decoding JSON:", e)
        response={"status":"ERROR","message":"ERROR OCCURRED", "detail": str(e)}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response, media_type="application/json")
    
@email_router.post("/generate_message",operation_id="generate_message")
async def generate_message(
    request: Request
): 
    try: 
        body = await request.json()
        user_message = body.get("user_message")
        user_query = HumanMessage(content = user_message)
        output = workflow.invoke({"messages" : [user_query]})
        raw_output_content = output["messages"][-1].content
        parsed_output = raw_output_content.strip().lstrip("```json").rstrip("```").strip()
        response ={"status":"SUCCESS", "content" : json.loads(parsed_output)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=response, media_type="application/json")
    except Exception as e:
        print("Error decoding JSON:", e)
        response={"status":"ERROR","message":"ERROR OCCURRED", "detail": str(e)}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response, media_type="application/json")
    