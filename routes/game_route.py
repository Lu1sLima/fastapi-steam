from fastapi import Depends, HTTPException, Request
from sqlmodel import Session
from database.database import get_db
from database.models.game import Game
from database.schemas.game import GameSchema
from services.game_service import GameService

from fastapi import APIRouter, Depends, HTTPException

game_router = APIRouter(
    prefix="/games",
    tags=["Games"],
    responses={404: {"description": "Not found"}},
)

@game_router.get("/", response_model=list[GameSchema])
def get_all_games(limit: int = 20, db: Session = Depends(get_db)) -> list[Game]:
    try:
        return GameService.get_all_games(limit, db)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except Exception as error:
        raise HTTPException(status_code=500, detail="Error while trying to get games.") from error
    

@game_router.get("", response_model=list[GameSchema])
def get_game(request: Request, appid: int = None, name: str = None, developer: str = None, publisher: str = None, 
             platforms: str = None, required_age: str = None, steamspy_tags: str = None, categories: str = None, 
             genres: str = None, achievements: bool = True, positive_ratings: int = None, negative_ratings: int = None,
             average_playtime: float = None, median_playtime: float = None, owners: str = None, 
             price: float = None, db: Session = Depends(get_db)) -> list[Game]:
    try:
        return GameService.get_games_using_filter(request.query_params, db)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except Exception as error:
        raise HTTPException(status_code=500, detail="Error while trying to get games with parameters.") from error


@game_router.post("", response_model=GameSchema)
def insert_new_game(game: GameSchema, db: Session = Depends(get_db)) -> GameSchema:
    try:
        return GameService.insert_new_game(game, db)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str("Error while trying to insert game.")) from ex
    
@game_router.put("/", status_code=204)
def update_game(game: GameSchema, db: Session = Depends(get_db)) -> None:
    pass