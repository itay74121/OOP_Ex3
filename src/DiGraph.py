from GraphInterface import GraphInterface
from Node import Node
from Position import Position


class DiGraph(GraphInterface):
    def __init__(self) -> None:
        super().__init__()
        self.nodes = {} # key to node
        self.mode_count = 0

    def v_size(self) -> int:
        return len(self.nodes)
    
    def e_size(self) -> int:
        s = 0
        for i in self.nodes:
            if type(self.nodes[i]) is Node:
                s += len(self.nodes[i].neighbors)
        return s
    
    def get_all_v(self) -> dict:
        return self.nodes
    
    def all_in_edges_of_node(self, id1: int) -> dict:
        d = {}
        for node in self.nodes:
            if(node.has_edge_to(id1)):
                d[node.key] = node.get_weight_to(id1)
        return d

    def all_out_edges_of_node(self, id1: int) -> dict:
        if(self.nodes.get(id1)):
            d =  {}
            for key in self.nodes.get(id1).neighbors_weights:
                d[key] = self.nodes.get(id1).neighbors_weights[key]
            return d
        else:
            return None
    def get_mc(self) -> int:
        return self.mode_count
    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if(weight<0):
            return False
        node1 = self.nodes.get(id1)
        node2 = self.nodes.get(id2)
        if(node1 and node2):
            node1.create_edge(node2,weight)
            node1.neighbors[id2] = node2
            node2.neighbors[id1] = node1
            return True
        else:
            return False
    def add_node(self, node_id: int, pos: tuple) -> bool:
        keys = [i for i in self.nodes]
        if(node_id not in keys):
            n = Node(node_id,Position(pos[0],pos[1],pos[2]))
            self.nodes[node_id] = n
            return True
        else:
            return False
    def remove_node(self, node_id: int) -> bool:
        n = self.nodes.get(node_id)
        if(n):
            n.disconnect_all()
            del self.nodes[node_id]
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        node1 = self.nodes.get(node_id1)
        node2 = self.nodes.get(node_id2)
        if(node1 and node2):
            if(node1.has_edge_to(node_id2)):
                del node1.neighbors_weights[node_id2]
                if (not node2.has_edge_to(node_id1)):
                    del node1.neighbors[node_id2]
                    del node2.neighbors[node_id1]
                return True
            else:
                return False
        else:
            return False
    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        s = ""
        for key in self.nodes:
            s += str(self.nodes[key])
            for nkey in self.nodes[key].neighbors:
                s += str(self.nodes[key].neighbors[nkey])+" "
            s+="\n"
        return s


def main():
    g = DiGraph()



if __name__ == "__main__":
    main()












