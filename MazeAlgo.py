from tkinter import *
import time
from typing import List, Any, Tuple, Union


class Square:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.delete = False


class Cell:
    FILLED_COLOR_BG = "black"
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "black"
    EMPTY_COLOR_BORDER = "black"
    FILLED_COLOR_YW = "yellow"
    GOAL = "orange"
    NO_PATHS = "grey"

    def __init__(self, master, x, y, size):
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.isBlock = False
        self.start = False
        self.goal = False
        self.tag = ''.join((str(y), str(x)))

    def _switch(self):
        self.isBlock = True

    def draw(self):
        if self.master is not None:
            fill = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER
            if not self.isBlock:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size
            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=fill, outline=outline)
            print(rowLim, colLim)
            if self.abs == 0 and self.ord == 0:
                self.master.create_text((xmin + self.size // 2, ymin + self.size // 2), text="START")
            if self.abs == colLim and self.ord == rowLim:
                self.master.create_text((xmin + self.size // 2, ymin + self.size // 2), text="GOAL")

    def delete_path(self):
        if self.master is not None:
            fill = Cell.NO_PATHS
            outline = Cell.FILLED_COLOR_BORDER
            if not self.isBlock:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size
            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=fill, outline=outline)
            self.master.create_text((xmin + self.size // 2, ymin + self.size // 2), text="NO PATH",
                                    fill=Cell.EMPTY_COLOR_BG)

    def draw_path(self):
        if self.master is not None:
            fill = Cell.FILLED_COLOR_YW
            outline = Cell.FILLED_COLOR_BORDER

            goal = Cell.GOAL
            if not self.isBlock:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size
            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=fill, outline=outline)
            if self.abs == 0 and self.ord == 0:
                self.master.create_text((xmin + self.size // 2, ymin + self.size // 2), text="START")
            if self.abs == colLim and self.ord == rowLim:
                self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=goal, outline=outline)
                self.master.create_text((xmin + self.size // 2, ymin + self.size // 2), text="GOAL")

    def update(self):
        if self.master is not None:
            fill = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size


class CellGrid(Canvas):
    def __init__(self, master, rowNumber, columnNumber, matrix, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width=cellSize * columnNumber, height=cellSize * rowNumber, *args, **kwargs)
        global rowLim
        global colLim
        rowLim = rowNumber - 1
        colLim = columnNumber - 1
        self.cellSize = cellSize
        self.row_limit = rowNumber
        self.col_limit = columnNumber
        self.grid = []
        self.render = False

        for row in range(len(matrix)):

            line = []
            for column in range(len(matrix[0])):
                if matrix[row][column] == 1:
                    current_cell = Cell(self, column, row, cellSize)
                    current_cell.isBlock = True
                else:
                    current_cell = Cell(self, column, row, cellSize)
                line.append(current_cell)

            self.grid.append(line)
        self.switched = []
        self.draw()

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def temp(self):
        col_lim = self.col_limit
        row_lim = self.row_limit
        for col in range(col_lim):
            cell = self.grid[1][col]
            cell._switch()
            cell.draw()
            self.switched.append(cell)


"""
This class will contain your matrix for your algorithm, you can change the size of your matrix by changing 
-> self.grid = CellGrid(self.root, self.rows, self.cols, self.matrix, SIZE)
You can change the speed of the path showing on the app by changing:
-> self.root.after(TIME, self.update_clock)
You can add your own algorithm by removing this line and calling your own function:
-> self.find_path()
"""


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("DFS on a matrix")
        self.matrix = [
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],

        ]

        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])
        self.grid = CellGrid(self.root, self.rows, self.cols, self.matrix, 75)
        self.grid.pack()
        self.grid_list = []
        self.find_path()
        self.current_square = self.grid_list[0]
        self.grid.bind("<Button-1>", self.handleMouseClick)
        self.root.mainloop()

    def handleMouseClick(self, event):
        self.update_clock()

    def createSquares(self):
        for row in range(self.rows):
            square = Square(row, 1)
            self.grid_list.append(square)
        for row in range(self.rows):
            square = Square(row, 1)
            square.delete = True
            self.grid_list.append(square)

    def getSquare(self):
        if len(self.grid_list) == 1:
            return None
        else:
            tuple = self.grid_list[0]
            print(tuple.row, tuple.col)
            self.grid_list.pop(0)
            return self.grid_list[0]

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        square = self.current_square
        col = square.col
        row = square.row
        cell = self.grid.grid[row][col]
        if square.delete:
            cell.delete_path()
        else:
            cell._switch()
            cell.draw_path()

        self.current_square = self.getSquare()
        if self.current_square is None:
            return
        self.root.after(75, self.update_clock)

    def update_list(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) not in self.grid_list:
                    self.grid_list.append((row, col))
                    break
            else:
                continue
            break

    """
    The following functions are my BFS algorithm, uses the self.matrix defined in the object app, if you would like to 
    try your own algorithm you can replace the following code with your own. The way your path is shown on the app is by 
    adding -> self.add_to_path(current[ROW], current[COL], Bool) the boolean represents if your removing that cell from your
    path or adding to it. 
    """

    def get_neighboors(self, cell, visited):
        calculation = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        bound_x = len(self.matrix[0]) - 1
        bound_y = len(self.matrix) - 1
        neighboors: List[Tuple[Union[int, Any], Union[int, Any]]] = []
        for calc in calculation:
            new_row = cell[0] + calc[0]
            new_col = cell[1] + calc[1]
            if 0 <= new_row <= bound_y and 0 <= new_col <= bound_x and self.matrix[new_row][
                new_col] != 1 and (new_row, new_col) not in visited:
                neighboors.append((new_row, new_col))
        return neighboors

    def add_to_path(self, x, y, delete):
        square = Square(x, y)
        square.delete = delete
        self.grid_list.append(square)

    def find_path(self):
        goal_col = len(self.matrix[0]) - 1
        goal_row = len(self.matrix) - 1
        goal = (goal_row, goal_col)

        start = (0, 0)
        visited = set()
        stack = [start]
        final_path = []
        while stack:
            current = stack[-1]
            final_path.append(current)
            self.add_to_path(current[0], current[1], False)
            if current == goal:
                return final_path
            if current not in visited:
                visited.add(current)
                neighboors = self.get_neighboors(current, visited)
                if not neighboors:
                    stack.pop()
                    self.add_to_path(current[0], current[1], True)
                    final_path.pop()
                else:
                    stack.extend(neighboors)
            else:
                curr = stack.pop()
                self.add_to_path(curr[0], curr[1], True)


app = App()
