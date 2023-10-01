from fastapi.datastructures import QueryParams
from sqlmodel import Session
from database.dao.games_dao import GamesDAO

from database.models.game import Game
from database.schemas.game import GameSchema


class GameService:

    def get_all_games(limit: int, db: Session) -> list[GameSchema]:
        if limit > 50:
            raise ValueError('Limit too high!')
        
        return GamesDAO.get_all_games(limit, db)
    
    def get_games_using_filter(params: QueryParams, db: Session) -> list[GameSchema]:
        filters = {}

        for key, value in params.items():
            if getattr(Game, key):
                filters[key] = value

        if not filters:
            raise ValueError('Provided parameters do not match the supported parameters.')

        game_data = GameSchema(**filters)

        return GamesDAO.get_games_using_filter(game_data, db)
    
    def insert_new_game(game: GameSchema, db: Session) -> GameSchema:
        game_in_db = GamesDAO.get_game_by_name(game.name, db)
        
        if game_in_db:
            raise ValueError('Game already in database.')
    
        game_model = Game(**game.dict())
        added_game = GamesDAO.insert_new_game(game_model, db)

        return GameSchema(**added_game.dict())
    
    # def update_game