from processInput import checkProgramCall
import sys
from puzzle import Puzzle


class Solver:
    strategy = sys.argv[1]
    strategy_options = sys.argv[2]
    puzzleFileName = sys.argv[3]
    solutionFileName = sys.argv[4]
    solResultsFileName = sys.argv[5]


def main():
    checkProgramCall()
    solver = Solver()
    puzzle = Puzzle()

    puzzle.read(solver.puzzleFileName)


main()
