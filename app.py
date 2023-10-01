from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from database.database import create_db_and_tables
from routes.game_route import game_router

description = '''
## Alunos

- Luís Lima
- Lucas Garcia

## Descrição

Este é um projeto que demonstra o uso do FastAPI para criar uma API para gerenciar informações sobre jogos da STEAM.
'''

app = FastAPI(description=description)

@app.get('/', include_in_schema=False)
def get_home():
    return RedirectResponse(url='/docs')

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(game_router)
