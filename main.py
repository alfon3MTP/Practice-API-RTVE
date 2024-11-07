from app.services.fetch_rtve_data import fetch_programs
from app.db import init_db, engine

init_db()

for i in range(80):
    # fetch_programs(MAX_PAGE_SIZE, i)
    fetch_programs(60, i, engine)