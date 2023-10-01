from fastapi.datastructures import QueryParams
from sqlmodel import Session
from database.dao.games_dao import GamesDAO

from database.models.game import Game
from database.schemas.game import GameSchema


class GameService:

    @staticmethod
    def get_all_games(limit: int, db: Session) -> list[GameSchema]:
        """
        Retrieve a list of all games with an optional limit.

        This method retrieves a list of all games from the database, limited by the specified `limit`.

        Parameters:
        - `limit` (int): The maximum number of games to retrieve (default is 20).

        Returns:
        - list[GameSchema]: A list of game objects.

        Raises:
        - ValueError: If the provided `limit` is greater than 50.
        """
        if limit > 50:
            raise ValueError('Limit too high!')
        
        return GamesDAO.get_all_games(limit, db)
    
    @staticmethod
    def get_games_using_filter(params: QueryParams, db: Session) -> list[GameSchema]:
        """
        Retrieve a list of games based on filtering parameters.

        This method retrieves a list of games from the database based on the provided filtering parameters.

        Parameters:
        - `params` (QueryParams): Query parameters for filtering.

        Returns:
        - list[GameSchema]: A list of game objects.

        Raises:
        - ValueError: If the provided filtering parameters do not match supported parameters.
        """
        filters = {}

        for key, value in params.items():
            if getattr(Game, key):
                filters[key] = value

        if not filters:
            raise ValueError('Provided parameters do not match the supported parameters.')

        game_data = GameSchema(**filters)

        return GamesDAO.get_games_using_filter(game_data, db)
    
    @staticmethod
    def insert_new_game(game: GameSchema, db: Session) -> GameSchema:
        """
        Insert a new game into the database.

        This method inserts a new game into the database.

        Parameters:
        - `game` (GameSchema): The game object to be inserted.

        Returns:
        - GameSchema: The inserted game object.

        Raises:
        - ValueError: If the game with the same name already exists in the database.
        """
        game_in_db = GamesDAO.get_game_by_name(game.name, db)
        
        if game_in_db:
            raise ValueError('Game already in database.')
    
        game_model = Game(**game.dict())
        game_model.appid = None
        added_game = GamesDAO.insert_new_game(game_model, db)

        return GameSchema(**added_game.dict())
    
    @staticmethod
    def update_game(game: GameSchema, db: Session) -> None:
        """
        Update an existing game in the database.

        This method updates an existing game in the database.

        Parameters:
        - `game` (GameSchema): The game object with updated data.

        Raises:
        - ValueError: If the game with the same name does not exist in the database.
        """
        game_in_db = GamesDAO.get_game_by_name(game.name, db)

        if not game_in_db:
            raise ValueError('Game not in database.')
        
        game_dict = Game(**game.dict()).dict()
        del game_dict['appid']
        
        for key, value in game_dict.items():
            setattr(game_in_db, key, value)

        GamesDAO.insert_new_game(game_in_db, db)
    
    @staticmethod
    def delete_game(game_name: str, db: Session) -> GameSchema:
        """
        Delete a game by name from the database.

        This method deletes a game from the database based on its name.

        Parameters:
        - `game_name` (str): The name of the game to be deleted.

        Returns:
        - GameSchema: The deleted game object.

        Raises:
        - ValueError: If the game with the specified name does not exist in the database.
        """
        game_in_db = GamesDAO.get_game_by_name(game_name, db)

        if not game_in_db:
            raise ValueError('Game not in database.')
        
        deleted_game = GamesDAO.delete_game(game_in_db, db)

        return GameSchema(**deleted_game.dict())
