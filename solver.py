from processInput import checkProgramCall
import sys


class Puzzle:
    board = []
    rowNr = 0
    colNr = 0

    def read(self, fileName: str):
        with open(fileName) as f:
            # the first line contains the board size
            puzzleSize = f.readline().replace(" ", "")
            self.rowNr = int(puzzleSize[0])
            self.colNr = int(puzzleSize[1])

            # read values in each row (strip '\n' and omit whitespaces)
            elements = f.readline().strip().replace(" ", "")

            while elements:
                elementVal = list(map(int, elements))
                self.board.append(elementVal)
                elements = f.readline().strip().replace(" ", "")


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
