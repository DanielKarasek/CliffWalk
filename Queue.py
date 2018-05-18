class Queue:

    def __init__(self):
        self.top = None

        
    def push(self,value):
        if self.isEmpty():
            node = Node(value)
            self.top = node
        else:
            node = Node(value)
            node.setNext(self.top)
            self.top = node

    def isEmpty(self):
        if self.top == None:
            return True
        else: return False

    def pop(self):
        if self.isEmpty():
            return None
        else:
            n = self.top
            self.top = n.getNext()
            return n

class Node:
    
    def __init__(self,value):
        self.value = value
        self.next = None

    def isLast(self):
        if self.next == None:
            return True
        else:
            return False

    def getNext(self):
        return self.next

    def getValue(self):
        return self.value

    def setNext(self,node):
        self.next = node
    
    def setValue(self,value):
        self.value = value

        
