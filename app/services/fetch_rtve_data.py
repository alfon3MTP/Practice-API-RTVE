import requests

RTVE_API_URL = "https://www.rtve.es/api/"
MAX_PAGE_SIZE = 60 

from app.models import TVProgram

#https://www.rtve.es/api/agr-programas.json?size=60&?page=2
def fetch_programs(size: int,  page: int):
    
    endpoint = "programas.json"
    url_filters = f"?size={MAX_PAGE_SIZE}&?page={page}"
    
    url = f"{RTVE_API_URL}{endpoint}{url_filters}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    programs_data = data.get("page", {}).get("items", [])
    
    programs = []
    for program_data in programs_data:
        # Create a TVProgram object from the data
        program = TVProgram(**program_data)
        programs.append(program)
    
        print(program)
    

for i in range(2):
    # fetch_programs(MAX_PAGE_SIZE, i)
    fetch_programs(1, i)