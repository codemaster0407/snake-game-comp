# import deque 

class CustomQueue:
    def __init__(self):
        self.node_queue = []
        self.visited_nodes = []
    
    def enqueue(self, node_value):
        self.node_queue.append(node_value)
    
    def dequeue_node(self):
       if len(self.node_queue) > 0:
        return self.node_queue.pop(0)
       else:
          return None 
    
# if __name__ == "__main__":
#     q = CustomQueue()

#     q.push_queue((1,2))
#     q.push_queue((2,3))
#     print(q.node_queue)
#     print(q.dequeue_node())
#     print(q.dequeue_node())
#     print(q.dequeue_node())