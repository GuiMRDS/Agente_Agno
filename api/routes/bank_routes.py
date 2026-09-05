# Conta Corrente Bancária - FastApi

from bank_routes import FastAPI
import uvicorn
from pydantic import BaseModel, Field


app = FastAPI(title="Conta Corrente Bancária - FastApi")

db_client = {
    "Joao": 1000,
    "Maria": 20,
    "Pedro": 3,
}

class Movimentacao(BaseModel):
    cliente: str = Field(..., description="Nome do Cliente")
    valor: float = Field(..., gt=0, description="Valor da Movimentacao")

@app.get("/")
def read_root():
    return {"message": "Conta Corrente Bancária - FastApi"}

@app.post("/saldo")
def saldo(cliente: str):

    if cliente not in db_client:
        return {"erro": "Cliente não encontrado"}

    return {
        "cliente": cliente,
        "saldo": db_client[cliente]
    }

@app.post("/saque")
def saque(movimentacao: Movimentacao):
   db_client[movimentacao.cliente] -= movimentacao.valor
   return {
       "message": f"Cliente: {movimentacao.cliente}, valor_movimentação {db_client[movimentacao.cliente]}",
       "saldo": db_client[movimentacao.cliente]
   }

@app.post("/deposito")
def deposito(movimentacao: Movimentacao):
    db_client[movimentacao.cliente] += movimentacao.valor
    return {"message": f"Cliente: {movimentacao.cliente}, valor_movimentação {db_client[movimentacao.cliente]}",
            "saldo": db_client[movimentacao.cliente]
            }


uvicorn.run(
    "banco_api:app",
    host="0.0.0.0",
    port=8000,
    reload=True
)