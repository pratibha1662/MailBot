from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


healthcheck_router=APIRouter() 
@healthcheck_router.get("/healthcheck",operation_id="healthcheck")
async def healthcheck():
    response={"status":"ok"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=response, media_type="application/json")