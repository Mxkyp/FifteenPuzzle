from collections import deque
from queue import PriorityQueue
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
        self.visited.add(self.toTuple(puzzle.board))
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
                    new_state = self.toTuple(new_puzzle.board)

                    if new_state not in self.visited:
                        self.visited.add(new_state)
                        puzzle.visitedStates += 1
                        queue.append((new_puzzle, moves + [move]))

        puzzle.computationTime = time.time() - start_time

    def dfs(self, puzzle: Puzzle) -> None:
        """Solves the puzzle using Depth-First Search (DFS). Modifies the input puzzle directly."""

        start_time = time.time()
        stack = [(puzzle, [], 0)]  # (puzzle state, move list, current depth)
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
            for move in reversed(self.strategy_options):  # reversed for DFS
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
        return tuple(tuple(row) for row in board)

    @staticmethod
    def distanceHamming(puzzle) -> int:
        """ Calculate Hamming distance (number of misplaced tiles) """
        distance: int = 0
        for i in range(puzzle.rowNr):
            for j in range(puzzle.colNr):
                if puzzle.board[i][j] != 0:  # Skip the empty tile
                    expectedValue: int = i * puzzle.colNr + j + 1  # Calculate the expected position for this value
                    if i == puzzle.rowNr - 1 and j == puzzle.colNr - 1:  # Account for the last position (should be 0)
                        expectedValue = 0

                    if puzzle.board[i][j] != expectedValue:
                        distance += 1
        return distance

    @staticmethod
    def distanceManhattan(puzzle) -> int:
        """ Calculate Manhattan distance (number of misplaced tiles) """
        distance: int = 0
        for i in range(puzzle.rowNr):
            for j in range(puzzle.colNr):
                value: int = puzzle.board[i][j]
                if value != 0:  # Skip the empty tile
                    expectedRow: int = (value - 1) // puzzle.colNr  # Calculate the expected position for this value
                    expectedCol: int = (value - 1) % puzzle.colNr

                    distance += abs(i - expectedRow) + abs(
                        j - expectedCol)  # Calculate Manhattan distance for this tile
        return distance

    def astar(self, puzzle: Puzzle) -> None:
        """ Solves the puzzle using A* algorithm with the specified heuristic """
        startTime = time.time()

        openSet = PriorityQueue() # Priority queue for A* (fScore, moveCount, moves, puzzle)

        heuristicFunction = (  # Choose the heuristic function
            self.distanceHamming if self.strategy == "hamn" else self.distanceManhattan
        )

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
