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

        
import weakref
HC  = weakref.WeakValueDictionary()
class AbstractNode:
    #BIG = True
    
    def __init__(self):
        self._cache = None
        self._hash = None
    
    def __hash__(self):
        if self._hash is None:
            self._hash = (
                self.population,
                self.level     ,
                self.nw        ,
                self.ne        ,
                self.sw        ,
                self.se        ,
            )
            self._hash = hash(self._hash)
        return self._hash
    
    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, AbstractNode):
            return False
        return \
            self.level      == other.level      and \
            self.population == other.population and \
            self.nw         is other.nw         and \
            self.ne         is other.ne         and \
            self.sw         is other.sw         and \
            self.se         is other.se
        

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
    def canon(node):
        return HC.setdefault(node, node)
    
    @staticmethod
    def cell(alive):
        return AbstractNode.canon(CellNode(alive))
    
    @staticmethod
    def node(nw, ne, sw, se):
        return AbstractNode.canon(Node(
            nw = nw,
            ne = ne,
            sw = sw,
            se = se))
    
    @staticmethod
    def zero(k):
        if k == 0:
            return AbstractNode.cell(False)
        else:
            zero = AbstractNode.zero(k-1)
            return AbstractNode.node(
                nw = zero, 
                ne = zero, 
                sw = zero, 
                se = zero
                )
        
    
    def extend(self):
        node = self
        if node.level == 0: 
            extended_node = Node(self, AbstractNode.zero(self.level), AbstractNode.zero(self.level), AbstractNode.zero(self.level))
        else:
            zero = AbstractNode.zero(self.level-1)
            extended_node = Node(
                Node(
                    zero,
                    zero, 
                    zero, 
                    node.nw
                    ),
                Node(
                    zero,
                    zero,
                    node.ne, 
                    zero
                    ),
                Node(
                    zero, 
                    node.sw, 
                    zero, 
                    zero
                    ),
                Node(
                    node.se, 
                    zero,
                    zero, 
                    zero
                )
            )
        return extended_node
    
    def forward(self, l=None):
        self._cache = {} if self._cache is None else self._cache
        #print(self._cache)
        
        if self in self._cache:
            return self._cache[self]
        
        if self.population == 0:
            self._cache[self] = self.zero(self.level -1)
            return self._cache[self]
        
    
        if self.level < 2:
            return None 
        elif self.level == 2:
            cells = [[self.nw.nw.population, self.nw.ne.population, self.ne.nw.population, self.ne.ne.population], 
                      [self.nw.sw.population, self.nw.se.population, self.ne.sw.population, self.ne.se.population],
                      [self.sw.nw.population, self.sw.ne.population, self.se.nw.population, self.se.ne.population],
                      [self.sw.sw.population, self.sw.se.population, self.se.sw.population, self.se.se.population]]
            # n = 4
            # m = 4
            # naive_universe = NaiveUniverse(n, m, cells)
            # naive_universe.round()
            # self._cache[self] = AbstractNode.node(nw=AbstractNode.cell(cells[1][1]), 
            #                               ne=AbstractNode.cell(cells[1][2]), 
            #                               sw=AbstractNode.cell(cells[2][1]), 
            #                               se=AbstractNode.cell(cells[2][2]))
            # return  self._cache[self]
# =============================================================================
#         NOT SO NAIVE IMPLEMENTATION
# =============================================================================
            
            mask = 0b0
            for i in range(len(cells)):
                for j in range(len(cells)):
                    if cells[i][j]:
                        mask = mask | 0b1 << (15 - (4*i + j))
                        
        
            # FIVE --------------------
            
            # if bit number 5 is alive
            if (0b1<<5)&mask == 0:
                five_alive = False
            else:
                five_alive = True
                
            # word with only the neighbors of 5
            w = 0b11101010111 & mask 
            five = 0b11101010111
            
            # algo to determine how many neighbors are alive
            n = 0
            while w != 0:
                w = w&(w-1)
                n += 1
                
            # modify five's state accordingly 
            if five_alive:
                if n != 2 and n != 3:
                    five_alive = False
            else:
                if n == 3:
                    five_alive = True
                    
            # SIX --------------------
            
            if (0b1<<6)&mask == 0:
                six_alive = False
            else:
                six_alive = True
            
            six = five << 1
            w = six & mask 
            
            n = 0
            while w != 0:
                w = w&(w-1)
                n += 1
            
            if six_alive:
                if n != 2 and n != 3:
                    six_alive = False
            else:
                if n == 3:
                    six_alive = True
                    
            # NINE --------------------
            
            if (0b1<<9)&mask == 0:
                nine_alive = False
            else:
                nine_alive = True
            
            nine = six << 3
            w = nine & mask
            
            n = 0
            while w != 0:
                w = w&(w-1)
                n += 1
            
            if nine_alive:
                if n != 2 and n != 3:
                    nine_alive = False
            else:
                if n == 3:
                    nine_alive = True
                    
            # TEN --------------------
            
            if (0b1<<10)&mask == 0:
                ten_alive = False
            else:
                ten_alive = True
            
            ten = nine << 1
            w = ten & mask
            
            n = 0
            while w != 0:
                w = w&(w-1)
                n += 1
            
            if ten_alive:
                if n != 2 and n != 3:
                    ten_alive = False
            else:
                if n == 3:
                    ten_alive = True
                    
            res = 0
            if five_alive:
                res = res | (0b1 << 5)
            if six_alive:
                res = res | (0b1 << 6)
            if nine_alive:
                res = res | (0b1 << 9)
            if ten_alive:
                res = res | (0b1 << 10)
            self._cache[self] = AbstractNode.node(
                nw=AbstractNode.cell(0b1<<10&res),
                ne=AbstractNode.cell(0b1<<9&res),
                sw=AbstractNode.cell(0b1<<6&res),
                se=AbstractNode.cell(0b1<<5&res))
            return self._cache[self]
            
        else:
            if l is not None:
                if l >= 0 and l <= self.level-2:
                    rnw = AbstractNode.node(
                        nw = self.nw.nw.se,
                        ne = self.nw.ne.sw,
                        sw = self.nw.sw.ne,
                        se = self.nw.se.sw
                        )
                    rne = AbstractNode.node(
                        nw = self.ne.nw.se,
                        ne = self.ne.ne.sw,
                        sw = self.ne.sw.ne, 
                        se = self.ne.se.nw
                        )
                    rtc = AbstractNode.node(
                        nw = self.nw.ne.se,
                        ne = self.ne.nw.sw, 
                        sw = self.ne.se.ne,
                        se = self.nw.sw.nw
                        )
                    rcl = AbstractNode.node(
                        nw = self.nw.sw.se, 
                        ne = self.nw.se.sw,
                        sw = self.sw.nw.ne, 
                        se = self.sw.ne.nw
                        )
                    rcr = AbstractNode.node(
                        nw = self.ne.sw.se, 
                        ne = self.ne.se.sw, 
                        sw = self.se.nw.ne,
                        se = self.se.ne.nw
                        )
                    
                    rsw = AbstractNode.node(
                        nw = self.sw.nw.se,
                        ne = self.sw.ne.sw,
                        sw = self.sw.sw.ne,
                        se = self.sw.se.nw)
                    
                    rbc = AbstractNode.node(
                        nw = self.sw.ne.se,
                        ne = self.se.nw.sw,
                        sw = self.sw.se.ne,
                        se = self.se.sw.nw)
                    
                    rse = AbstractNode.node(
                        nw = self.se.nw.se,
                        ne = self.se.ne.sw,
                        sw = self.se.sw.ne,
                        se = self.se.se.nw)
                    
                    rcc = AbstractNode.node(
                        nw = self.nw.se.se,
                        ne = self.ne.sw.sw,
                        sw = self.sw.ne.ne,
                        se = self.se.nw.nw)
                    
                    anw = AbstractNode.node(
                        nw = rnw, 
                        ne = rtc, 
                        sw = rcl, 
                        se = rcc
                        )
                    ane = AbstractNode.node(
                        nw = rtc, 
                        ne = rne, 
                        sw = rcc, 
                        se = rcr
                        )
                    
                    asw = AbstractNode.node(
                        nw = rcl,
                        ne = rcc,
                        sw = rsw,
                        se = rbc)
                    
                    ase = AbstractNode.node(
                        nw = rcc,
                        ne = rcr,
                        sw = rbc,
                        se = rse)
                    
                    C = AbstractNode.node(
                        nw = anw.forward(),
                        ne = ane.forward(), 
                        sw = asw.forward(), 
                        se = ase.forward()
                        )
                    
                    self._cache[self] = C
                    return self._cache[self]
    
            else:
                rnw = self.nw.forward()
                #self._cache.update(self.nw._cache)
                rne = self.ne.forward()
                #self._cache.update(self.ne._cache)
                rsw = self.sw.forward()
                #self._cache.update(self.sw._cache)
                rse = self.se.forward()
                #self._cache.update(self.se._cache)
                
                left = AbstractNode.node(
                    nw = self.nw.sw,
                    ne = self.nw.se,
                    sw = self.sw.nw,
                    se = self.sw.ne
                )
                
                right = AbstractNode.node(
                    nw = self.ne.sw,
                    ne = self.ne.se,
                    sw = self.se.nw,
                    se = self.se.ne
                    )
                
                top = AbstractNode.node(
                    nw = self.nw.ne,
                    ne = self.ne.nw,
                    sw = self.nw.se,
                    se = self.ne.sw
                    )
                
                bottom = AbstractNode.node(
                    nw = self.sw.ne,
                    ne = self.se.nw,
                    sw = self.sw.se,
                    se = self.se.sw
                    )
                
                center = AbstractNode.node(
                    nw = self.nw.se,
                    ne = self.ne.sw,
                    sw = self.sw.ne,
                    se = self.se.nw
                    )
                
                rcl = left.forward()
                #self._cache.update(left._cache)
                rcr = right.forward()
                #self._cache.update(right._cache)
                rtc = top.forward()
                #self._cache.update(top._cache)
                rbc  = bottom.forward()
                #self._cache.update(bottom._cache)
                
                rcc = center.forward()
                #self._cache.update(center._cache)
                
                anw = AbstractNode.node(
                    nw = rnw,
                    ne = rtc,
                    sw = rcl,
                    se = rcc
                    )
                
                ane = AbstractNode.node(
                    nw = rtc,
                    ne = rne,
                    sw = rcc,
                    se = rcr
                    )
                
                asw = AbstractNode.node(
                    nw = rcl, 
                    ne = rcc, 
                    sw = rsw, 
                    se = rbc
                    )
                
                ase = AbstractNode.node(
                    nw = rcc, 
                    ne = rcr, 
                    sw = rbc, 
                    se = rse
                    )
                
                C_nw = anw.forward()
                #self._cache.update(anw._cache)
                C_ne = ane.forward()
                #self._cache.update(ane._cache)
                C_sw = asw.forward()
                #self._cache.update(asw._cache)
                C_se = ase.forward()
                #self._cache.update(ase._cache)
                
                C = AbstractNode.node(
                    nw = C_nw,
                    ne = C_ne,
                    sw = C_sw,
                    se = C_se
                    )
                self._cache[self] = C
                
                return self._cache[self]
        
        
    def get(self, i, j):
        print(i, j, 'level', self.level)
        if self.level == 2:
            cells = {(0, 0):self.ne.sw, 
                     (0, 1):self.ne.nw,
                     (1, 1):self.ne.ne,
                     (1, 0):self.ne.se,
                     (-1, 0):self.nw.se,
                     (-2, 0):self.nw.sw,
                     (-2, 1):self.nw.nw,
                     (-1, 1):self.nw.ne,
                     (-1, -1):self.sw.ne,
                     (-2, -1):self.sw.nw,
                     (-2, -2):self.sw.sw,
                     (-1, -2):self.sw.se,
                     (0, -1):self.se.nw,
                     (1, -1):self.se.ne,
                     (0, -2):self.se.sw,
                     (1, -2):self.se.se
                     }
            if (i, j) in cells:
                if cells[(i, j)].population == 1:
                    return True
                else:
                    return False
            else:
                return False
        else:
            if i >= 0 and j >= 0:
                return self.ne.get(i-2**(self.level-2), j-2**(self.level-2))
            elif i >= 0 and j < 0:
                return self.se.get(i-2**(self.level-2), j+2**(self.level-2))
            elif i < 0 and j >= 0:
                return self.nw.get(i+2**(self.level-2), j-2**(self.level-2))
            elif i < 0 and j < 0:
                return self.sw.get(i+2**(self.level-2), j+2**(self.level-2))
                

                
class CellNode(AbstractNode):
    def __init__(self, alive):
        super().__init__()

        self._alive = bool(alive)
        self._hash = None

    level      = property(lambda self : 0)
    population = property(lambda self : int(self._alive))
    alive      = property(lambda self : self._alive)
    
    
    def __hash__(self):
        if self._hash is None:
            self._hash = (self._alive)
            self._hash = hash(self._hash)
        return self._hash
    
    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, AbstractNode):
            return False
        return \
            self.level      == other.level      and \
            self.population == other.population and \
            self.nw         is other.nw         and \
            self.ne         is other.ne         and \
            self.sw         is other.sw         and \
            self.se         is other.se
            
    
    
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
        self._hash = None
    
    def __hash__(self):
        if self._hash is None:
            self._hash = (
                self.population,
                self.level     ,
                self.nw        ,
                self.ne        ,
                self.sw        ,
                self.se        ,
            )
            self._hash = hash(self._hash)
        return self._hash
    
    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, AbstractNode):
            return False
        return \
            self.level      == other.level      and \
            self.population == other.population and \
            self.nw         is other.nw         and \
            self.ne         is other.ne         and \
            self.sw         is other.sw         and \
            self.se         is other.se

    level      = property(lambda self : self._level)
    population = property(lambda self : self._population)

    nw = property(lambda self : self._nw)
    ne = property(lambda self : self._ne)
    sw = property(lambda self : self._sw)
    se = property(lambda self : self._se)
    
    @staticmethod
    def level2_bitmask(mask):
        
        # FIVE --------------------
        
        # if bit number 5 is alive
        if (0b1<<5)&mask == 0:
            five_alive = False
        else:
            five_alive = True
            
        # word with only the neighbors of 5
        w = 0b11101010111 & mask 
        five = 0b11101010111
        
        # algo to determine how many neighbors are alive
        n = 0
        while w != 0:
            w = w&(w-1)
            n += 1
            
        # modify five's state accordingly 
        if five_alive:
            if n != 2 and n != 3:
                five_alive = False
        else:
            if n == 3:
                five_alive = True
                
        # SIX --------------------
        
        if (0b1<<6)&mask == 0:
            six_alive = False
        else:
            six_alive = True
        
        six = five << 1
        w = six & mask 
        
        n = 0
        while w != 0:
            w = w&(w-1)
            n += 1
        
        if six_alive:
            if n != 2 and n != 3:
                six_alive = False
        else:
            if n == 3:
                six_alive = True
                
        # NINE --------------------
        
        if (0b1<<9)&mask == 0:
            nine_alive = False
        else:
            nine_alive = True
        
        nine = six << 3
        w = nine & mask
        
        n = 0
        while w != 0:
            w = w&(w-1)
            n += 1
        
        if nine_alive:
            if n != 2 and n != 3:
                nine_alive = False
        else:
            if n == 3:
                nine_alive = True
                
        # TEN --------------------
        
        if (0b1<<10)&mask == 0:
            ten_alive = False
        else:
            ten_alive = True
        
        ten = nine << 1
        w = ten & mask
        
        n = 0
        while w != 0:
            w = w&(w-1)
            n += 1
        
        if ten_alive:
            if n != 2 and n != 3:
                ten_alive = False
        else:
            if n == 3:
                ten_alive = True
                
        res = 0
        if five_alive:
            res = res | (0b1 << 5)
        if six_alive:
            res = res | (0b1 << 6)
        if nine_alive:
            res = res | (0b1 << 9)
        if ten_alive:
            res = res | (0b1 << 10)
        
        return AbstractNode.node(
            nw=AbstractNode.cell(0b1<<10&res),
            ne=AbstractNode.cell(0b1<<9&res),
            sw=AbstractNode.cell(0b1<<6&res),
            se=AbstractNode.cell(0b1<<5&res))
        
        
            
        
        
    
    
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
        return self._root.get(i, j)
        
    def extend(self, k):
        k = self.level
        all_dead = True
        for i in range(-2**k, 2**k, 2**(k-1)):
            for j in range(-2**k, 2**k, 2**(k-1)):
                if self.get(i, j):
                    all_dead = False
                    break
            if not all_dead:
                break
        if (not all_dead) or self._root.level < max(k, 2):
            self._root.extend(k)
        

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
        
    
# import time
#gen, m, n, data = (1, 3, 1, [[True], [True], [True]])
# if isinstance(gen, int):
#     gen = [None] * gen 
    
    
#U = HashLifeUniverse(3, 1, [[True], [True], [True]])
#node = U.root
# #a = U.get(0,0)
# #print(a)
# node = HashLifeUniverse(3, 1, [[True], [True], [True]]).root
# node = node.extend()
# print('node: ', node)
# # for g in gen:
# #   for _ in range(1):         # see the log
# #     node = node.extend()
# #   node = node.forward(g) if g is not None else node.forward()
# start = time.time()
# for _ in range(10):
#     node.forward()
# end = time.time()

gen, m, n, data = ([0, 1, 2, 2, 1, 5, 4, 4], 3, 1, [[True], [True], [True]])# The test input data

if isinstance(gen, int):
  gen = [None] * gen

U = HashLifeUniverse(m, n, data)
print(U.root)
node = U.root
print(node)

for g in gen:
  for _ in range(1):         # see the log
      print('node in', node)
      node = node.extend()
  node = node.forward(g) if g is not None else node.forward()


# print('LALALALALLALALALA: ' ,(end-start))
    

#Uni = HashLifeUniverse(36, 9, [[False, False, False, True, True, False, False, False, False], [False, False, False, True, True, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, True, True, True, False, False, False, False], [False, True, False, False, False, True, False, False, False], [True, False, False, False, False, False, True, False, False], [True, False, False, False, False, False, True, False, False], [False, False, False, True, False, False, False, False, False], [False, True, False, False, False, True, False, False, False], [False, False, True, True, True, False, False, False, False], [False, False, False, True, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, True, True, True, False, False], [False, False, False, False, True, True, True, False, False], [False, False, False, True, False, False, False, True, False], [False, False, False, False, False, False, False, False, False], [False, False, True, True, False, False, False, True, True], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, True, True, False, False], [False, False, False, False, False, True, True, False, False]])
# n = Uni.root.ne.sw.population
#print(Uni.get(-18,-1))
# # print(node)
    




















