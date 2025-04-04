from collections import deque
from processInput import checkProgramCall
import sys
from puzzle import Puzzle
import copy


class Solver:
    strategy = sys.argv[1]
    strategy_options = list(sys.argv[2])  # ex 'L' 'U' 'R' 'D'
    puzzleFileName = sys.argv[3]
    solutionFileName = sys.argv[4]
    solResultsFileName = sys.argv[5]
    visited = set()

    def bfs(self, puzzle: Puzzle):
        """Solves the puzzle using Breadth-First Search (BFS)."""

        queue = deque([(puzzle, [])])  # (current puzzle state, moves taken)
        self.visited.add(self.to_tuple(puzzle.board))  # Store initial state

        while queue:
            current_puzzle, moves = queue.popleft()

            # If puzzle is solved, return it with its solution steps
            if current_puzzle.isGoal():
                current_puzzle.solutionSteps = moves
                return current_puzzle

            # Explore all possible moves
            for move in current_puzzle.getPossibleMoves():
                new_puzzle = current_puzzle.makeMove(move)
                new_state = self.to_tuple(new_puzzle.board)

                if new_state not in self.visited:
                    self.visited.add(new_state)
                    queue.append((new_puzzle, moves + [move]))

        return None  # No solution found (shouldn't happen for solvable puzzles)

    def to_tuple(self, board):
        """Convert board to a tuple for hashing in a set (to track visited states)."""
        return tuple(tuple(row) for row in board)


def main():
    checkProgramCall()
    solver = Solver()
    puzzle = Puzzle(solver.puzzleFileName)

    solved = solver.bfs(puzzle)

    solved.printBoard()
    solved.save(solver.solutionFileName, solver.solResultsFileName)


main()
