from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "IMU API is running"}

@app.post("/imu")
async def receive_imu(request: Request):
    data = await request.json()
    print("📥 Received IMU Data:", data)
    return {"status": "received"}


#test
#test