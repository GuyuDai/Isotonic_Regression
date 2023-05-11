from collections import deque

from Util import *


class TreeNode:
    def __init__(self, node: Node):
        self.node = node
        self.children = []  # TreeNode[]
        node.tnode = self

        self.solved = True

    def __str__(self):
        return "(TN)" + self.node.__str__()

    def has_next(self):
        return len(self.children) != 0


class Tree:
    def __init__(self, root: TreeNode = None):
        self.root = root
        self.block_class = BlockClass()

    def __str__(self):
        return "Tree:" + self.block_class.__str__()

    def getTreeNodeByNode(self, target: Node):  # use node.toSpecific() don't use this method!!
        if (self.root is None) or (target is None):
            return None
        elif target is self.root.node:
            return self.root
        else:
            return self.getTreeNodeByNodeHelper(self.root.children, target)

    def getTreeNodeByNodeHelper(self, tnodes: list, target: Node):
        next_level = []
        for tnode in tnodes:
            if target is tnode.node:
                return tnode
            else:
                next_level += tnode.children
        if len(next_level) == 0:
            return None
        else:
            return self.getTreeNodeByNodeHelper(next_level, target)

    def addNode(self, node: Node, parent: Node = None):
        tparent = None
        if parent is not None:
            tparent = parent.toSpecific()
        tnode = TreeNode(node)
        if (self.root is None) and (tparent is None):
            self.root = tnode
        elif (self.root is not None) and (tparent is not None):
            tparent.children.append(tnode)
            tparent.solved = False
        else:
            raise Exception("invalid input, the parent is empty or no such parent in this tree")

        self.block_class.addSingletonBlock(node)

    def getSons(self, block: Block):
        children_of_block = {child for node in block.nodes for child in
                             node.toSpecific().children}  # TreeNode{}
        children_of_block_without_self = {child.node for child in children_of_block} - block.nodes  # Node{}
        sons = {self.block_class.getBlockByNode(node) for node in children_of_block_without_self}
        return sons

    def blockToBH(self, block: Block):
        result = BinomialHeap()
        blocks = self.getSons(block)
        blocks.add(block)
        for b in blocks:
            result = result.add(b)
        return result

    def order(self):
        temp = deque([])  # queue of all nodes
        wait_list = []  # stack of nodes which are not immediately to be solved
        to_solve = []  # stack of nodes whose children are all solved
        if self.root is None:
            return []
        temp.append(self.root)
        while len(temp) > 0:
            pointer = temp.popleft()
            flag = True
            for tn in pointer.children:
                if not tn.solved:
                    temp.append(tn)
                    flag = False
            if flag:
                to_solve.append(pointer)
            else:
                wait_list.append(pointer)
        return wait_list + to_solve  # result is a stack, using pop() is the right order

    def isotonicRegression(self):
        if (self.root is None) or (len(self.root.children) == 0):
            return
        to_solve = self.order()
        # print('\n'.join(str(obj) for obj in to_solve))  # correct
        while len(to_solve) > 0:
            pointer = to_solve.pop()
            # print(pointer)  # correct
            p_block = self.block_class.getBlockByNode(pointer.node)
            # print(p_block)  # correct
            p_heap = self.blockToBH(p_block)
            # print(p_heap.head.block)    # for testing
            while p_block.key < p_heap.getMax().block.key:
                block_k = p_heap.getMax()
                self.block_class.merge(to=p_block, b=block_k.block)
                p_heap = self.blockToBH(p_block)