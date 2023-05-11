
class Node:
    def __init__(self, tag, value, weight=1):
        self.tag = tag  # String tag = x1
        self.value = value  # float value
        self.weight = weight  # double weight

        self.tnode = None
        self.bstnode = None
        self.lnode = None

    def __str__(self):
        return f"{self.tag}:v={self.value},w={self.weight}"

    def toSpecific(self):
        if self.tnode is not None:
            return self.tnode
        if self.bstnode is not None:
            return self.bstnode
        if self.lnode is not None:
            return self.lnode
        raise Exception("no subclass instance")


class Block:
    def __init__(self, *nodes):
        if len(nodes) == 0 or nodes is None:
            raise Exception("invalid input, nodes should not be empty!")
        else:
            self.nodes = set(nodes)  # Nodes{} nodes
            self.key = self.av()

    def __str__(self):
        result = f'B(Av={self.key})' + "{\n"
        for node in self.nodes:
            result = result + str(node) + ";\n"
        result += "}"
        return result

    def absort(self, other):  # merge two blocks into one
        if not isinstance(other, Block):
            raise Exception("invalid input, expect a Block")
        else:
            self.nodes.update(other.nodes)
            self.key = self.av()

    def av(self):  # weighted average
        w = 0
        wsum = 0
        for node in self.nodes:
            w += node.weight
            wsum += node.weight * node.value
        if w == 0:
            return float('-inf')
        return float(wsum / w)


class BlockClass:
    def __init__(self):
        self.blocks = set()

    def __str__(self):
        result = "{\n"
        for block in self.blocks:
            result = result + block.__str__() + ";\n"
        result += "}"
        return result

    def valid(self, dataset: set):  # Node{} dataset
        temp = set()
        for block in self.blocks:
            if len(temp.intersection(block.nodes)) != 0:
                return False
            else:
                temp.update(block.nodes)
        return len(temp ^ dataset) == 0

    def addSingletonBlock(self, node: Node):
        self.blocks.add(Block(node))

    def add(self, b: Block):
        self.blocks.add(b)

    def getBlockByNode(self, target: Node):
        for block in self.blocks:
            if target in block.nodes:
                return block
        return None

    def getNodeByTag(self, target: str):
        for block in self.blocks:
            for node in block.nodes:
                if target == node.tag:
                    return node
        return None

    def getBlockByTag(self, target: str):
        target_node = self.getNodeByTag(target)
        return self.getBlockByNode(target_node)

    def merge(self, to: Block, b: Block):
        to.absort(b)
        self.blocks.remove(b)


class BHNode:
    def __init__(self, block: Block = None, degree: int = 0, parent=None, child=None,
                 sibling=None):
        self.block = block
        self.degree = degree  # number of nodes = 2 ** degree, degree: 0~inf
        self.parent = parent
        self.child = child  # link tree
        self.sibling = sibling  # other BHNodes in the same tree and at the same level, or the other heads

    def __str__(self):
        return self.block.__str__()


class BinomialHeap:  # max heap!!
    def __init__(self, head: BHNode = None):
        self.head = head

    @classmethod
    def link(cls, t: BHNode, to: BHNode):  # link to binomial tree with same degree k to one k+1 degree tree
        t.parent = to
        t.sibling = to.child
        to.child = t
        to.degree += 1

    def getMax(self):  # public Block getMax()
        result = None
        temp = self.head
        temp_max = float('-inf')
        while temp is not None:
            if temp.block.key > temp_max:
                temp_max = temp.block.key
                result = temp
            temp = temp.sibling
        return result

    def extractMax(self):  # usage: self = self.extractMax()
        result = None
        p = self.head
        x = None
        x_prev = None
        p_prev = None
        if p is None:
            result = BinomialHeap()
            return result
        x = p
        temp_max = p.block.key
        p_prev = p
        p = p.sibling
        while p is not None:
            if p.block.key > temp_max:
                x_prev = p_prev
                x = p
                temp_max = p.block.key
            p_prev = p
            p = p.sibling
        if x == self.head:
            self.head = x.sibling
        elif x.sibling is None:
            x_prev.sibling = None
        else:
            x_prev.sibling = x.sibling
        child_x = x.child
        if child_x is not None:
            h1 = BinomialHeap()
            child_x.parent = None
            h1.head = child_x
            p = child_x.sibling
            child_x.sibling = None
            while p is not None:
                p_prev = p
                p = p.sibling
                p_prev.sibling = h1.head
                h1.head = p_prev
                p_prev.parent = None
            result = BinomialHeap.union(self, h1)
        return result

    @classmethod
    def changeKey(cls, new: Block, target: BHNode):
        target.block = new
        temp = target
        parent = target.parent
        while (parent is not None) and (temp.block.key > parent.block.key):
            temp.block = parent.block
            parent.block = new
            temp = parent
            parent = temp.parent

    @classmethod
    def union(cls, h1, h2):  # usage: self = BinomialHeap.union(h1, h2)
        result = BinomialHeap()
        p = None
        p1 = h1.head
        p2 = h2.head
        if p1 is None:
            return h2
        if p2 is None:
            return h1
        # part1: create a queue of binomial trees
        if p1.degree < p2.degree:
            result.head = p1
            p = result.head
            p1 = p1.sibling
        else:
            result.head = p2
            p = result.head
            p2 = p2.sibling
        while (p1 is not None) and (p2 is not None):
            if p1.degree < p2.degree:
                p.sibling = p1
                p = p1
                p1 = p1.sibling
            else:
                p.sibling = p2
                p = p2
                p2 = p2.sibling
        if p1 is not None:
            p.sibling = p1
        else:
            p.sibling = p2
        # part2: linking the trees with same degree
        pre = None
        x = result.head
        nex = x.sibling
        while nex is not None:
            if x.degree != nex.degree or (nex.sibling is not None and x.degree == nex.sibling.degree):
                pre = x
                x = nex
            elif x.block.key >= nex.block.key:
                x.sibling = nex.sibling
                result.link(nex, x)
            else:
                if pre is None:
                    result.head = nex
                else:
                    pre.sibling = nex
                result.link(x, nex)
            nex = x.sibling
        return result

    def add(self, block: Block):
        node = BHNode(block=block)
        h1 = BinomialHeap()
        h1.head = node
        return BinomialHeap.union(self, h1)
