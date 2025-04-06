from puzzle import Puzzle
import sys

class Validator:
    def __init__(self, imputFile: str, outputFile: str):
        self.imputFile = imputFile
        self.outputFile = outputFile

    def validate(self) -> bool:
        try:
            puzzle = Puzzle(self.imputFile)
        except Exception as e:
            print(f"Error loading puzzle: {e}", file=sys.stderr)
            return False

        try:
            with open(self.outputFile) as f:
                lines = [line.strip() for line in f.readlines()]
        except Exception as e:
            print(f"Error loading solution {e}", file=sys.stderr)
            return False

        if not lines:
            print(f"Solution file is emppty.", file=sys.stderr)
            return False

        if lines[0] == "-1":
            return not puzzle.isGoal()

        try:
            numMoves = int(lines[0])
        except ValueError:
            print(f"Invalid number of moves in solution file.", file=sys.stderr)
            return False

        if len(lines) < 2:
            print(f"No moves provided in solution file.", file=sys.stderr)
            return False

        moves = lines[1:]
        if numMoves != len(moves):
            print(f"Move count ({numMoves}) does not mach sequence length ({len(moves)})." , file=sys.stderr)
            return False

        for move in moves:
            if move not in ["L", "R", "U", "D"]:
                print(f"Invalid move {move}.", file=sys.stderr)
                return False
            if move not in puzzle.PossibleMoves():
                print(f"Move {move} is not possible in current state.", file=sys.stderr)
                return False
            puzzle = puzzle.makeMove(move)

        if puzzle.isGoal():
            return True
        else:
            print(f"Final board is not the goal state.", file=sys.stderr)
            return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python validator.py <inputFile> <outputFile>", file=sys.stderr)
        sys.exit(1)

    validator = Validator(sys.argv[1], sys.argv[2])
    result = validator.validate()
    sys.exit(0 if result else 1)

if __name__ == "__main__":
    main()

#python3 validator.py input.txt bfs_solution.txt
#echo $?
#runval python3 validator.py input.txt bfs_solution.txt

