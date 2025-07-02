from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/imu")
async def receive_imu(request: Request):
    data = await request.json()
    print(f"📦 Received IMU Data: {data}")
    return {"status": "received"}