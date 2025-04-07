from puzzle import Puzzle
import sys


class Validator:
    """
    Klasa walidująca rozwiązanie układanki przesuwnej (sliding puzzle).
    Sprawdza, czy sekwencja ruchów z pliku wyjściowego prawidłowo prowadzi od stanu
    początkowego do stanu końcowego układanki.
    """
    def __init__(self, inputFile: str, outputFile: str):
        """
        Inicjalizacja obiektu walidatora.

        Parametry:
            inputFile: Ścieżka do pliku z początkowym stanem układanki
            outputFile: Ścieżka do pliku z rozwiązaniem (sekwencją ruchów)
        """
        self.inputFile = inputFile                                      # Plik wejściowy z układanką
        self.outputFile = outputFile                                    # Plik wyjściowy z sekwencją ruchów

    def validate(self) -> bool:
        """
        Sprawdza poprawność rozwiązania układanki.

        Zwraca:
            bool: True, jeśli rozwiązanie jest poprawne, False w przeciwnym przypadku

        Walidacja obejmuje:
        1. Wczytanie układanki z pliku wejściowego
        2. Wczytanie sekwencji ruchów z pliku wyjściowego
        3. Sprawdzenie, czy wartość "-1" (brak rozwiązania) jest uzasadniona
        4. Sprawdzenie zgodności liczby ruchów z długością sekwencji
        5. Weryfikację każdego ruchu pod kątem poprawności i możliwości wykonania
        6. Sprawdzenie, czy po wykonaniu wszystkich ruchów układanka jest rozwiązana

        Błędy są zgłaszane na standardowe wyjście błędów (stderr).
        """
        try:
            puzzle = Puzzle(self.inputFile)                             # Próba wczytania układanki z pliku wejściowego
        except Exception as e:
            print(f"Error loading puzzle: {e}", file=sys.stderr)        # Obsługa błędów podczas wczytywania układanki
            return False

        try:
            with open(self.outputFile) as f:
                lines = [line.strip() for line in f.readlines()]        # Wczytanie linii i usunięcie białych znaków
        except Exception as e:
            print(f"Error loading solution {e}", file=sys.stderr)
            return False

        if not lines:
            print(f"Solution file is emppty.", file=sys.stderr)         # Sprawdzenie, czy plik rozwiązania nie jest pusty
            return False

        if lines[0] == "-1":                                            # Wartość "-1" oznacza, że algorytm nie znalazł rozwiązania
            return not puzzle.isGoal()

        try:
            numMoves = int(lines[0])                                    # Próba odczytania liczby ruchów z pierwszej linii pliku
        except ValueError:
            print(f"Invalid number of moves in solution file.", file=sys.stderr)
            return False

        if len(lines) < 2:                                              # Sprawdzenie, czy plik zawiera sekwencję ruchów (co najmniej 2 linie)
            print(f"No moves provided in solution file.", file=sys.stderr)
            return False

        moves = list(lines[1])                                          # Pobranie sekwencji ruchów z drugiej linii pliku

        if numMoves != len(moves):                                      # Sprawdzenie zgodności zadeklarowanej liczby ruchów z długością sekwencji
            print(
                f"Move count ({numMoves}) does not mach sequence length ({len(moves)}).",
                file=sys.stderr,
            )
            return False

        for move in moves:                                              # Wykonanie każdego ruchu z sekwencji i sprawdzenie jego poprawności
            if move not in ["L", "R", "U", "D"]:                        # Sprawdzenie, czy ruch jest jednym z dozwolonych (L, R, U, D)
                print(f"Invalid move {move}.", file=sys.stderr)
                return False

            if move not in puzzle.getPossibleMoves():                   # Sprawdzenie, czy ruch jest możliwy do wykonania w bieżącym stanie układanki
                print(f"Move {move} is not possible in current state.", file=sys.stderr)
                return False

            puzzle = puzzle.makeMove(move)                              # Wykonanie ruchu, aktualizacja stanu układanki

        # Po wykonaniu wszystkich ruchów sprawdzenie, czy układanka jest rozwiązana
        if puzzle.isGoal():
            return True                                                 # Rozwiązanie jest poprawne
        else:
            # Jeśli po wykonaniu wszystkich ruchów układanka nie jest rozwiązana, to rozwiązanie jest niepoprawne
            print(f"Final board is not the goal state.", file=sys.stderr)
            return False


def main():
    """
    Główna funkcja programu walidatora.

    Sprawdza poprawność argumentów wiersza poleceń, tworzy obiekt walidatora,
    przeprowadza walidację i zwraca odpowiedni kod wyjścia.

    Kod wyjścia 0 oznacza poprawne rozwiązanie, kod 1 oznacza błąd walidacji.
    """
    if len(sys.argv) != 3:                                              # Sprawdzenie, czy podano dokładnie 2 argumenty (ścieżki do plików)
        print("Usage: python validator.py <inputFile> <outputFile>", file=sys.stderr)
        sys.exit(1)

    validator = Validator(sys.argv[1], sys.argv[2])                     # Utworzenie obiektu walidatora z argumentami z wiersza poleceń
    result = validator.validate()                                       # Przeprowadzenie walidacji
    sys.exit(0 if result else 1)                                        # Zakończenie programu z odpowiednim kodem wyjścia (0 - sukces, 1 - błąd)


if __name__ == "__main__":
    main()
