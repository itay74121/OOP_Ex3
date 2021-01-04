from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from GraphInterface import GraphInterface
from json import loads,dump
from Position import Position
from Node import Node
from collections import defaultdict
from typing import List

class GraphAlgo(GraphAlgoInterface):
    def __init__(self,graph=None) -> None:
        self.graph = graph
        self.Time = 0
        self.scc = 0
        self.scc_list = defaultdict(list)
    
    def get_graph(self) -> GraphInterface:
        return self.graph
    
    def load_from_json(self, file_name: str) -> bool:
        d = None
        with open(file_name,"r") as file:
            d = loads(file.read())
        if(d):
            g = DiGraph()
            for di in d["Nodes"]:
                if type(di) is dict:
                    pos = di.get("pos")
                    id  = di.get("id")
                    if pos and id:
                        id = int(id)
                        x,y,z=[float(i) for i in pos.split(",")]
                        pos = (x,y,z)
                        g.add_node(id,pos)
                    else:
                        continue
            for di in d["Edges"]:
                if type(di) is dict:
                    src = di.get("src")
                    w = di.get("w")
                    dest = di.get("dest")
                    if src and w and dest:
                        src = int (src)
                        w = float(w)
                        dest = int(dest)
                        g.add_edge(src,dest,w)
                    else:
                        continue
            self.graph = g
            return True
        else:
            return False
    def save_to_json(self, file_name: str) -> bool:
        if self.graph and type(self.graph) is DiGraph:
            d = {"Edges":[],"Nodes":[]}
            for key in self.graph.nodes:
                di = {}
                di ["id"] = self.graph.nodes[key].key
                di ["pos"] = str(self.graph.nodes[key].pos)
                d["Nodes"].append(di)
                di = {}
                for nikey in self.graph.nodes[key].neighbors_weights:
                    di["src"] = key
                    di["dest"] = nikey
                    di ["w"] = self.graph.nodes[key].neighbors_weights[nikey].getweight()
                    d["Edges"].append(di)
            with open(file_name,"w") as file:
                dump(d,file,indent=4 )
            return True
        else:
            return False

    def SCCUtil(self,u:Node, low:dict, disc:dict, stackMember:dict, st): 
        disc[u] = self.Time 
        low[u] = self.Time 
        self.Time += 1
        stackMember[u] = True
        st.append(u) 
    
        for vkey in u.neighbors_weights: 
            v = u.neighbors[vkey]
            if disc.get(v) == None: 
                self.SCCUtil(v, low, disc, stackMember, st)
                low[u] = min(low[u], low[v]) 
            elif stackMember.get(v):  
                low[u] = min(low[u], disc[v]) 
            else:
                low[u] = min(low[u],low[v])
        w = -1 
        if low[u] == disc[u]: 
            self.scc += 1
            while w != u: 
                w = st.pop() 
                stackMember[w] = False
                self.scc_list[self.scc].append(w)

    def SCC(self): 
        self.Time = 0
        disc =  {}
        low =  {}
        stackMember = {}
        st =[] 
        self.scc = 0
        self.scc_list = defaultdict(list)
        for node_key in self.graph.nodes:
            if disc.get(self.graph.nodes[node_key]) == None: 
                self.SCCUtil(self.graph.nodes[node_key], low, disc, stackMember, st) 
    def connected_component(self,id1:int) -> list:
        if (self.graph.nodes.get(id1)==None):
            return [] # empty list symbolizes that node is not in the graph 
        node = self.graph.nodes[id1]
        self.SCC()
        ret = None
        for i in self.scc_list:
            if(node in self.scc_list[i]):
                ret = self.scc_list[i]
                break
        return ret

    def connected_components(self) -> List[list]:
        self.SCC()
        l = []
        for i in self.scc_list:
            l.append(self.scc_list[i])
        return l
    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if not self.graph:
            return None
        if self.graph.contains(id1,id2):
            src = self.graph.nodes.get(id1)
            dest = self.graph.nodes.get(id2)
            parent = {} # parent dictionary 
            stack = [src] # init the stack with the src
            for key in self.graph.nodes: # iterate over nodes and set weights to -1
                self.graph.nodes[key].weight = -1
            src.weight = 0 # set src weight to 0
            while(len(stack)!=0): # as long as the stack isn't empty 
                node = stack.pop() # pop a node out of the stack 
                for ni_key in node.neighbors_weights: # iterate over the edges that go out of the node
                    if node.neighbors[ni_key].weight == -1: #means we never reached it
                        node.neighbors[ni_key].weight = node.neighbors_weights[ni_key].getweight()+node.weight
                        stack.append(node.neighbors[ni_key])
                        stack.sort(key=lambda x: x.weight,reverse=True)
                        parent[ node.neighbors[ni_key]] = node
                    elif node.neighbors[ni_key].weight > node.neighbors_weights[ni_key].getweight()+node.weight:   
                        node.neighbors[ni_key].weight = node.neighbors_weights[ni_key].getweight()+node.weight
                        stack.sort(key=lambda x: x.weight,reverse=True)
                        parent[ node.neighbors[ni_key]] = node
            # once finished the algorithm 
            # should check if we reached the dest 
            # check if dest is in parent dict
            if parent.get(dest) == None: # means we never reached it 
                #thus return None
                return None
            else: # means we reached it so we should trace the path back 
                n = dest
                l = []
                while(parent[n]!=src):
                    l.append(n)
                    n = parent[n]
                l.append(n)
                l.append(parent[n])
                l.reverse()
                return (dest.weight,l)



def main():
    g = DiGraph()
    g.add_node(1,(0,0,0))
    g.add_node(2,(0,0,0))
    g.add_node(3,(0,0,0))
    g.add_node(4,(0,0,0))
    g.add_node(5,(0,0,0))
    g.add_node(6,(0,0,0))

    g.add_edge(1,2,5)
    g.add_edge(2,3,5)
    g.add_edge(3,4,5)
    g.add_edge(4,1,5)
    g.add_edge(3,6,5)

    ga = GraphAlgo(g)
    #ga.load_from_json("./data/A1")
    print(ga.connected_component(6))
    print(ga.connected_components())
    print(ga.shortest_path(1,6))



if  __name__ == "__main__":
    main()