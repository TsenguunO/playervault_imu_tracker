from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, Float
from collections import deque
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

class IMUData(Base):
    __tablename__ = "imu_data"

    id = Column(Integer, primary_key=True, index=True)
    seq = Column(Integer)
    ax = Column(Float)
    ay = Column(Float)
    az = Column(Float)
    gx = Column(Float)
    gy = Column(Float)
    gz = Column(Float)

app = FastAPI()
imu_log = deque(maxlen=100)

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def health_check():
    return {"status": "IMU API running with log-html"}
#
@app.post("/imu")
async def receive_imu(request: Request):
    data = await request.json()
    imu_log.append(data)

    async with SessionLocal() as session:
        imu = IMUData(**data)
        session.add(imu)
        await session.commit()

    return {"status": "received"}

@app.get("/log")
async def get_log():
    return list(imu_log)[-10:]




@app.get("/log-html", response_class=HTMLResponse)
def get_log_html():
    rows = reversed(list(imu_log)[-10:])
    html = "<h2>Latest IMU Data</h2><table border=1><tr><th>Seq</th><th>ax</th><th>ay</th><th>az</th><th>gx</th><th>gy</th><th>gz</th></tr>"
    for d in rows:
        html += f"<tr><td>{d['seq']}</td><td>{d['ax']:.3f}</td><td>{d['ay']:.3f}</td><td>{d['az']:.3f}</td><td>{d['gx']:.3f}</td><td>{d['gy']:.3f}</td><td>{d['gz']:.3f}</td></tr>"
    html += "</table>"
    return html
