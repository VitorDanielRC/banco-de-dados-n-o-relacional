import json
import time
import redis

r = redis.Redis(
    host="redis",
    port=6379,
    db=0,
    decode_responses=True
)

print("Worker iniciado. Aguardando pedidos...")

while True:
    item = r.brpop("fila:pedidos")

    fila, pedido_json = item
    pedido = json.loads(pedido_json)

    print(f"Pedido recebido da fila: {pedido}")

    time.sleep(3)

    print(f"Pedido processado com sucesso: {pedido}")