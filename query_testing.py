from app.rtve.models import TVProgram
from sqlmodel import select, func
from app.db import get_session_hc


session = get_session_hc()

result = session.exec(select(func.count()).select_from(TVProgram))
print("Num rows: ", result.one())







