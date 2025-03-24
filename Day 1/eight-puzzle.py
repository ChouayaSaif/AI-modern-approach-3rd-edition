import random
import time
import heapq
from functools import partial
from tkinter import *

class EightPuzzle:
    def __init__(self, initial_state):
        self.state = tuple(initial_state)
        self.goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def actions(self, state):
        zero_index = state.index(0)
        row, col = zero_index // 3, zero_index % 3
        moves = []
        if row > 0: moves.append("UP")
        if row < 2: moves.append("DOWN")
        if col > 0: moves.append("LEFT")
        if col < 2: moves.append("RIGHT")
        return moves

    def result(self, state, action):
        zero_index = state.index(0)
        new_state = list(state)
        row, col = zero_index // 3, zero_index % 3
        move_map = {"UP": -3, "DOWN": 3, "LEFT": -1, "RIGHT": 1}
        swap_index = zero_index + move_map[action]
        new_state[zero_index], new_state[swap_index] = new_state[swap_index], new_state[zero_index]
        return tuple(new_state)

    def heuristic(self, state):
        return sum(abs((val - 1) % 3 - i % 3) + abs((val - 1) // 3 - i // 3)
                   for i, val in enumerate(state) if val != 0)

    def astar_search(self):
        frontier = [(self.heuristic(self.state), 0, self.state, [])]
        explored = set()
        while frontier:
            _, cost, state, path = heapq.heappop(frontier)
            if state == self.goal:
                return path
            if state in explored:
                continue
            explored.add(state)
            for action in self.actions(state):
                new_state = self.result(state, action)
                heapq.heappush(frontier, (cost + 1 + self.heuristic(new_state), cost + 1, new_state, path + [action]))
        return []

class EightPuzzleGUI:
    def __init__(self):
        self.root = Tk()
        self.state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.puzzle = EightPuzzle(self.state)
        self.buttons = [None] * 9
        self.init_ui()
        self.root.mainloop()

    def init_ui(self):
        self.create_buttons()
        scramble_btn = Button(self.root, text='Scramble', font=('Helvetica', 30, 'bold'), width=8, command=self.scramble)
        scramble_btn.grid(row=3, column=0, ipady=10)
        solve_btn = Button(self.root, text='Solve', font=('Helvetica', 30, 'bold'), width=8, command=self.solve_steps)
        solve_btn.grid(row=3, column=2, ipady=10)

    def scramble(self):
        actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        for _ in range(60):
            move = random.choice(actions)
            if move in self.puzzle.actions(self.state):
                self.state = list(self.puzzle.result(self.state, move))
        self.update_buttons()

    def solve_steps(self):
        solution = self.puzzle.astar_search()
        for move in solution:
            self.state = list(self.puzzle.result(self.state, move))
            self.update_buttons()
            self.root.update()
            time.sleep(0.75)

    def exchange(self, index):
        zero_ix = self.state.index(0)
        if abs(zero_ix - index) in [1, 3]:
            self.state[zero_ix], self.state[index] = self.state[index], self.state[zero_ix]
            self.update_buttons()

    def create_buttons(self):
        for i in range(9):
            self.buttons[i] = Button(self.root, text=f'{self.state[i]}' if self.state[i] != 0 else None,
                                     width=6, font=('Helvetica', 40, 'bold'), command=partial(self.exchange, i))
            self.buttons[i].grid(row=i // 3, column=i % 3, ipady=40)

    def update_buttons(self):
        for i in range(9):
            self.buttons[i].config(text=f'{self.state[i]}' if self.state[i] != 0 else None)

if __name__ == "__main__":
    EightPuzzleGUI()
