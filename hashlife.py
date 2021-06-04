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
        cells = [[self.cells[i][j] for j in range(self.m)] for i in range(self.n)]
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
        if k == 0:
            return CellNode(0)
        else:
            return Node(AbstractNode.zero(k-1), AbstractNode.zero(k-1), AbstractNode.zero(k-1), AbstractNode.zero(k-1))
        
    
    def extend(self):
        node = self
        print(node.population, 'nw:', node.nw.population, 'ne:', node.ne.population, 'sw:', node.sw.population, 'se:', node.se.population)
        print(self.population)
        if node.level == 0: 
            extended_nodenode = Node(self, AbstractNode.zero(self.level), AbstractNode.zero(self.level), AbstractNode.zero(self.level))
        else:
            extended_nodenode = Node(
                Node(
                    AbstractNode.zero(self.level-1),
                    AbstractNode.zero(self.level-1), 
                    AbstractNode.zero(self.level-1), 
                    node.nw
                    ),
                Node(
                    AbstractNode.zero(self.level-1),
                    AbstractNode.zero(self.level-1),
                    node.ne, 
                    AbstractNode.zero(self.level-1)
                    ),
                Node(
                    AbstractNode.zero(self.level-1), 
                    node.sw, 
                    AbstractNode.zero(self.level-1), 
                    AbstractNode.zero(self.level-1)
                    ),
                Node(
                    node.se, 
                    AbstractNode.zero(self.level-1),
                    AbstractNode.zero(self.level-1), 
                    AbstractNode.zero(self.level-1)
                    )
                )
        return extended_nodenode
    
    def forward(self):
        if self.level < 2:
            return None 
        elif self.level == 2:
            cells = [[nw.population], [ne.population], [sw.population], [ne.population]]
            n = 4
            m = 1
            for i in range(n):
                for j in range(m):
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
            
            
        pass

            
    
    
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
    
import math

class HashLifeUniverse(Universe):
    def __init__(self, *args):
        if len(args) == 1:
            self._root = args[0]
        else:
            self._root = HashLifeUniverse.load(*args)

        self._generation = 0

    @staticmethod
    def load(n, m, cells):
        level = math.ceil(math.log(max(1, n, m), 2))

        mkcell = getattr(AbstractNode, 'cell', CellNode)
        mknode = getattr(AbstractNode, 'node', Node    )

        def get(i, j):
            i, j = i + n // 2, j + m // 2
            return \
                i in range(n) and \
                j in range(m) and \
                cells[i][j]
                
        def create(i, j, level):
            if level == 0:
                return mkcell(get (i, j))

            noffset = 1 if level < 2 else 1 << (level - 2)
            poffset = 0 if level < 2 else 1 << (level - 2)

            nw = create(i-noffset, j+poffset, level - 1)
            sw = create(i-noffset, j-noffset, level - 1)
            ne = create(i+poffset, j+poffset, level - 1)
            se = create(i+poffset, j-noffset, level - 1)

            return mknode(nw=nw, ne=ne, sw=sw, se=se)
                
        return create(0, 0, level)

    def get(self, i, j):
        # Do something here
        raise NotImplementedError()

    def rounds(self, n):
        # Do something here
        raise NotImplementedError()

    def round(self):
        return self.rounds(1)

    @property
    def root(self):
        return self._root
        
    @property
    def generation(self):
        return self._generation
        
        

data = 3, 1, [[True], [True], [True]]
test_node = HashLifeUniverse(*data).root
extended_test_node = test_node.extend()
print('results (pop, lvl):', extended_test_node.population, extended_test_node.level)






















