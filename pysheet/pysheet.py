#!/usr/bin/env python

import tkinter as tk
import math
import re
from collections import ChainMap

Nrows = 5
Ncols = 5

cellre = re.compile(r'\b[A-Z][0-9]\b')


def cellname(col, row):
    return chr(ord('A')+col) + str(row+1)
    # returns a string translates col 0, row 0 to 'A1'
    # pass


class Cell():
    values = {}
    def __init__(self, row, col, siblings, parent):
        # save off instance variables from arguments
        # and also
        #set name to cellname(i, j)
        # set value of cell to zero
        # set formula to a str(value)
        # Set of Dependencies - must be updated if this cell changes
        # make deps empty
        # Set of Requirements - values required for this cell to calculate
        # make reqs empty
        self.row = row
        self.col = col
        self.name = cellname(col, row)
        self.siblings = siblings
        self.parent = parent

        self.value = 0
        self.formula = str(self.value)

        self.dependencies = set()
        self.requirements = set()
        # be happy you get this machinery for free.
        self.var = tk.StringVar()
        entry = self.widget = tk.Entry(parent,
                                       textvariable=self.var,
                                       justify='right')
        entry.bind('<FocusIn>', self.edit)
        entry.bind('<FocusOut>', self.update)
        entry.bind('<Return>', self.update)
        entry.bind('<Up>', self.move(-1, 0))
        entry.bind('<Down>', self.move(+1, 0))
        entry.bind('<Left>', self.move(0, -1))
        entry.bind('<Right>', self.move(0, 1))
        self.var.set(self.value)
        # set this cell's var to cell's value
        # and you're done.

    def move(self, rowadvance, coladvance):
        targetrow = (self.row + rowadvance) % Nrows
        targetcol = (self.col + coladvance) % Ncols

        def focus(event):
            targetwidget = self.siblings[cellname(targetrow, targetcol)].widget
            targetwidget.focus()

        return focus

    def calculate(self):
        # find all the cells mentioned in the formula.
        #  put them all into a tmp set currentreqs
        #
        # Add this cell to the new requirement's dependents
        # removing all the reqs that we might no longer need
        # for each in currentreqs - self.reqs
        #    my siblings[].deps.add(self.name)
        # Add remove this cell from dependents no longer referenced
        # for each in self.reqs - currentreqs:
        #    my siblings[r].deps.remove(self.name)
        #
        # Look up the values of our required cells
        # reqvalues = a comprehension of r, self.siblings[r].value for r in currentreqs
        # Build an environment with these values and basic math functions

        environment = ChainMap(math.__dict__, reqvalues)
        # Note that eval is DANGEROUS and should not be used in production
        self.value = eval(self.formula, {}, environment)

        # save currentreqs in self.reqs
        # set this cell's var to cell's value
        #

    def propagate(self):

        pass
        # for each of your deps
        #     calculate
        #     propogate

    def edit(self, event):
        # make sure to update the cell with the formula
        self.widget.select_range(0, tk.END)

    def update(self, event):
        # get the value of this cell and put it in formula
        # calculate all dependencies
        # propogate to all dependecnies
        l_formula = str(self.var.get())
        if l_formula[0] == 'A' or l_formula[0] == 'B' or l_formula[0] == 'C' or l_formula[0] == 'D' or l_formula[0] == 'E':
            cellname1 = l_formula[:2]
            cellname2 = l_formula[3:5]
            cell_operation = l_formula[2:3]
            c = self.values[cellname1] + cell_operation + self.values[cellname2]
            d = eval(c)
            self.var.set(d)
            self.values.update( {self.name : d} )
            # pass
        else:
            self.formula = l_formula
            self.values['self.name'] = int(l_formula)
            self.values.update( { self.name : self.formula } )
        if hasattr(event, 'keysym') and event.keysym == "Return":
            self.var.set(self.formula)


    def save(self, filename):
        pass

    def load(self, filename):
        pass

class SpreadSheet(tk.Frame):
    def __init__(self, rows=5, cols=5, master=None):
        super().__init__(master)
        self.rows = rows
        self.cols = cols
        self.cells = {}

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Frame for all the cells
        self.cellframe = tk.Frame(self)
        self.cellframe.pack(side='top')

        # Column labels
        blank = tk.Label(self.cellframe)
        blank.grid(row=0, column=0)
        for j in range(self.cols):
            label = tk.Label(self.cellframe, text=chr(ord('A')+j))
            label.grid(row=0, column=j+1)

        # Fill in the rows
        for i in range(self.rows):
            rowlabel = tk.Label(self.cellframe, text=str(i + 1))
            rowlabel.grid(row=1+i, column=0)
            for j in range(self.cols):
                cell = Cell(i, j, self.cells, self.cellframe)
                self.cells[cell.name] = cell
                cell.widget.grid(row=1+i, column=1+j)


root = tk.Tk()
app = SpreadSheet(Nrows, Ncols, master=root)
app.mainloop()
