import uvicorn
from fastapi import FastAPI

# Import Routers
from app.rtve import router as rtve_router
from app.monitoring import router as monitoring_router
from app.teams import router as teams_router


app = FastAPI(
    title="AGGREGATOR",
    description="Prueba de Routers",
)


@app.get("/")
def read_root():
    return {"message": "Hello World!"}


app.include_router(monitoring_router.router)
app.include_router(rtve_router.router)
app.include_router(teams_router.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
