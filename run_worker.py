#!/usr/bin/env python3
"""
RCA Platform Background Worker Startup Script
"""
import asyncio
import os
from dotenv import load_dotenv
from app.worker import RCAWorker

load_dotenv()

if __name__ == "__main__":
    print("🚀 Starting RCA Background Worker...")
    worker = RCAWorker()
    asyncio.run(worker.run_continuous()) 