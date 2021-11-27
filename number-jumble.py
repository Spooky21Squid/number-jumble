#!/usr/bin/env python3

import re

"""
You get a string of 'random' letters, like: oaadnggeghthwhtohtthrtthehe.
Hidden in that string are numbers, in word form, e.g. above: one two three.
Find the number in the string.
Assumes they don't overlap.

get1() uses Regex to find the first occurence of a number.
get2() gradually builds a tree of correct, incomplete words, with an empty string as the root. Each word is a
branch. Once a word is found (a branch is completed), it resets the tree and keeps going to find the rest.

E.g.              ""
                /    \
               o      t
               |     /  \
               n    w    h
               |         |
               e         r    -> one is completed, so is added to the result number string

I think this can be used to find overlapping instances if the tree isn't reset each time a word is found, and
a counter is introduced so found numbers aren't repeated.

Also, in the case of "othrene", one and three are found at the same time. It just picks the number that started first.
"""

class Node:
    def __init__(self, data) -> None:
        self.data = data
        self.children = list()
    

    def addChild(self, node):
        self.children.append(node)
    

    def deleteSelf(self):
        """deletes this node and its children from the tree"""
        self.deleteChildren()
        del self

    
    def deleteChildren(self):
        """deletes all children of this node"""
        for c in self.children:
            c.deleteSelf()


class Tree:
    def __init__(self, root:Node, words:set) -> None:
        self.root = root
        self.allowedWords = words
        self.foundWord = ""
    

    def addRecursive(self, l, node, word):
        """Recursively checks if a letter can be added to the tree. If it can it adds it"""

        word += node.data
        letterIsChild = False
        for c in node.children:
            if c.data == l:
                letterIsChild = True
            self.addRecursive(l, c, word)
        
        if not letterIsChild:
            # check if it can be added
            for w in self.allowedWords:
                if len(word) < len(w) and w.startswith(word):
                    if w[len(word):][0] == l:
                        node.addChild(Node(l))
                        if word + l == w:
                            self.foundWord = w
                        break
    

    def add(self, l:str):
        """Adds letter l to the tree based on the allowed words"""
        self.addRecursive(l, self.root, "")


    def check(self):
        """Checks if there is a full word in the tree. If yes, returns that word. If no, returns empty string"""
        return self.foundWord
    

    def reset(self):
        """Deletes all nodes, except the root node"""
        self.root.deleteChildren()
        self.foundWord = ""


def textToNumber(t:str, intFlag=0):
    """Converts the text representation of a one-digit number to its integer form. If intFlag is set to 1, returns the number
    as an integer instead of a string. Returns None if no number found.
    
    Assumes all the letters are there, as this only checks hte first and last letter. My use case doesn't need to
    check all the letters (get1 method).
    """
    n = ""

    if t[0] == "z":
        n = "0"
    if t[0] == "o":
        n = "1"
    if t[0] == "e":
        n = "8"
    if t[0] == "n":
        n = "9"
    if t[0] == "t":
        if t[-1] == "o":
            n = "2"
        if t[-1] == "e":
            n = "3"
    if t[0] == "f":
        if t[-1] == "e":
            n = "5"
        if t[-1] == "r":
            n = "4"
    if t[0] == "s":
        if t[-1] == "n":
            n = "7"
        if t[-1] == "x":
            n = "6"
    
    if n == "":
        return None

    if intFlag:
        return int(n)
    else:
        return n


def get2(s, words={"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"}):
    tree = Tree(Node(""), words)
    n = ""  # The resulting number
    r = re.sub("a|b|c|d|j|k|l|m|p|q|y", "", s) # Remove all redundant letters

    for l in r:
        tree.add(l)
        x = tree.check()
        if x:
            n = n + textToNumber(x)
            tree.reset()
    
    if n:
        return n
    else:
        return None


def get1(s):

    r = re.sub("a|b|c|d|j|k|l|m|p|q|y", "", s) # Remove all redundant letters

    """
    METHOD
    check if theres any of the numbers in there using regex pattern p
    find the first occurence of that match
    find that number by using the first and last letters (for each number, the combination of the two is unique)
    add to number string
    remove that part from the string
    repeat until no matches found
    """

    n = ""
    p = ".*?(z.*?e.*?r.*?.*?o)|(o.*?n.*?e)|(t.*?w.*?o)|(t.*?h.*?r.*?e.*?e)|(f.*?o.*?u.*?r)|(f.*?i.*?v.*?e)|(s.*?i.*?x)|(s.*?e.*?v.*?e.*?n)|(e.*?i.*?g.*?h.*?t)|(n.*?i.*?n.*?e)"

    while True:
        m = re.search(p, r)
        if not m:
            break

        t = r[m.start():m.end()]

        # Decide which number it is
        n = n + textToNumber(t)
        
        r = r[m.end():]
    
    if n:
        return n
    else:
        return None


s = "oaadnggeghthwhtohtthrtthehe"
t = "othrene"

#print(get1(s))
print(get2(s))
