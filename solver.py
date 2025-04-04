from collections import deque
from processInput import checkProgramCall
import sys
from puzzle import Puzzle
import time


class Solver:
    strategy = sys.argv[1]
    strategy_options = list(sys.argv[2])  # ex 'L' 'U' 'R' 'D'
    puzzleFileName = sys.argv[3]
    solutionFileName = sys.argv[4]
    solResultsFileName = sys.argv[5]
    visited = set()

    def bfs(self, puzzle: Puzzle) -> None:
        start_time = time.time()
        queue = deque([(puzzle, [])])  # (current puzzle state, moves taken)
        self.visited.add(self.to_tuple(puzzle.board))
        puzzle.visitedStates = 1

        while queue:
            current_puzzle, moves = queue.popleft()
            puzzle.processedStates += 1

            if current_puzzle.isGoal():
                puzzle.solutionSteps = moves
                puzzle.solutionLength = len(moves)
                puzzle.computationTime = time.time() - start_time
                return

            possible_moves = current_puzzle.getPossibleMoves()
            for move in self.strategy_options:
                if move in possible_moves:
                    new_puzzle = current_puzzle.makeMove(move)
                    new_state = self.to_tuple(new_puzzle.board)

                    if new_state not in self.visited:
                        self.visited.add(new_state)
                        puzzle.visitedStates += 1
                        queue.append((new_puzzle, moves + [move]))

        puzzle.computationTime = time.time() - start_time

    def dfs(self, puzzle: Puzzle) -> None:
        """Solves the puzzle using Depth-First Search (DFS). Modifies the input puzzle directly."""

        start_time = time.time()
        stack = [(puzzle, [], 0)]  # (puzzle state, move list, current depth)
        self.visited.add(self.to_tuple(puzzle.board))
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
            for move in reversed(self.strategy_options):  # reversed for DFS
                if move in possible_moves:
                    new_puzzle = current_puzzle.makeMove(move)
                    new_state = self.to_tuple(new_puzzle.board)

                    if new_state not in self.visited:
                        self.visited.add(new_state)
                        puzzle.visitedStates += 1
                        stack.append((new_puzzle, moves + [move], depth + 1))

        puzzle.computationTime = time.time() - start_time

    def to_tuple(self, board):
        return tuple(tuple(row) for row in board)


def main():
    checkProgramCall()
    solver = Solver()
    puzzle = Puzzle(solver.puzzleFileName)

    if solver.strategy == "bfs":
        solver.bfs(puzzle)
    if solver.strategy == "dfs":
        solver.dfs(puzzle)

    puzzle.save(solver.solutionFileName, solver.solResultsFileName)


main()
