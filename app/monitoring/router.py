import psutil
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/monitor",
    tags=["System Monitor"]
)

# TODO: Add async/await calls

@router.get("/cpu")
def get_cpu_usage():
    usage = psutil.cpu_percent(interval=1, percpu=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {"cpu_usage_history": {"timestamp": timestamp, "usage": usage}}

@router.get("/memory")
def get_memory_usage():
    mem = psutil.virtual_memory()
    usage = mem.percent
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {"memory_usage_history": {"timestamp": timestamp, "usage": usage}}

@router.get("/disk")
def get_disk_usage():
    disk = psutil.disk_usage('/')
    usage = disk.percent
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {"disk_usage_history": {"timestamp": timestamp, "usage": usage}}


