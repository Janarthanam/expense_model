#!/usr/bin/env python3
from fastapi import FastAPI
from routes import gpt3,regex,bulk_extract,static
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from uvicorn.logging import DefaultFormatter
import logging
import uvicorn

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(DefaultFormatter())
logger.addHandler(handler)

# Create the FastAPI instance
app = FastAPI()
app.include_router(regex.router)
app.include_router(gpt3.router)
app.include_router(bulk_extract.router)
app.include_router(static.router)

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    process_time = (datetime.utcnow() - start_time).total_seconds() * 1000
    print(
        f"{request.method} {request.url.path} {response.status_code} {process_time:.2f}ms"
    )
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
