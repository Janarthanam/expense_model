#!/usr/bin/env python3
from fastapi import FastAPI
from routes import gpt3,regex
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from uvicorn.logging import DefaultFormatter
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(DefaultFormatter())
logger.addHandler(handler)

# Create the FastAPI instance
app = FastAPI()
app.include_router(regex.router)
app.include_router(gpt3.router)

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    process_time = (datetime.utcnow() - start_time).total_seconds() * 1000
    print(
        f"{request.method} {request.url.path} {response.status_code} {process_time:.2f}ms"
    )
    return response
