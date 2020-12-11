import numpy as np
import random
import argparse

class Board():
    def __init__(self, size, num_people):
        self.size = size
        self.board = np.zeros((size, size), dtype=np.int32)
        self.cross_board = np.zeros((size, size), dtype=np.bool)
        self.num2pos = dict() # self.num2pos[number] = (row, col) in this board

        # fill the board
        self.random_fill(num_people)

    def random_fill(self, num_people):
        ''' fill the board '''
        population = range(num_people)
        # draw self.size * self.size numbers
        sampled = random.sample(population, self.size * self.size)
        self.board[:, :] = np.array(sampled).reshape(self.size, self.size)

        # for later fast retrieval
        for row in range(self.size):
            for col in range(self.size):
                number = self.board[row, col]
                self.num2pos[number] = (row, col)

    def cross(self, number):
        ''' given a number, cross it out on the board '''
        if number not in self.num2pos:
            return
        row, col = self.num2pos[number]
        self.cross_board[row, col] = 1 # mark it hit
        return

    def check(self):
        ''' check if there is any line in this board '''
        hit = False
        # row and col
        for i in range(self.size):
            hit |= all(self.cross_board[i, :]) # row
            hit |= all(self.cross_board[:, i]) # col
            if hit:
                break
        hit |= all(self.cross_board[i, i] for i in range(self.size)) # main diagonal
        hit |= all(self.cross_board[i, self.size-i-1] for i in range(self.size)) # minor diagonal
        return hit

class Report():
    def __init__(self):
        self.count = 0
        self.avg_end_iteration = 0.
        self.avg_num_hit_board = 0. # how many boards hit when the game ends

    def __str__(self):
        # NOTE: avg_end_iteration is the index, so we need to add 1
        return "Average of iteration takes to finish this game is {} and num_hit_board: {}".\
                format(self.avg_end_iteration + 1, self.avg_num_hit_board)

    def add(self, end_iteration, num_hit_board):
        # moving average
        self.avg_end_iteration = \
            (self.avg_end_iteration * self.count + end_iteration) / (self.count + 1)
        self.avg_num_hit_board = \
            (self.avg_num_hit_board * self.count + num_hit_board) / (self.count + 1)

        self.count += 1

def simulate(seed, num_tests, num_people, board_size):
    # fix the source of randomness
    random.seed(seed)

    report = Report()
    for _ in range(num_tests):
        # Initialize boards held by each people
        boards = [Board(board_size, num_people) for _ in range(num_people)]
        # Random the sequence being drawn
        numbers = list(range(num_people))
        random.shuffle(numbers)

        end = False
        end_iteration = -1
        num_hit_board = 0
        for i, num in enumerate(numbers):
            # num is drawn
            for board in boards:
                # cross this number out
                board.cross(num)
                # check if this board has any lines
                if board.check():
                    end = True
                    num_hit_board += 1

            # the game will end whenever at least one people check() is True
            if end:
                end_iteration = i
                break

        # if we draw all people, the game must end
        assert end
        # at least will take 3 iterations to connect the board
        assert end_iteration >= 2

        report.add(end_iteration, num_hit_board)

    assert report.count == num_tests

    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("num_tests", type=int)
    parser.add_argument("num_people", type=int)
    parser.add_argument("board_size", type=int)
    args = parser.parse_args()
    report = simulate(0, args.num_tests, args.num_people, args.board_size)
    print(report)

if __name__ == "__main__":
    main()
