from game import Board, Game, BOARD_SIZE, N_IN_ROW
from mcts_alphaZero import MCTSPlayer
from policy_value_net_pytorch import PolicyValueNet


class Human:
    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            location = input("Your move: ")
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in board.availables:
            print("invalid move")
            move = self.get_action(board)
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run():
    model_file = 'best_policy_pytorch.model'
    try:
        board = Board(size=BOARD_SIZE, n_in_row=N_IN_ROW)
        game = Game(board)

        # ############### human VS AI ###################
        best_policy = PolicyValueNet(BOARD_SIZE, model_file)

        mcts_player = MCTSPlayer(best_policy.policy_value_fn,
                                 c_puct=5,
                                 n_playout=800)  # set larger n_playout for better performance

        # human player, input your move in the format: 2,3
        human = Human()

        # set start_player=0 for human first
        game.start_play(human, mcts_player, start_player=1, is_shown=1)
    except KeyboardInterrupt:
        print('\nQuit')


if __name__ == '__main__':
    run()
