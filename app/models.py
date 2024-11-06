from pydantic import BaseModel
from typing import List
from datetime import datetime

class Program(BaseModel):
    id: int
    title: str