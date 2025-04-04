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
    puzzle.printBoard()
    puzzle.solutionLength = 5
    puzzle.visitedStates = 4
    puzzle.visitedStates = 2
    puzzle.max_recursionDepth = 3
    puzzle.computationTime = 3.5232
    puzzle.save(solver.solutionFileName, solver.solResultsFileName)


main()
