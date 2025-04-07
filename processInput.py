import sys
import re

def checkProgramCall():
    # Sprawdzenie, czy liczba argumentów wywołania programu jest dokładnie 6
    if len(sys.argv) != 6:
        print(
            "Usage: python fifteenPuzzle.py <bfs/dfs/astr> <permutations of LURD/hamm/manh> <puzzleFileName> <outputFileName> <specificOutputFileName"
        )
        sys.exit(1)
    # Sprawdzenie, czy pierwszy argument to poprawna metoda przeszukiwania (bfs, dfs lub astr)
    if re.match("bfs|dfs|astr", sys.argv[1]) is None:
        print("Usage: python fifteenPuzzle.py <bfs/dfs/astr>**")
    # Sprawdzenie, czy drugi argument to poprawna heurystyka lub permutacja kierunków ruchu
    # - dla BFS/DFS: permutacje LURD
    # - dla A*: nazwy heurystyk (manh - Manhattan, hamm - Hamming)
    if re.match("[LURD]{4}|manh|hamm", sys.argv[2]) is None:
        print(
            "Usage: python fifteenPuzzle.py <bfs/dfs/astr> <permutations of LURD/hamm/manh>**"
        )
