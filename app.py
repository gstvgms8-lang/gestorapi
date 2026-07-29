import time
from typing import Any

import pymssql
from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI(
    title="Teste de conexão Gestor",
    version="1.0.0",
)

GESTOR_HOST = "sistema.atdata.com.br"
GESTOR_PORT = "35987"
GESTOR_DATABASE = "MASTER_PRD"
GESTOR_USER = "MasterLog"
GESTOR_PASSWORD = "Master1252@#"
GESTOR_LOGIN_TIMEOUT = 10
GESTOR_QUERY_TIMEOUT = 10


def _configuracao_gestor() -> dict[str, Any]:
    return {
        "server": GESTOR_HOST,
        "port": GESTOR_PORT,
        "database": GESTOR_DATABASE,
        "user": GESTOR_USER,
        "password": GESTOR_PASSWORD,
        "login_timeout": GESTOR_LOGIN_TIMEOUT,
        "timeout": GESTOR_QUERY_TIMEOUT,
        "charset": "UTF-8",
        "autocommit": True,
        "read_only": True,
        "appname": "Vercel-Gestor-Teste",
    }


def _valor_json(valor: Any) -> Any:
    if hasattr(valor, "isoformat"):
        return valor.isoformat()
    return valor


@app.get("/")
def inicio():
    return {
        "status": "ok",
        "mensagem": "API de teste do Gestor iniciada.",
        "proximo_teste": "/teste-gestor",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/teste-gestor")
def testar_conexao_gestor():
    inicio_teste = time.perf_counter()
    conexao = None
    cursor = None

    try:
        configuracao = _configuracao_gestor()

        conexao = pymssql.connect(**configuracao)
        cursor = conexao.cursor(as_dict=True)
        cursor.execute(
            """
            SELECT
                DB_NAME() AS banco,
                @@SERVERNAME AS servidor,
                GETDATE() AS data_servidor
            """
        )
        resultado = cursor.fetchone() or {}
        latencia_ms = round(
            (time.perf_counter() - inicio_teste) * 1000,
            2,
        )

        return {
            "status": "ok",
            "mensagem": "Vercel conectou ao Gestor com sucesso.",
            "latencia_ms": latencia_ms,
            "banco": _valor_json(resultado.get("banco")),
            "servidor": _valor_json(resultado.get("servidor")),
            "data_servidor": _valor_json(
                resultado.get("data_servidor")
            ),
        }

    except Exception as erro:
        latencia_ms = round(
            (time.perf_counter() - inicio_teste) * 1000,
            2,
        )
        return JSONResponse(
            status_code=503,
            content={
                "status": "erro",
                "mensagem": (
                    "A função iniciou, mas não conseguiu conectar "
                    "ao Gestor."
                ),
                "tipo": type(erro).__name__,
                "detalhe": str(erro),
                "latencia_ms": latencia_ms,
            },
        )

    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass

        try:
            if conexao:
                conexao.close()
        except Exception:
            pass
