from processInput import checkProgramCall
import sys
import copy
from typing import List, Tuple, Optional, Set, Dict, Callable, Union

class Puzzle:
    def __init__(self, filename: Optional[str] = None, rows: int = 4, cols: int = 4) -> None:

        self.visitedStates: int = 0
        self.processedStates: int = 0
        self.max_recursionDepth: int = 0
        self.solutionLength: int = 0
        self.computationTime: float = 0.0

        self.board: List[List[int]] = []
        self.zeroPos: Tuple[int, int] = (0, 0) #pozycja pustego pola (wiersz, kolumna)
        self.rowNr: int = rows
        self.colNr: int = cols

        if filename:
            self.read(self, filename)
        else:
            self.initSolvedState(rows, cols)

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

    def initSolvedState(self, rowNr: int, colNr: int) -> None: # Inicjalizacja w stanie rozwiązanym
        self.board = []
        count = 1
        for i in range(rowNr):
            row = []
            for j in range(colNr):
                if i == rowNr - 1 and j == colNr - 1:
                    row.append(0)
                    self.zeroPos = (i, j)
                else:
                    row.append(count)
                    count += 1
            self.board.append(row)

    def isGoal(self) -> bool: # Sprawdza czy plansza jest w stanie końcowym
        count = 1
        for i in range(self.rowNr):
            for j in range(self.colNr):
                if i == self.rowNr - 1 and j == self.colNr - 1:
                    if self.board[i][j] != 0:
                        return False
                elif self.board[i][j] != count:
                    return False
                count += 1
        return True

    def getPossibleMoves(self) -> List[str]: # Zwraca możliwe ruchy z aktualnego stany planszy
        moves = []
        row, col = self.zeroPos

        if col > 0:
            moves.append('L')

        if col < self.colNr - 1:
            moves.append('R')

        if row > 0:
            moves.append('U')

        if row < self.rowNr - 1:
            moves.append('D')

        return moves


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
