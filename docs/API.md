# API Reference – WindSurf Adapter

FastAPI service located at `scripts/windsurf_adapter.py` exposes secure endpoints for WindSurf agents or any HTTP client.

| Method | Path        | Description                             |
|--------|-------------|-----------------------------------------|
| POST   | `/monitor`  | Executa `monitor.py` e retorna stdout/err e código de retorno. |
| POST   | `/rotate`   | Executa `rotate_personas.py` (verifica rotações). |
| POST   | `/report`   | Executa `generate_report.py` e devolve relatório. |

## Execução local

```bash
uvicorn scripts.windsurf_adapter:app --reload --port 8080
```

A documentação interativa (Swagger UI) ficará disponível em `http://localhost:8080/docs`.

## Esquemas de Resposta

```jsonc
{
  "return_code": 0,
  "stdout": "... saída do script ...",
  "stderr": ""  // vazio se sem erros
}
```

Em caso de erro de script, `return_code` será diferente de `0` e `stderr` trará detalhes.

## Autenticação / Segurança

Atualmente não há autenticação; recomenda-se colocar o Uvicorn atrás de um proxy autenticado ou VPN quando em produção.

## Exemplos de Chamada via `curl`

```bash
# Monitorar
curl -X POST http://localhost:8080/monitor | jq

# Forçar rotação
curl -X POST http://localhost:8080/rotate -d '{"force": true}' -H "Content-Type: application/json"
```

Consulte `.windsurf/rules.mdc` para ver as políticas que regem esses endpoints quando invocados por agentes WindSurf.
