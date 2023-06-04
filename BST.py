from Util import *


class BSTNode:
    def __init__(self, node: Node):
        self.node = node
        self.left = None
        self.right = None
        node.bstnode = self

    def __str__(self):
        return "(BSTN)" + self.node.__str__()


class BST:
    def __init__(self, root: BSTNode = None):
        self.root = root
        self.block_class = BlockClass()

    def __str__(self):
            return "BST:" + self.block_class.__str__()

    def addNode(self, node: Node):
        bstnode = BSTNode(node)
        if self.root is None:
            self.root = bstnode
        else:
            self.addNodeHelper(self.root, bstnode)

        self.block_class.addSingletonBlock(node)

    def addNodeHelper(self, parent: BSTNode, target: BSTNode):
        if target.node.value < parent.node.value:
            if parent.left is not None:
                self.addNodeHelper(parent.left, target)
            else:
                parent.left = target
        else:
            if parent.right is not None:
                self.addNodeHelper(parent.right, target)
            else:
                parent.right = target

    def isotonicRegression(self):
        if self.root is None:
            return
        self.block_class.blocks = self.isotonicRegressionHelper(solution=[], unsolved=[self.root])

    def isotonicRegressionHelper(self, solution: [], unsolved: []):  # Block{} solution, BSTNode{} unsolved
        rights = set()
        temp = unsolved.pop()
        while temp is not None:
            rights.add(temp.node)
            if temp.left is not None:
                unsolved.append(temp.left)
            temp = temp.right

        temp_block = Block(*rights)
        if len(solution) > 0:
            parent_block = solution[-1]
            if parent_block.key < temp_block.key:
                parent_block.absorb(temp_block)
            else:
                solution.append(temp_block)
        else:
            solution.append(temp_block)

        if len(unsolved) == 0:
            return set(solution)
        else:
            return self.isotonicRegressionHelper(solution, unsolved)
