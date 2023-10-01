from sqlalchemy import func, or_
from sqlmodel import Session
from database.models.game import Game
from database.schemas.game import GameSchema


class GamesDAO:

    @staticmethod
    def get_all_games(limit: int, db: Session) -> list[GameSchema]:
        return db.query(Game).limit(limit).all()
    
    @staticmethod
    def get_games_using_filter(game_data: GameSchema, db: Session) -> list[GameSchema]:
        filter_query = lambda key, value : getattr(Game, key).ilike(f'%{value.lower()}%') if type(value) is str else getattr(Game, key) == value
        query = db.query(Game)
        game_data_dict = game_data.dict()

        for key, value in game_data_dict.items():
            if not value:
                continue

            if type(value) == list:
                filter_list = []
                for v in value:
                    filter_list.append(filter_query(key, v))
                query = query.filter(or_(*filter_list))
                continue
            
            query = query.filter(filter_query(key, value))

        return query.limit(20).all()  

    @staticmethod
    def get_game_by_name(name: str, db: Session) -> Game:
        return db.query(Game).filter(func.lower(Game.name) == name.lower()).one_or_none()

    @staticmethod
    def insert_new_game(game: Game, db: Session) -> Game:
        game.appid = None

        db.add(game)
        db.commit()

        return game