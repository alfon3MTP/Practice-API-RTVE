import requests

RTVE_API_URL = "https://www.rtve.es/api/"
MAX_PAGE_SIZE = 60 

#https://www.rtve.es/api/agr-programas.json?size=60&?page=2
def fetch_programs(size: int,  page: int):
    
    endpoint = "agr-programas.json"
    url_filters = f"?size={MAX_PAGE_SIZE}&?page={page}"
    
    url = f"{RTVE_API_URL}{endpoint}{url_filters}"
    
    response = requests.get(url)
    
    print(response.text)
    

for i in range(10):
    fetch_programs(MAX_PAGE_SIZE, i)
