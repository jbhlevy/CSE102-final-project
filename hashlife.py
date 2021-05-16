# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

class Universe:
    def round(self):
        """Compute (in place) the next generation of the universe"""
        raise NotImplementedError

    def get(self, i, j):
        """Returns the state of the cell at coordinates (ij[0], ij[1])"""
        raise NotImplementedError

    def rounds(self, n):
        """Compute (in place) the n-th next generation of the universe"""
        for _i in range(n):
            self.round()
            
            
class NaiveUniverse(Universe):
    def __init__(self, n, m, cells):
        # Do something here
        raise NotImplementedError()

    def round(self):
        # Do something here
        raise NotImplementedError()

    def get(self, i, j):
        # Do something here
        raise NotImplementedError()
        
        
### IS IT NORMAL THAT WE REDEFINE THE PYTHON_IMPLEMENTED ROUNED FUNCTION???