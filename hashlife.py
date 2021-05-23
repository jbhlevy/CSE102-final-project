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
        self.n = n
        self.m = m
        self.cells = cells

    def round(self):
        cells = []
        for i in range(self.n):
            cells.append([0 for j in range(self.m)])
        for i in range(self.n):
            for j in range(self.m):
                cells[i][j] = self.cells[i][j]
        for i in range(self.n):
            for j in range(self.m):
                cell = cells[i][j]
                counter = 0
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if (0<=i+k<self.n and 0<=j+l<self.m) and not (l==0 and k==0):
                            if cells[i+k][j+l]:
                                counter += 1
                if cell and (counter != 2 and counter != 3):
                    self.cells[i][j] = False
                if not cell and counter == 3:
                    self.cells[i][j] = True

    def get(self, i, j):
        return self.cells[i][j]
    

class AbstractNode:
    @property
    def level(self):
        """Level of this node"""
        raise NotImplementedError

    @property
    def population(self):
        """Total population of the area"""
        raise NotImplementedError

    nw = property(lambda self : None)
    ne = property(lambda self : None)
    sw = property(lambda self : None)
    se = property(lambda self : None)
    
    @staticmethod
    def zero(k):
        node = AbstractNode()
        node.level = k
        node.population = 0
        return node
    
    def extend(self):
        node = AbstractNode()
        node.level = self.level + 1
        node.nw = AbstractNode(se=self.nw)
        node.ne = AbstractNode(sw=self.ne)
        node.sw = AbstractNode(ne=self.sw)
        node.se = AbstractNode(nw=self.se)
        return node
    
    
class CellNode(AbstractNode):
    def __init__(self, alive):
        super().__init__()

        self._alive = bool(alive)

    level      = property(lambda self : 0)
    population = property(lambda self : int(self._alive))
    alive      = property(lambda self : self._alive)
    
    
class Node(AbstractNode):
    def __init__(self, nw, ne, sw, se):
        super().__init__()

        self._level      = 1 + nw.level
        self._population =  \
            nw.population + \
            ne.population + \
            sw.population + \
            se.population
        self._nw = nw
        self._ne = ne
        self._sw = sw
        self._se = se

    level      = property(lambda self : self._level)
    population = property(lambda self : self._population)

    nw = property(lambda self : self._nw)
    ne = property(lambda self : self._ne)
    sw = property(lambda self : self._sw)
    se = property(lambda self : self._se)
    
    

        
        
























