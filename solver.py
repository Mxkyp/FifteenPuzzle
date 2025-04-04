from processInput import checkProgramCall
import sys
from puzzle import Puzzle


class Solver:
    strategy = sys.argv[1]
    strategy_options = list(sys.argv[2])  # ex 'L' 'U' 'R' 'D'
    puzzleFileName = sys.argv[3]
    solutionFileName = sys.argv[4]
    solResultsFileName = sys.argv[5]

    def bfs(self, puzzle: Puzzle) -> Puzzle:
        return puzzle


def main():
    checkProgramCall()
    solver = Solver()
    puzzle = Puzzle(solver.puzzleFileName)

    puzzle.printBoard()


main()
