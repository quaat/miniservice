#!/usr/bin/env bash
pip install -U -e /minicore/.
uvicorn asgi:app --reload --host 0.0.0.0 --port 5000