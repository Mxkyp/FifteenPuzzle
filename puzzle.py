import sys
from typing import List, Tuple, Optional
import copy


class Puzzle:
    """
    Klasa reprezentująca grę układanki przesuwanej (sliding puzzle, fifteen puzzle).
    Pozwala na wczytywanie układanki z pliku, rozwiązywanie jej i zapisywanie rozwiązania.
    """
    def __init__(
        self, filename: Optional[str] = None, rows: int = 4, cols: int = 4
    ) -> None:
        """
        Inicjalizacja obiektu układanki.

        Parametry:
            filename: Opcjonalna ścieżka do pliku z układanką do wczytania
            rows: Liczba wierszy układanki (domyślnie 4)
            cols: Liczba kolumn układanki (domyślnie 4)

        Inicjalizuje zmienne statystyczne i stan układanki.
        """
        # Zmienne do śledzenia statystyk rozwiązania
        self.visitedStates: int = 0                     # Liczba odwiedzonych stanów podczas rozwiązywania
        self.processedStates: int = 0                   # Liczba przetworzonych stanów podczas rozwiązywania
        self.max_recursionDepth: int = 20               # Maksymalna dozwolona głębokość rekursji
        self.recursionDepth = 0                         # Aktualna głębokość rekursji
        self.solutionLength: int = 0                    # Długość znalezionego rozwiązania
        self.computationTime: float = 0.0               # Czas obliczeń w sekundach

        # Stan układanki
        self.board: List[List[int]] = []                # Plansza układanki jako lista list
        self.zeroPos: Tuple[int, int] = (0, 0)          # Pozycja pustego pola (wiersz, kolumna)
        self.rowNr: int = rows                          # Liczba wierszy układanki
        self.colNr: int = cols                          # Liczba kolumn układanki
        self.solutionSteps: List[str] = []              # Lista kroków rozwiązania (U, D, L, R)

        # Inicjalizacja stanu początkowego
        if filename:
            self.read(filename)                         # Wczytanie układanki z pliku
            self.setZeroPos()                           # Znalezienie pozycji pustego pola
        else:
            self.initSolvedState(rows, cols)            # Zainicjowanie stanu rozwiązanego (cel)

    def read(self, fileName: str):
        """
        Wczytuje układankę z pliku.

        Parametry:
            fileName: Ścieżka do pliku z układanką

        Format pliku:
        - Pierwszy wiersz: liczba wierszy i kolumn oddzielone spacją
        - Kolejne wiersze: wartości pól oddzielone spacjami (0 oznacza puste pole)

        Sprawdza poprawność danych wejściowych i kończy program w przypadku błędów.
        """
        with open(fileName) as f:
            # Odczytanie wymiarów układanki
            puzzleSize = f.readline().strip().split()
            if not puzzleSize:
                print(f"Error: Imput file {fileName} is empty or missing dimensions.")
                sys.exit(1)
            # Pierwszy wiersz zawiera wymiary planszy
            self.rowNr = int(puzzleSize[0])
            self.colNr = int(puzzleSize[1])

            # Odczytanie wartości dla każdego wiersza (usuń '\n' i ignoruj białe znaki)
            self.board = []
            for i in range(self.rowNr):
                elements = f.readline().strip().split()
                if not elements:
                    print(f"Error: Imput file {fileName} has fewer rows than expected ({self.rowNr}).")
                    sys.exit(1)
                if len(elements) != self.colNr:
                    print(f"Erroe: Row {i + 1} in {fileName} has {len(elements)} elements, expected {self.colNr}.")
                    sys.exit(1)
                elementVal = list(map(int, elements))                   # Konwersja elementów na liczby całkowite
                self.board.append(elementVal)

            # Sprawdzenie, czy nie ma dodatkowych wierszy
            extraLine = f.readline().strip()
            if extraLine:
                print(f"Error: Input file {fileName} has more rows than expected ({self.rowNr}).")
                sys.exit(1)

            # Sprawdzenie poprawności wartości na planszy (czy zawierają wszystkie liczby od 0 do n*m-1)
            expectedValues = set(range(self.rowNr * self.colNr))
            boardValues = set()
            for row in self.board:
                for value in row:
                    boardValues.add(value)
            if boardValues != expectedValues:
                print(f"Error: Board values in {fileName} are invalid. Expected {expectedValues}, got {boardValues}")
                sys.exit(1)

    def setZeroPos(self):
        """
        Ustawia pozycję pustego pola (oznaczonego jako 0) na planszy.

        Wyjątek:
            ValueError: Jeśli jest pusta lub nie zaleziono pustego pola.
        """
        if not self.board:
            raise ValueError("Board is empty.")

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] == 0:
                    self.zeroPos = (r, c)
                    return
        raise ValueError("No empty tile (0) found on the board.")

    def save(self, solutionFileName: str, solResultsFileName: str):
        """
        Zapisuje rozwiązanie i statystyki do plików.

        Parametry:
            solutionFileName: Ścieżka do pliku, gdzie zostanie zapisane rozwiązanie
            solResultsFileName: Ścieżka do pliku, gdzie zostaną zapisane statystyki rozwiązania

        Format pliku rozwiązania:
        - Pierwszy wiersz: długość rozwiązania lub -1, jeśli nie znaleziono rozwiązania
        - Następny wiersz: kroki rozwiązania (U, D, R, L)

         Format pliku statystyk:
        - Pierwszy wiersz: długość rozwiązania lub -1, jeśli nie znaleziono rozwiązania
        - Drugi wiersz: liczba odwiedzonych stanów
        - Trzeci wiersz: liczba przetworzonych stanów
        - Czwarty wiersz: głębokość rekursji
        - Piąty wiersz: czas obliczeń w sekundach (z dokładnością do 3 miejsc po przecinku)
        """
        with open(solutionFileName, "w") as f:
            # Jeśli nie znaleziono rozwiązania, ale sprawdzono jakieś stany
            if self.solutionLength == 0 and self.visitedStates != 0:
                f.write("-1" + "\n")  # Nie udało się znaleźć rozwiązania
            else:
                f.write(str(self.solutionLength) + "\n")
                for step in self.solutionSteps:
                    f.write(step)

        with open(solResultsFileName, "w") as f:
            # Jeśli nie znaleziono rozwiązania, ale sprawdzono jakieś stany
            if self.solutionLength == 0 and self.visitedStates != 0:
                f.write("-1" + "\n")
            else:
                f.write(str(self.solutionLength) + "\n")

            f.write(str(self.visitedStates) + "\n")
            f.write(str(self.processedStates) + "\n")
            f.write(str(self.recursionDepth) + "\n")
            f.write(str(round(self.computationTime, 3)) + "\n")

    def initSolvedState(self, rowNr: int, colNr: int) -> None:
        """
        Inicjalizuje planszę w stanie rozwiązanym (cel).

        Parametry:
            rowNr: Liczba wierszy układanki
            colNr: Liczba kolumn układanki

        Stan rozwiązany to liczby od 1 do (rolNr*colNr-1) ustawione po kolei,
        a puste pole (0) znajduje się w prawym dolnym rogu.
        """
        self.board = []
        count = 1
        for i in range(rowNr):
            row = []
            for j in range(colNr):
                if i == rowNr - 1 and j == colNr - 1:
                    row.append(0)                               # Puste pole w prawym dolnym rogu
                    self.zeroPos = (i, j)
                else:
                    row.append(count)
                    count += 1
            self.board.append(row)

    def isGoal(self) -> bool:
        """
        Sprawdza, czy plansza jest w stanie końcowym (rozwiązanym).

        Zwraca:
             bool: True, jeśli układanka jest rozwiązana, False w przeciwnym wypadku
        """
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

    def getPossibleMoves(self) -> List[str]:
        """
        Zwraca listę możliwych ruchów z aktualnego stanu planszy

        Zwraca:
             List[str]: Lista dozwolonych ruchów ("L", "R", "U", "D")

        Możliwe ruchy zależą od pozycji pustego pola:
        - "L": przesunięcie płytki z lewej strony na puste pole
        - "R": przesunięcie płytki z prawej strony na puste pole
        - "U": przesunięcie płytki z góry na puste pole
        - "D": przesunięcie płytki z dołu na puste pole
        """
        moves = []
        row, col = self.zeroPos

        if col > 0:                             # Można przesunąć w lewo (płytka z lewej na puste pole)
            moves.append("L")

        if col < self.colNr - 1:                # Można przesunąć w prawo
            moves.append("R")

        if row > 0:                             # Można przesunąć w górę
            moves.append("U")

        if row < self.rowNr - 1:                # Można przesunąć w dół
            moves.append("D")

        return moves

    def makeMove(self, move: str):
        """
        Wykonuje ruch i zwraca nowy stan planszy.

        Parametry:
            move: Kierunek ruchu ("L", "R", "U", "D")

        Zwraca:
            Puzzle: Nowy obiekt Puzzle po wykonaniu ruchu

        Uwaga: Kierunki odnoszone są do przesunięcia płytki, a nie pustego pola.
        Na przykład, "L" oznacza przesunięcie płytki z lewej strony na puste pole.
        """
        newBoard = copy.deepcopy(self)
        row, col = newBoard.zeroPos

        if move == "L":
            if col > 0:                                                     # Sprawdzenie, czy można przesunąć w lewo
                newBoard.board[row][col] = newBoard.board[row][col - 1]     # Przesuwanie płytki na puste pole
                newBoard.board[row][col - 1] = 0                            # Nowa pozycja pustego pola
                newBoard.zeroPos = (row, col - 1)                           # Aktualizacja pozycji pustego pola
                return newBoard

        elif move == "R":
            if col < self.colNr - 1:                                        # Sprawdzenie, czy można przesunąć w prawo
                newBoard.board[row][col] = newBoard.board[row][col + 1]
                newBoard.board[row][col + 1] = 0
                newBoard.zeroPos = (row, col + 1)
                return newBoard

        elif move == "U":
            if row > 0:                                                     # Sprawdź, czy można przesunąć w górę
                newBoard.board[row][col] = newBoard.board[row - 1][col]
                newBoard.board[row - 1][col] = 0
                newBoard.zeroPos = (row - 1, col)
                return newBoard

        elif move == "D":
            if row < self.rowNr - 1:                                        # Sprawdź, czy można przesunąć w dół
                newBoard.board[row][col] = newBoard.board[row + 1][col]
                newBoard.board[row + 1][col] = 0
                newBoard.zeroPos = (row + 1, col)
                return newBoard

        return newBoard                 # Jeśli ruch jest nieprawidłowy, zwróć niezmienioną planszę

