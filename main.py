from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

busy_data: Dict[str, List[List[str]]] = {}
# Dict[str,List[Dict[str,int,str,List[List[str]]]]]
booked_slots: List[List[str]] = []
# busy_data: Dict[str, List[List[str]]] = {}
WORK_START = "09:00"
WORK_END = "18:00"
TIME_FORMAT = "%H:%M"

def parse_time(t: str) -> datetime:
    return datetime.strptime(t, TIME_FORMAT)

def format_time(t: datetime) -> str:
    return t.strftime(TIME_FORMAT)

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/slots")
async def save_slots(payload: Dict[str,List[Dict]]):
    # print(payload)
    # global busy_data,booked_slots
    busy_data.clear()
    booked_slots.clear()
    payload = payload['users']
    for user in payload:
        busy_data[str(user["id"])] = user["busy"]
    return {"message": "Slots saved successfully."}

@app.get("/suggest")
def suggest_slots(duration: int):
    all_busy = []
    # print(busy_data)
    for slots in busy_data.values():
        all_busy.extend(slots)
        
    #  to include later booked intervals
    all_busy.extend(booked_slots)
    
    busy = sorted([(parse_time(s), parse_time(e)) for s, e in all_busy], key=lambda x: x[0])
    # print(busy)
    merged = []
    for start, end in busy:
        # print(start,end)
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    # print(merged)
    free_slots = []
    # start and end time in datetime format
    work_start = parse_time(WORK_START)
    work_end = parse_time(WORK_END)
    duration = timedelta(minutes=duration)
    cur = work_start
    for start, end in merged:
        if cur + duration <= start:
            free_slots.append([cur, start])
        cur = max(cur, end)
    if cur + duration <= work_end:
        free_slots.append([cur, work_end])
    
    # print(free_slots)
    thr_freeslots =[]
    for start,end in free_slots:
        thr_freeslots.append([format_time(start), format_time(end)])
    print(thr_freeslots)
    return thr_freeslots
    

@app.get("/calendar/{user_id}")
async def calendar(user_id: str):
    # slots = busy_data.get(user_id, []) + booked_slots
    # print(busy_data)
    # print(str(user_id))
    slots = busy_data.get(user_id,[])
    # slots = busy_data[user_id]
    print(slots)
    print(booked_slots)
    # print(slots)
    return {"slots":slots,"booked_slots":booked_slots}

@app.post("/book")
async def book_slot(slot_bk: Dict):
    # print(slot_bk)
    start, end = slot_bk["slot"]
    duration = int(slot_bk["duration"])
    # for id in booked_slots:
    #     print(id)
    work_start = parse_time(start)
    work_end = parse_time(end)
    duration = timedelta(minutes=duration)
    t_slot = [format_time(work_start),format_time(work_start+duration)]
    
    # print(t_slot)
        
    # as same for all usrs so not editing the main schedule
    # global booked_slots 
    booked_slots.append(t_slot)
    # print(booked_slots)
    return {"message": "Slot booked successfully."}
