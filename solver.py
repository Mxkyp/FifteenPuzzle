from processInput import checkProgramCall
import sys


class Puzzle:
    board = []
    rowNr = 0
    colNr = 0


class Solver:
    strategy = sys.argv[1]
    strategy_options = sys.argv[2]
    puzzleFileName = sys.argv[3]
    solutionFileName = sys.argv[4]
    solResultsFileName = sys.argv[5]


def readPuzzle(fileName: str, board: Puzzle):
    with open(fileName) as f:
        puzzleSize = f.readline().split(" ")
        board.rowNr = int(puzzleSize[0])
        board.colNr = int(puzzleSize[1])

        elements = f.readline().split(" ")
        while elements:
            pass


def main():
    checkProgramCall()
    solver = Solver()
    readPuzzle(solver.puzzleFileName)


main()
