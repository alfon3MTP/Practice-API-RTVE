import uvicorn
from fastapi import FastAPI

# Import Routers
from app.routers import monitoring, rtve


app = FastAPI(
    title="AGGREGATOR",
    description="Prueb ade Routers",
)


@app.get("/")
def read_root():
    return {"message": "Hello World!"}


app.include_router(monitoring.router)
app.include_router(rtve.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
