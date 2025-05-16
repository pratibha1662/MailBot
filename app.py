from fastapi import FastAPI,APIRouter,status
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
from controller.healthcheck_controller import healthcheck_router
from controller.email_controller import email_router


app=FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"])

app.include_router(healthcheck_router,prefix="/trs/api/email")

app.include_router(email_router,prefix="/trs/api/email")




if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
   