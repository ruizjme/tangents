#!/usr/bin/env python

"""
Draw circles with tangents

Sources:
    https://stackoverflow.com/questions/4781184/tkinter-displaying-a-square-grid
    http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

Author: Jaime RS
Date:   Jun 2020
"""

import math
import sys
import sympy

if sys.version_info[0] == 3:  # for Python3
    import tkinter as tk
else:  # for Python2
    import Tkinter as tk

def find_q(px, py, h, k, R, r, precision=2):
    """
    Solve for a point Q on the big circle such that a line
    between P and Q is tangent to the small circle at A = (0.5P+0.5Q)

    Symbolic equations python from:
        https://stackoverflow.com/questions/44145450/system-of-quadratic-equations-python
    """
    qx, qy = sympy.symbols("qx qy", real=True)
    eq1 = sympy.Eq(((0.5*px+0.5*qx) - h)**2 + ((0.5*py+0.5*qy) - k)**2, r**2)
    eq2 = sympy.Eq((qx - h)**2 + (qy - k)**2, R**2)
    return [(round(s[qx], precision), round(s[qy], precision))
            for s in sympy.solve([eq1, eq2])]

class GUI(tk.Tk):
    """
    Example:
    >>> app = GUI(R, n)
    >>> app.mainloop()
    """

    def __init__(self, R, *args, n=None, r=None, **kwargs):
        """
        R (int) size of the big circle
        n (int) number of sides of the polygon
        """
        W = 500
        H = 500

        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self,
                                width=W,
                                height=H,
                                borderwidth=0,
                                highlightthickness=0)

        # self.canvas.focus_set()
        # self.canvas.bind("<Key>", lambda event: exit())
        self.canvas.pack(side="top", fill="both", expand="true")

        # Params
        if not r and n:
            r = R * math.sin((math.pi/2)*(n-2)/n)
        self.R = R
        self.r = r
        self.h = h = W/2
        self.k = k = H/2

        # Big circle
        self.big_circle = (h-R, k-R, h+R, k+R)
        self.canvas.create_oval(*self.big_circle)

        # Small circle
        self.small_circle = (h-r, k-r, h+r, k+r)
        self.canvas.create_oval(*self.small_circle)

        # Lines
        self.lines = []

        self.p0 = h-R, k
        self.redraw(50, self.p0)

    def redraw(self, delay, p, prev_p=None):

        # while True:
        # # for i in range(30):
        solutions = find_q(p[0], p[1], self.h, self.k, self.R, self.r)
        print(solutions)
        q = None
        for s in solutions:
            if s != prev_p:
                q = s
                break
        if not q:
            print('RETURN 2')
            return
        self.lines.append((p[0], p[1], q[0], q[1]))
        # Drawing ####################################
        self.canvas.create_oval(*self.small_circle)
        self.canvas.create_oval(*self.big_circle)
        for line in self.lines:
            self.canvas.create_line(*line)
        ##############################################
        if q == self.p0:
            print('RETURN 3')
            return
        prev_p = p
        p = q

        self.after(delay, lambda: self.redraw(delay, p, prev_p=prev_p))


if __name__ == '__main__':

    # n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    r = 150
    R = 200
    app = GUI(R, r=r)
    app.mainloop()
