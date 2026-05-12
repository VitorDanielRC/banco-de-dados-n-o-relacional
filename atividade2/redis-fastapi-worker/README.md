# Redis + FastAPI + Worker Queue

Projeto desenvolvido utilizando **FastAPI + Redis + Docker**, implementando:

* Cache com TTL
* Fila Producer/Consumer
* Worker em background
* Contador de requisições
* Rate Limiting por IP
* Docker Compose com múltiplos serviços

---

# Tecnologias Utilizadas

* FastAPI
* Redis
* Docker
* Python 3.12

---

# Estrutura do Projeto

```txt
redis-fastapi-worker/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
│
└── app/
    ├── main.py
    └── worker.py
```

---

# Fase 01 — Ambiente Docker

O projeto possui três serviços funcionando em rede compartilhada:

| Serviço | Função             |
| ------- | ------------------ |
| Redis   | Banco em memória   |
| API     | Aplicação FastAPI  |
| Worker  | Consumidor da fila |

---

# Como Executar

## 1. Clonar o projeto

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
```

## 2. Entrar na pasta

```bash
cd redis-fastapi-worker
```

## 3. Subir containers

```bash
docker compose up --build
```

---

# Serviços Disponíveis

| Serviço | URL                                                      |
| ------- | -------------------------------------------------------- |
| API     | [http://localhost:8000](http://localhost:8000)           |
| Swagger | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Redis   | localhost:6379                                           |

---

# Fase 02 — Cache com Redis

Endpoint:

```http
GET /dados
```

## Funcionamento

* Primeira requisição:

  * Processamento lento simulado
  * Redis armazena resultado por 30 segundos
  * Header:

```txt
X-Cache: MISS
```

* Próximas requisições:

  * Dados retornados do Redis
  * Header:

```txt
X-Cache: HIT
```

## Teste

```bash
curl -i http://localhost:8000/dados
```

---

# Fase 03 — Fila Producer/Consumer

## Producer

A API envia pedidos para a fila Redis usando:

```python
LPUSH
```

Endpoint:

```http
POST /pedidos
```

Exemplo:

```bash
curl -X POST http://localhost:8000/pedidos \
-H "Content-Type: application/json" \
-d "{\"cliente\":\"Vitor\",\"produto\":\"Notebook\",\"quantidade\":1}"
```

---

## Consumer

O Worker consome pedidos usando:

```python
BRPOP
```

Processando pedidos em background.

Logs esperados:

```txt
Pedido recebido da fila
Pedido processado com sucesso
```

---

# Fase 04 — Contador + Rate Limit

## Contador de requisições

Endpoint:

```http
GET /contador
```

Utiliza:

```python
INCR
```

para contabilizar acessos.

---

## Rate Limiting por IP

Endpoint:

```http
GET /protegido
```

Regras:

* Máximo de 10 requisições
* Janela de 60 segundos
* Controle baseado no IP

Erro retornado:

```json
{
  "detail": "Limite de requisições excedido. Tente novamente depois."
}
```

Status HTTP:

```txt
429 Too Many Requests
```

---

# Comandos Docker

## Subir aplicação

```bash
docker compose up --build
```

## Derrubar containers

```bash
docker compose down
```

## Ver logs

```bash
docker compose logs -f
```

## Ver logs do worker

```bash
docker compose logs -f worker
```

---

# Principais Estruturas Redis Utilizadas

| Estrutura | Uso        |
| --------- | ---------- |
| String    | Cache      |
| List      | Fila       |
| Counter   | Contador   |
| TTL       | Expiração  |
| INCR      | Rate Limit |

---

# Conceitos Aplicados

* Microsserviços
* Containerização
* Cache distribuído
* Filas assíncronas
* Processamento em background
* Controle de concorrência
* Rate limiting
* Producer/Consumer

---

# Autor

**Vitor Daniel**

* GitHub: [VitorDanielRC GitHub](https://github.com/VitorDanielRC?utm_source=chatgpt.com)
* Curso: Engenharia de Software

---

# Resultado Esperado

✔ Docker funcionando
✔ Redis integrado
✔ FastAPI funcionando
✔ Cache com TTL
✔ Worker processando fila
✔ Contador de requisições
✔ Rate limiting por IP
✔ Projeto publicado no GitHub
