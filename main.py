from app.services.fetch_rtve_data import fetch_programs



for i in range(2):
    # fetch_programs(MAX_PAGE_SIZE, i)
    fetch_programs(1, i)