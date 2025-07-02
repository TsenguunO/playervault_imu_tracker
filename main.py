from fastapi import FastAPI, Request
from collections import deque

app = FastAPI()
imu_log = deque(maxlen=100)  # store last 100 packets

@app.get("/")
def health_check():
    return {"status": "IMU API is running"}

@app.post("/imu")
async def receive_imu(request: Request):
    data = await request.json()
    print("📥 Received IMU Data:", data)
    imu_log.append(data)
    return {"status": "received"}

@app.get("/log")
def get_log():
    return list(imu_log)[-10:]  # return last 10 packets
