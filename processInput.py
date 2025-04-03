import sys
import re


def checkProgramCall():
    if len(sys.argv) != 6:
        print(
            "Usage: python fifteenPuzzle.py <bfs/dfs/astr> <permutations of LURD/hamm/manh> <puzzleFileName> <outputFileName> <specificOutputFileName"
        )
        sys.exit(1)
    if re.match("bfs|dfs|astr", sys.argv[1]) is None:
        print("Usage: python fifteenPuzzle.py <bfs/dfs/astr>**")
    if re.match("[LURD]{4}|manh|hamm", sys.argv[2]) is None:
        print(
            "Usage: python fifteenPuzzle.py <bfs/dfs/astr> <permutations of LURD/hamm/manh>**"
        )
