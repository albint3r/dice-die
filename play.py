
from model.board import Board



if __name__ == '__main__':
    bg = Board()
    bg2 = Board()
    bg.add(1, 6)
    bg.add(1, 5)
    bg.add(1, 5)
    bg.add(2, 3)
    bg2.add(1, 5)
    bg2.add(2, 3)
    bg.score.update_column_points(bg.grid, 1)
    bg.score.update_column_points(bg.grid, 2)
    bg.score.update_total_score()
    print(bg)
    bg2.remove_and_update_opponent_board(bg, 1, 5)
    print(bg)
    print(bg is bg)
