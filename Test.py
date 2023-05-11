import random

from Tree import *
from BST import *
from Line import *


def generator(target, num: int):
    result = []
    for i in range(1, num + 1):
        result.append(Node("node" + str(i), i + random.gauss(0, 2)))
    if isinstance(target, Line) or isinstance(target, BST):
        for node in result:
            target.addNode(node)
    if isinstance(target, Tree):
        marked = set()
        for node in result:
            if len(marked) == 0:
                target.addNode(node)
            else:
                parent = random.sample(marked, 1)[0]
                target.addNode(node, parent)
            marked.add(node)
    if not (isinstance(target, Tree) or isinstance(target, BST) or isinstance(target, Line)):
        raise Exception("wrong input data type")

    return set(result)


ln1 = Node("ln1", 6)
ln2 = Node("ln2", 0)
ln3 = Node("ln3", 2)
ln4 = Node("ln4", 4)
ln5 = Node("ln5", 3)

l = Line()
l.addNode(ln1)
l.addNode(ln2)
l.addNode(ln3)
l.addNode(ln4)
l.addNode(ln5)

lset = {ln1, ln2, ln3, ln4, ln5}

l.isotonicRegression()
print("Test-Line: \n" + str(l.block_class))
print("valid: " + str(l.block_class.valid(lset)))
#####################################################################################################################
bn1 = Node("bn1", 15)
bn2 = Node("bn2", 8)
bn3 = Node("bn3", 23)
bn4 = Node("bn4", 5)
bn5 = Node("bn5", 11)
bn6 = Node("bn6", 20)
bn7 = Node("bn7", 29)
bn8 = Node("bn8", 4)
bn9 = Node("bn9", 7)
bn10 = Node("bn10", 10)
bn11 = Node("bn11", 13)
bn12 = Node("bn12", 18)
bn13 = Node("bn13", 21)
bn14 = Node("bn14", 24)
bn15 = Node("bn15", 30)

bst = BST()
bst.addNode(bn1)
bst.addNode(bn2)
bst.addNode(bn3)
bst.addNode(bn4)
bst.addNode(bn5)
bst.addNode(bn6)
bst.addNode(bn7)
bst.addNode(bn8)
bst.addNode(bn9)
bst.addNode(bn10)
bst.addNode(bn11)
bst.addNode(bn12)
bst.addNode(bn13)
bst.addNode(bn14)
bst.addNode(bn15)

bstset = {bn1, bn2, bn3, bn4, bn5, bn6, bn7, bn8, bn9, bn10, bn11, bn12, bn13, bn14, bn15}

bst.isotonicRegression()
print("Test-BST: \n" + str(bst.block_class))
print("valid: " + str(bst.block_class.valid(bstset)))
########################################################################################################################
tn1 = Node("x1", 7)
tn2 = Node("x2", 5)
tn3 = Node("x3", 8)
tn4 = Node("x4", 0)
tn5 = Node("x5", 3)
tn6 = Node("x6", 6)
tn7 = Node("x7", 10)
tn8 = Node("x8", 3)
tn9 = Node("x9", 4)
tn10 = Node("x10", 2)
tn11 = Node("x11", 8)
tn12 = Node("x12", 5)
tn13 = Node("x13", 7)
tn14 = Node("x14", 2)
tn15 = Node("x15", 10)

t = Tree()
t.addNode(tn1)
t.addNode(tn2, tn1)
t.addNode(tn3, tn1)
t.addNode(tn4, tn2)
t.addNode(tn5, tn2)
t.addNode(tn6, tn3)
t.addNode(tn7, tn3)
t.addNode(tn8, tn4)
t.addNode(tn9, tn4)
t.addNode(tn10, tn5)
t.addNode(tn11, tn5)
t.addNode(tn12, tn6)
t.addNode(tn13, tn6)
t.addNode(tn14, tn7)
t.addNode(tn15, tn7)

tset = {tn1, tn2, tn3, tn4, tn5, tn6, tn7, tn8, tn9, tn10, tn11, tn12, tn13, tn14, tn15}

t.isotonicRegression()
print("Test-Tree: \n" + str(t.block_class))
print("valid: " + str(t.block_class.valid(tset)))
########################################################################################################################
lt = Tree()
lt.addNode(ln1)
lt.addNode(ln2, ln1)
lt.addNode(ln3, ln2)
lt.addNode(ln4, ln3)
lt.addNode(ln5, ln4)

lt.isotonicRegression()
print("Test-LTree: \n" + str(lt.block_class))
print("valid: " + str(t.block_class.valid(lset)))

########################################################################################################################
ll = Line()
llset = generator(ll, 1)
ll.isotonicRegression()
print("BigData-Test: \n" + str(ll.block_class))
print("valid: " + str(ll.block_class.valid(llset)))