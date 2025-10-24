#!/bin/bash
cd /Users/ayush/Downloads/Discord-clone/backend
/Users/ayush/Downloads/Discord-clone/backend/venv/bin/python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
