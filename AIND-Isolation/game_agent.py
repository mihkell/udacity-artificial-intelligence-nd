"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
from isolation.isolation import Board

NEGATIVE_MOVE = (-1, -1)
INFINITY = float('inf')
NEG_INFINITY = float('-inf')


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


square_moves = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (0, 1), (1, 1)
]

second_moves_outside = [(-2, 0), (2, 0), (0, -2), (0, 2)]

second_moves = [square_moves[0], square_moves[2],
                square_moves[5], square_moves[7]]


def custom_score(game, player) -> float:
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return INFINITY
    if game.is_loser(player):
        return NEG_INFINITY

    player_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(player_moves - opponent_moves * 8)


def custom_score_2(game, player) -> float:
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    def future_open_move_locations(game, player):
        future_step_locations = []
        blank_spaces = game.get_blank_spaces()
        player_location = game.get_player_location(player)
        s_moves = []
        s_moves.extend(second_moves_outside)
        s_moves.extend(square_moves)
        for move in s_moves:
            location = tuple(map(sum, zip(player_location, move)))
            if location in blank_spaces:
                future_step_locations.append(location)
        return future_step_locations

    def future_open_move_locations_amount(game, player):
        return len(future_open_move_locations(game, player))

    if game.is_winner(player):
        return INFINITY
    if game.is_loser(player):
        return NEG_INFINITY

    player_moves_count = len(game.get_legal_moves(player))

    return float(player_moves_count + future_open_move_locations_amount(game, player))


def custom_score_3(game: Board, player) -> float:
    def future_open_move_locations(game, player):
        future_step_locations = []
        blank_spaces = game.get_blank_spaces()
        player_location = game.get_player_location(player)
        s_moves = []
        s_moves.extend(second_moves_outside)
        s_moves.extend(square_moves)
        for move in s_moves:
            location = tuple(map(sum, zip(player_location, move)))
            if location in blank_spaces:
                future_step_locations.append(location)
        return future_step_locations

    def future_open_move_locations_amount(game, player):
        return len(future_open_move_locations(game, player))
    if game.is_winner(player):
        return INFINITY
    if game.is_loser(player):
        return NEG_INFINITY

    future_step_locations_amount = future_open_move_locations_amount(game, player)

    player_moves_count = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(player_moves_count / 2 + future_step_locations_amount / 3 - opponent_moves / 2)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=15.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.current_best_move = NEGATIVE_MOVE


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game: Board, time_left: callable) -> tuple:
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            if self.current_best_move:
                best_move = self.current_best_move

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game: Board, depth: int) -> tuple:
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if game.is_loser(game.active_player):
            return NEGATIVE_MOVE

        legal_moves = game.get_legal_moves(game.active_player)

        self.current_best_move = NEGATIVE_MOVE
        max_val = NEG_INFINITY
        for next_move in legal_moves:
            new_max = self.min_value(game.forecast_move(next_move),
                                     depth - 1)
            if new_max >= max_val:
                max_val = new_max
                self.current_best_move = next_move

        return self.current_best_move

    def max_value(self, game: Board, depth: int) -> float:
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if game.is_loser(game.active_player):
            return NEG_INFINITY

        if depth <= 0:
            return self.score(game, game.active_player)

        legal_moves = game.get_legal_moves(game.active_player)
        move = NEG_INFINITY
        for next_move in legal_moves:
            move = max(move,
                       self.min_value(game.forecast_move(next_move), depth - 1))

        return move

    def min_value(self, game: Board, depth: int) -> float:
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if game.is_loser(game.active_player):
            return INFINITY

        if depth <= 0:
            return self.score(game, game.inactive_player)

        legal_moves = game.get_legal_moves(game.active_player)
        move = INFINITY
        for next_move in legal_moves:
            move = min(move,
                       self.max_value(game.forecast_move(next_move), depth - 1))

        return move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        self.current_best_move = NEGATIVE_MOVE

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 0
            while True:
                depth += 1
                self.current_best_move = self.alphabeta(game, depth)
                if game.utility(game.active_player):
                    break

        except SearchTimeout:
            if self.current_best_move == NEGATIVE_MOVE and \
                    game.get_legal_moves(game.active_player):
                return game.get_legal_moves(game.active_player)[0]

        return self.current_best_move

    def alphabeta(self,
                  game: Board, depth, alpha=float("-inf"), beta=float("inf")) -> tuple:
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!

        move = NEG_INFINITY
        alpha_move = (alpha, NEGATIVE_MOVE)
        for next_move in game.get_legal_moves(game.active_player):
            move = max(move,
                       self.min_value(game.forecast_move(next_move),
                                      depth - 1,
                                      alpha_move[0],
                                      beta))
            if move == alpha_move[0]:
                continue
            alpha_move = max(alpha_move, (move, next_move))
        return alpha_move[1]

    def max_value(self, game: Board, depth: int, alpha: float, beta: float) -> float:
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth <= 0 or game.is_loser(game.active_player):
            return self.score(game, game.active_player)

        legal_moves = game.get_legal_moves(game.active_player)
        move = NEG_INFINITY
        for next_move in legal_moves:
            move = max(move,
                       self.min_value(game.forecast_move(next_move),
                                      depth - 1,
                                      alpha,
                                      beta))
            if move >= beta:
                return move
            alpha = max(alpha, move)
        return alpha

    def min_value(self, game: Board, depth: int, alpha: float, beta: float) -> float:
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth <= 0 or game.is_loser(game.active_player):
            return self.score(game, game.inactive_player)

        legal_moves = game.get_legal_moves(game.active_player)
        move = INFINITY
        for next_move in legal_moves:
            move = min(move,
                       self.max_value(game.forecast_move(next_move),
                                      depth - 1,
                                      alpha,
                                      beta))
            if move <= alpha:
                return move
            beta = min(beta, move)
        return beta
