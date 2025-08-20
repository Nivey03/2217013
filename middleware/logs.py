import requests
from dotenv import load_dotenv
import os

load_dotenv() 
TOKEN = os.getenv("MY_SECRET_TOKEN")

Stack = {
    "backend",
    "frontend"
}

Level = {
    "debug",
    "info",
    "warning",
    "error",
    "fatal"
}

Package = {
    "cache",
    "controller",
    "cron_job",
    "db",
    "domain",
    "handler",
    "repository",
    "route",
    "service"
}


def send_log(stack, level, package, message):
    url = "http://20.244.56.144/evaluation-service/logs"
    payload = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message
    }
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    
    try:
        requests.post(url, json=payload, headers=headers, timeout=2)
    except Exception as e:
        print(f"Log failed: {e}")

