from Position import Position
from Edge import Edge

class Node:
    def __init__(self,key:int,pos:Position):
        self.key = key
        self.neighbors = {} # key to neighbor
        self.neighbors_weights = {} # key to edge to that nieghbor
        self.weight = 0
        self.pos = pos
    """
    This method is for adding another Node as a neighbor.
    this method will override existing Node object with similar key.
    @return: true or flase
    """
    def add_neighbor(self,other):
        if(type(other)is Node):
            self.neighbors[other.key] = other
            return True # since success
        else:
            return False # since other is not of type Node
    """
    This method creates an edge between two nodes. and 
    @return true or false
    """
    def create_edge(self,other,weight:float):
        if(type(other) is Node):
            self.neighbors_weights[other.key] = Edge(self.key,other.key,weight)
            self.add_neighbor(other)
            return True
        else:
            return False

    def __eq__(self, o: object) -> bool:
        if type(o) is not Node:
            return False
        if(self.key == o.key):
            for key in self.neighbors_weights:
                if(o.neighbors_weights.get(key) != self.neighbors_weights[key]):
                    return False
            for key in o.neighbors_weights:
                if(o.neighbors_weights.get(key) != self.neighbors_weights.get(key)):
                    return False
            return True
        else:
            return False
    def has_edge_to(self,key:int):
        return self.neighbors_weights.get(key)!=None
    def get_weight_to(self,key:int):
        if(self.has_edge_to(key)):
            return self.neighbors_weights[key].getweight()
        else:
            return -1
    
    def disconnect_all(self):
        for key in self.neighbors:
            del self.neighbors_weights[key]
            del self.neighbors[key].neighbors[self.key]
            del self.neighbors[key].neighbors_weights[self.key]
        self.neighbors.clear()
        self.neighbors_weights.clear()
        
    def __hash__(self):
        return self.key
    def __str__(self) -> str:
        return f"[Node {self.key}]"
    def __repr__(self) -> str:
        return self.__str__()