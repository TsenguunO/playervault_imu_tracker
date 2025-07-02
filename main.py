from fastapi import FastAPI, Request

app = FastAPI()

received_data = []

@app.get("/")
def health_check():
    return {"status": "IMU API is running"}

@app.post("/imu")
async def receive_imu(request: Request):
    data = await request.json()
    print("📥 Received IMU Data:", data)
    received_data.append(data)
    return {"status": "received"}

@app.get("/log")
def get_latest_data():
    return received_data[-10:]  # Show last 10 packets
