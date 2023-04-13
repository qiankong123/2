# 双向链表

# Define the Node class for the doubly linked list
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

# Define the DoublyLinkedList class
class DoublyLinkedList:
    def __init__(self):
        self.head = None

    # Method to insert a new node in the doubly linked list
    def insert(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        elif self.head.data > data:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        else:
            current = self.head
            while current.next is not None and current.next.data < data:
                current = current.next
            new_node.next = current.next
            if current.next is not None:
                current.next.prev = new_node
            current.next = new_node
            new_node.prev = current

    # Method to print the doubly linked list
    def print_list(self):
        current = self.head
        while current is not None:
            print(current.data)
            current = current.next

# Create a new doubly linked list
dll = DoublyLinkedList()

# Insert the given data into the doubly linked list
dll.insert(18)
dll.insert(34)
dll.insert(1)
dll.insert(44)
dll.insert(65)
dll.insert(66)
dll.insert(68)

# Print the doubly linked list
dll.print_list()
