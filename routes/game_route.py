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
    """
    Get a list of all games.

    This route allows you to retrieve a list of all games from the database.
    
    Parameters:
    - `limit` (optional): The maximum number of games to retrieve (default is 20, maximum is 50).
    
    Responses:
    - 200 OK: Returns a list of game objects.
    - 400 Bad Request: If there is a validation error.
    - 500 Internal Server Error: If there is a server error.
    """
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
    """
    Get games with filtering options.

    This route allows you to retrieve a list of games from the database with various filtering options.

    Parameters:
    - All parameters are optional and can be used to filter games based on specific criteria.

    Responses:
    - 200 OK: Returns a list of game objects based on the specified filters.
    - 400 Bad Request: If there is a validation error.
    - 500 Internal Server Error: If there is a server error.
    """
    try:
        return GameService.get_games_using_filter(request.query_params, db)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except Exception as error:
        raise HTTPException(status_code=500, detail="Error while trying to get games with parameters.") from error


@game_router.post("", response_model=GameSchema)
def insert_new_game(game: GameSchema, db: Session = Depends(get_db)) -> GameSchema:
    """
    Insert a new game.

    This route allows you to insert a new game into the database.

    Parameters:
    - `game` (request body): The game object to be inserted.

    Responses:
    - 201 Created: Returns the inserted game object.
    - 400 Bad Request: If there is a validation error.
    - 500 Internal Server Error: If there is a server error.
    """
    try:
        return GameService.insert_new_game(game, db)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str("Error while trying to insert game.")) from ex
    
@game_router.put("/", status_code=204)
def update_game(game: GameSchema, db: Session = Depends(get_db)) -> None:
    """
    Update an existing game.

    This route allows you to update an existing game in the database.

    Parameters:
    - `game` (request body): The game object with updated data.

    Responses:
    - 204 No Content: Indicates the update was successful.
    - 404 Not Found: If game not in database.
    - 500 Internal Server Error: If there is a server error.
    """
    try:
        GameService.update_game(game, db)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve)) from ve
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str("Error while trying to update game.")) from ex
    
        
@game_router.delete("/{game_name}", response_model=GameSchema)
def delete_game(game_name: str, db: Session = Depends(get_db)) -> GameSchema:
    """
    Delete a game by name.

    This route allows you to delete a game from the database by its name.

    Parameters:
    - `game_name` (path parameter): The name of the game to be deleted.

    Responses:
    - 200 OK: Returns the deleted game object.
    - 404 Not found: If game not in database.
    - 500 Internal Server Error: If there is a server error.
    """
    try:
        return GameService.delete_game(game_name, db)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve)) from ve
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str("Error while trying to delete game.")) from ex
