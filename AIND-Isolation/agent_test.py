"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

    def test_game_play(self):
        game = isolation.Board(self.player1, self.player2, width=3, height=3)
        depth = 2
        player = game_agent.MinimaxPlayer(search_depth=depth)
        time_left = lambda: 10000
        print(game.to_string(), -1)

        for i in range(13):
            move = player.get_move(game, time_left)
            if move == (-1, -1):
                print("{} wins".format(game.inactive_player))
                break
            else:
                print("Move: {}".format(move))

            game.apply_move(move)
            print(game.to_string(), i)

        pass

    @unittest.skip
    def test_return_best_starting_position_if_first_to_act(self):
        pass


if __name__ == '__main__':
    unittest.main()
