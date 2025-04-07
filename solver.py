from collections import deque
from queue import PriorityQueue
from processInput import checkProgramCall
import sys
from puzzle import Puzzle
import time

"""
Klasa rozwiązująca układanke fifteen-puzzle
"""
class Solver:
    """
    Klasa rozwiązująca układankę fifteen-puzzle (układanka 15 lub ogólnie puzzle N)
    Implementuje trzy różne algorytmy przeszukiwania: BFS, DFS i A*
    """
    # Przetwarzanie argumentów wiersza poleceń
    strategy = sys.argv[1]                                          # Pierwszy argument: strategia rozwiązywania (bfs, dfs, astr)

    if strategy == "astr":
        heuristic = sys.argv[2]                                     # Dla A* drugi argument to heurystyka (hamm lub manh)
        strategyOptions = ["L", "U", "D", "R"]                      # Dla A* używamy stałej kolejności ruchów
    else:
        strategyOptions = list(sys.argv[2])                         # Dla BFS/DFS drugi argument to kolejność ruchów (np. LUDR)
        heuristic = None                                            # Dla BFS/DFS nie używamy heurystyki

    # Nazwy plików z argumentów wiersza poleceń
    puzzleFileName = sys.argv[3]                                    # Plik wejściowy z układanką
    solutionFileName = sys.argv[4]                                  # Plik do zapisania rozwiązania
    solResultsFileName = sys.argv[5]                                # Plik do zapisania statystyk rozwiązania
    visited = set()                                                 # Zbiór odwiedzonych stanów planszy (zapobiega cyklom)

    def bfs(self, puzzle: Puzzle) -> None:
        """
        Algorytm przeszukiwania wszerz (Breadth-First Search) do rozwiązania układanki.

        Parametry:
         - `puzzle`: obiekt z klasy Puzzle (w początkowej pozycji)

        Poniższe atrybuty obiektu 'puzzle' są aktualizowane przez metodę:
         - `puzzle.visitedStates`: liczba stanów odwiedzonych w trakcie przeszukiwania
         - `puzzle.processedStates`: liczba stanów przetworzonych (wyjętych z kolejki)
         - `puzzle.solutionSteps`: lista kroków (znaków ze zbioru {L,U,R,D}) prowadzących do rozwiązania
         - `puzzle.solutionLength`: liczba kroków potrzebnych do uzyskania rozwiązania
         - `puzzle.computationTime`: czas potrzebny do znalezienia rozwiązania w sekundach

        BFS gwarantuje znalezienie najkrótszego rozwiązania, ale może wymagać dużo pamięci.
         """
        start_time = time.time()                                    # Rozpoczęcie pomiaru czasu
        queue = deque([(puzzle, [])])                               # Kolejka FIFO dla BFS: (stan układanki, lista wykonanych ruchów)
        self.visited.add(self.toTuple(puzzle.board))                # Dodanie stanu początkowego do odwiedzonych
        puzzle.visitedStates = 1                                    # Licznik odwiedzonych stanów

        while queue:
            current_puzzle, moves = queue.popleft()
            puzzle.processedStates += 1

            if current_puzzle.isGoal():
                puzzle.solutionSteps = moves
                puzzle.solutionLength = len(moves)
                puzzle.computationTime = time.time() - start_time
                return

            possible_moves = current_puzzle.getPossibleMoves()
            for move in self.strategyOptions:
                if move in possible_moves:
                    new_puzzle = current_puzzle.makeMove(move)
                    new_state = self.toTuple(new_puzzle.board)

                    if new_state not in self.visited:
                        self.visited.add(new_state)
                        puzzle.visitedStates += 1
                        queue.append((new_puzzle, moves + [move]))

        puzzle.computationTime = time.time() - start_time

    def dfs(self, puzzle: Puzzle) -> None:
        """
        Algorytm przeszukiwania w głąb (Depth-First Search) do rozwiązania układanki.

        Parametry:
         - `puzzle`: obiekt z klasy Puzzle (w początkowej pozycji)

        Poniższe atrybuty obiektu 'puzzle' są aktualizowane przez metodę:
         - `puzzle.visitedStates`: liczba stanów odwiedzonych w trakcie przeszukiwania
         - `puzzle.processedStates`: liczba stanów przetworzonych (wyjętych ze stosu)
         - `puzzle.solutionSteps`: lista kroków (znaków ze zbioru {L,U,R,D}) prowadzących do rozwiązania
         - `puzzle.solutionLength`: liczba kroków potrzebnych do uzyskania rozwiązania
         - `puzzle.computationTime`: czas potrzebny do znalezienia rozwiązania w sekundach
         - `puzzle.recursionDepth`: maksymalna głębokość osiągnięta podczas przeszukiwania

        DFS może nie znaleźć najkrótszego rozwiązania, ale zużywa mniej pamięci niż BFS.
        Ograniczamy głębokość przeszukiwania do puzzle.max_recursionDepth, aby uniknąć nieskończonej rekursji.
       """
        start_time = time.time()
        stack = [(puzzle, [], 0)]  # (stan puzzla, lista ruchów, obecna głębokość)
        self.visited.add(self.toTuple(puzzle.board))
        puzzle.visitedStates = 1
        puzzle.recursionDepth = 0

        while stack:
            current_puzzle, moves, depth = stack.pop()
            puzzle.processedStates += 1
            puzzle.recursionDepth = max(puzzle.recursionDepth, depth)

            if depth >= puzzle.max_recursionDepth:
                continue

            if current_puzzle.isGoal():
                puzzle.solutionSteps = moves
                puzzle.solutionLength = len(moves)
                puzzle.computationTime = time.time() - start_time
                return

            possible_moves = current_puzzle.getPossibleMoves()
            for move in reversed(self.strategyOptions):
                if move in possible_moves:
                    new_puzzle = current_puzzle.makeMove(move)
                    new_state = self.toTuple(new_puzzle.board)

                    if new_state not in self.visited:
                        self.visited.add(new_state)
                        puzzle.visitedStates += 1
                        stack.append((new_puzzle, moves + [move], depth + 1))

        puzzle.computationTime = time.time() - start_time

    @staticmethod
    def toTuple(board):
        """
        Konwertuje planszę (listę list) na krotkę krotek.

        Parametry:
        - `board`: plansza jako lista list

        Zwraca:
        - krotkę krotek reprezentującą planszę (do użycia jako klucz w zbiorach i słownikach)

        Funkcja pomocnicza, ponieważ listy nie są haszowalne, a krotki tak.
        Umożliwia to używanie planszy jako klucza w zbiorach i słownikach.
        """
        return tuple(tuple(row) for row in board)

    @staticmethod
    def distanceHamming(puzzle) -> int:
        """
        Oblicza odległość Hamminga dla układanki.

        Parametry:
         - `puzzle`: obiekt klasy Puzzle

        Zwraca:
         - liczbę elementów, które nie są na swoich docelowych pozycjach

        Odległość Hamminga to liczba elementów, które nie są na swoich docelowych pozycjach.
        Jest to prosta heurystyka do szacowania odległości od stanu końcowego.
        """
        distance: int = 0
        for i in range(puzzle.rowNr):
            for j in range(puzzle.colNr):
                if puzzle.board[i][j] != 0:                                         # Pomijamy puste pole (0)
                    expectedValue: int = i * puzzle.colNr + j + 1                   # Obliczanie oczekiwanej wartość dla tej pozycji
                    if i == puzzle.rowNr - 1 and j == puzzle.colNr - 1:             # Uwzględnienie ostatniej pozycji (powinna być 0)
                        expectedValue = 0

                    if puzzle.board[i][j] != expectedValue:
                        distance += 1
        return distance

    @staticmethod
    def distanceManhattan(puzzle) -> int:
        distance: int = 0
        for i in range(puzzle.rowNr):
            for j in range(puzzle.colNr):
                value: int = puzzle.board[i][j]
                if value != 0:  # Skip the empty tile
                    expectedRow: int = (value - 1) // puzzle.colNr  # Calculate the expected position for this value
                    expectedCol: int = (value - 1) % puzzle.colNr

                    distance += abs(i - expectedRow) + abs(j - expectedCol)  # Calculate Manhattan distance for this tile
        return distance

    def astar(self, puzzle: Puzzle) -> None:
        """
      Parametery:
         - `puzzle`: obiekt z klasy Puzzle (we wstepnej pozycji)

     Poniżsi członkowie 'puzzle' są ustawiani w metodzie
         - `puzzle.visitedStates`: ilość stanów odwiedzonych
         - `puzzle.processedStates`: ilość stanów przetworzonych
         - `puzzle.solutionSteps`: lista kroków(znaków z zbioru {L,U,R,D}) podjętych do uzyskania rozwiązania
         - `puzzle.solutionLength`: ilość kroków podjętych do uzyskania rozwiązania
         - `puzzle.computationTime`: czas potrzebny do uzyskania rozwiązania.
         - `puzzle.recursionDepth`: maksymalna głebokość uzyskana przy poszukiwaniu rozwiązywania.

     metoda wykorzystuje jedną z dwóch heurystyk możliwych w `self.heuristic`:
     - `"hamm"`: heurystyka dystansu hamminga.
     - `"manh"`: heurystyka dystansu Manhattan.

     """
        startTime = time.time()

        openSet = PriorityQueue() # Priority queue for A* (fScore, moveCount, moves, puzzle)

        if self.heuristic == "hamm":
            heuristicFunction = self.distanceHamming
        elif self.heuristic == "manh":
            heuristicFunction = self.distanceManhattan
        else:
            raise ValueError(f"Unknown heuristic strategy: {self.heuristic}. Use 'hamm' or 'manh' instead. ")

        initialHScore = heuristicFunction(puzzle)
        initialStateTuple = self.toTuple(puzzle.board)
        openSet.put((initialHScore, 0, [], puzzle)) # Initial state

        visitedGScores = {initialStateTuple: 0} # Track visited states with their gScores (to avoid cycles)

        puzzle.visitedStates = 1
        puzzle.processedStates = 0
        puzzle.recursionDepth = 0

        while not openSet.empty():
            _, gScore, moves, currentPuzzle = openSet.get()  # Get the state with the lowest fScore
            puzzle.processedStates += 1

            if currentPuzzle.isGoal(): # Check if the goal was reached
                puzzle.solutionSteps = moves
                puzzle.solutionLength = len(moves)
                puzzle.computationTime = time.time() - startTime
                return

            possibleMoves = currentPuzzle.getPossibleMoves() # Try all possible moves
            for move in possibleMoves:
                newPuzzle = currentPuzzle.makeMove(move)
                newState = self.toTuple(newPuzzle.board)
                newGScore = gScore + 1

                if newState in visitedGScores and visitedGScores[newState] <= newGScore: # Check if the state has been visited with a better path
                    continue

                visitedGScores[newState] = newGScore # Updated visited states
                puzzle.visitedStates += 1

                hScore = heuristicFunction(newPuzzle) # Calculate heuristic score for the new state
                fScore = newGScore + hScore

                puzzle.recursionDepth = max(puzzle.recursionDepth, newGScore) # Update recursion depth

                openSet.put((fScore, newGScore, moves + [move], newPuzzle)) # Add to the priority queue

        puzzle.computationTime = time.time() - startTime # No solution found

def main():
    checkProgramCall()
    solver = Solver()
    puzzle = Puzzle(solver.puzzleFileName)

    if solver.strategy == "bfs":
        solver.bfs(puzzle)
    elif solver.strategy == "dfs":
        solver.dfs(puzzle)
    elif solver.strategy == "astr":
        solver.astar(puzzle)

    puzzle.save(solver.solutionFileName, solver.solResultsFileName)


main()
