import os
import json
import time


from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse 
import redis

app = FastAPI(
    title="Atividade Redis + Python",
    description="API de exemplo com cache e fila usando Redis",
    version="1.0.0",
)

r = redis.from_url(os.environ["REDIS_URL"], decode_response=True)

@app.get("/produtos/{pid}", summary="Buscar Produto(cache)")

def get_produto(pid: int, request: Request = None):
    key = f"produto:{pid}"
    cached = r.get(key)

    if cached: data = json.loads(cached)
    return JSONResponse(content={"data": data, "cache": "HIT"}, headers={"X-Cache": "HIT"})

time.sleep(2)
data = {"id": pid, "nome": f"Produto {pid}", "preco": round(pid * 9.9, 2)}

r.setex(key, 30, json.dumps(data))
r.hincrby("stats:endpoints","/produtos",1)

return JSONResponse(content={"data": data, "cache": "MISS"},
                    headers={"X-Cache":"MISS"})