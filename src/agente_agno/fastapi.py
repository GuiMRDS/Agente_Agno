# Conta Corrente Bancária - FastApi

from fastapi import FastAPI
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
    return {"message": f"Saldo do Cliente {cliente} é {db_client[cliente]}"}

@app.post("/saque")
def saque(movimentacao: Movimentacao):
   db_client[movimentacao.cliente] -= movimentacao.valor
   return {"message": f"Cliente: {movimentacao.cliente}, valor_movimentação {db_client[movimentacao.cliente]}",
           "saldo": {db_client[movimentacao.cliente]}}

@app.post("/deposito")
def deposito(movimentacao: Movimentacao):
    db_client[movimentacao.cliente] += movimentacao.valor
    return {"message": f"Cliente: {movimentacao.cliente}, valor_movimentação {db_client[movimentacao.cliente]}",
            "saldo": {db_client[movimentacao.cliente]}}


if __name__ == "__main__":
    uvicorn.run("exemplo2:app", host="0.0.0.0", port=8000, reload=True)