#!/usr/bin/env python3
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
static_dir = os.path.join(current_dir, "../static")

router = APIRouter()

# Mount static files
router.mount("/static", StaticFiles(directory=static_dir), name="static")
