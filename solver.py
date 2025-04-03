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


def readPuzzle(fileName: str, puzzle: Puzzle):
    with open(fileName) as f:
        # the first line contains the board size
        puzzleSize = f.readline().replace(" ", "")
        puzzle.rowNr = int(puzzleSize[0])
        puzzle.colNr = int(puzzleSize[1])

        # read values in each row (strip '\n' and omit whitespaces)
        elements = f.readline().strip().replace(" ", "")

        while elements:
            # turn an list of strings ex. ["1" ,"2" ,"3"] into an list of ints [1,2,3]
            print(elements)
            elementVal = list(map(int, elements))
            puzzle.board.append(elementVal)
            elements = f.readline().strip().replace(" ", "")


def main():
    checkProgramCall()
    solver = Solver()
    puzzle = Puzzle()
    readPuzzle(solver.puzzleFileName, puzzle)
    print(puzzle.board)


main()
