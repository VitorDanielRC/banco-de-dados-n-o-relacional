import time
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import redis

app = FastAPI()

r = redis.Redis(
    host="redis",
    port=6379,
    db=0,
    decode_responses=True
)

CACHE_TTL = 30
RATE_LIMIT = 10
RATE_LIMIT_TTL = 60


@app.get("/")
def home():
    return {
        "mensagem": "API FastAPI com Redis, Cache, Fila, Contador e Rate Limit"
    }


@app.get("/dados")
def dados():
    cache_key = "cache:dados"

    cached = r.get(cache_key)

    if cached:
        return JSONResponse(
            content=json.loads(cached),
            headers={"X-Cache": "HIT"}
        )

    time.sleep(2)

    data = {
        "mensagem": "Dados gerados pela API",
        "origem": "processamento pesado",
        "tempo_simulado": "2 segundos"
    }

    r.setex(cache_key, CACHE_TTL, json.dumps(data))

    return JSONResponse(
        content=data,
        headers={"X-Cache": "MISS"}
    )


@app.post("/pedidos")
def criar_pedido(pedido: dict):
    r.lpush("fila:pedidos", json.dumps(pedido))

    return {
        "mensagem": "Pedido enviado para a fila",
        "pedido": pedido
    }


@app.get("/contador")
def contador():
    total = r.incr("contador:requisicoes")

    return {
        "total_requisicoes": total
    }


@app.get("/protegido")
def protegido(request: Request):
    ip = request.client.host
    key = f"rate_limit:{ip}"

    requests_count = r.incr(key)

    if requests_count == 1:
        r.expire(key, RATE_LIMIT_TTL)

    if requests_count > RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Limite de requisições excedido. Tente novamente depois."
        )

    return {
        "mensagem": "Acesso permitido",
        "ip": ip,
        "requisicoes": requests_count,
        "limite": RATE_LIMIT
    }