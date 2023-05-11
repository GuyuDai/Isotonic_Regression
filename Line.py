from Util import *


class LineNode:
    def __init__(self, node: Node):
        self.node = node
        self.nex = None
        node.lnode = self

    def __str__(self):
        return "(LN)" + self.node.__str__()


class Line:
    def __init__(self, first: LineNode = None):
        self.first = first
        self.block_class = BlockClass()

    def __str__(self):
        return "Line:" + self.block_class.__str__()

    def addNode(self, node: Node):
        lnode = LineNode(node)
        if self.first is None:
            self.first = lnode
        else:
            self.addNodeHelper(self.first, lnode)

        self.block_class.addSingletonBlock(node)

    def addNodeHelper(self, pre: LineNode, target: LineNode):
        if pre.nex is None:
            pre.nex = target
        else:
            self.addNodeHelper(pre.nex, target)

    def getLineNodeByNode(self, target: Node):  # use node.toSpecific() don't use this method!!
        if (self.first is None) or (target is None):
            return None
        elif target is self.first.node:
            return self.first
        else:
            return self.getLineNodeByNodeHelper(self.first.nex, target)

    def getLineNodeByNodeHelper(self, lnode: LineNode, target: Node):
        if lnode is None:
            return None
        elif lnode.node is target:
            return lnode
        else:
            return self.getLineNodeByNodeHelper(lnode.nex, target)

    def getSon(self, block: Block):  # either None or only one block
        children_of_block = set()
        for node in block.nodes:
            lnode = node.toSpecific()
            if lnode.nex is not None:
                children_of_block.add(lnode.nex.node)
            else:
                children_of_block.add(None)
        children_of_block -= block.nodes  # Node{}
        uniq_child = children_of_block.pop()
        if uniq_child is None:
            return None
        else:
            return self.block_class.getBlockByNode(uniq_child)

    def getParent(self, block: Block, temp: LineNode = None):  # usage: line.getParent(block)
        if temp is None:
            temp = self.first
        if (self.first in block.nodes) or (temp.nex is None):
            return None
        elif (temp.nex.node in block.nodes) and not (temp in block.nodes):
            return self.block_class.getBlockByNode(temp.node)
        else:
            return self.getParent(block, temp.nex)

    def isotonicRegression(self):
        done = False
        without_first = self.block_class.blocks.copy()  # Block{}
        without_first.remove(self.block_class.getBlockByNode(self.first.node))  # Block{}
        if len(without_first) == 0:
            return
        b = without_first.pop()
        del without_first
        while not done:
            s = self.getSon(b)
            p = self.getParent(b)
            # print(b, s, p)  # for testing
            if (s is not None) and (b.key < s.key):
                self.block_class.merge(to=b, b=s)
            elif (p is not None) and (b.key > p.key):
                self.block_class.merge(to=b, b=p)
            elif (p is not None) and (b.key <= p.key):
                b = p
            else:
                done = True
