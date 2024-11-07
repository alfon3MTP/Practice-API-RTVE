from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/rtve",
    tags=["RTVE API"]
)


@router.get("/ping")
def ping_rtve():

    return {"message": "Welcome to RTVE Router"}