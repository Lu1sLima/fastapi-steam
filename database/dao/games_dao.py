from sqlalchemy import func, or_
from sqlmodel import Session
from database.models.game import Game
from database.schemas.game import GameSchema

class GamesDAO:

    @staticmethod
    def get_all_games(limit: int, db: Session) -> list[GameSchema]:
        """
        Retrieve a list of games with a limit.

        This method retrieves a list of games from the database with a specified limit.

        Parameters:
        - `limit` (int): The maximum number of games to retrieve.

        Returns:
        - list[GameSchema]: A list of game objects.

        """
        return db.query(Game).limit(limit).all()
    
    @staticmethod
    def get_games_using_filter(game_data: GameSchema, db: Session) -> list[GameSchema]:
        """
        Retrieve a list of games based on filtering criteria.

        This method retrieves a list of games from the database based on the provided filtering criteria.

        Parameters:
        - `game_data` (GameSchema): The filtering criteria as a GameSchema object.

        Returns:
        - list[GameSchema]: A list of game objects that match the filtering criteria.

        """
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
        """
        Retrieve a game by its name.

        This method retrieves a game from the database by its name.

        Parameters:
        - `name` (str): The name of the game to retrieve.

        Returns:
        - Game: The game object.

        """
        return db.query(Game).filter(func.lower(Game.name) == name.lower()).one_or_none()

    @staticmethod
    def insert_new_game(game: Game, db: Session) -> Game:
        """
        Insert a new game into the database.

        This method inserts a new game into the database.

        Parameters:
        - `game` (Game): The game object to be inserted.

        Returns:
        - Game: The inserted game object.

        """
        db.add(game)
        db.commit()
        return game
    
    @staticmethod
    def delete_game(game: Game, db: Session) -> Game:
        """
        Delete a game from the database.

        This method deletes a game from the database.

        Parameters:
        - `game` (Game): The game object to be deleted.

        Returns:
        - Game: The deleted game object.

        """
        db.delete(game)
        db.commit()
        return game
