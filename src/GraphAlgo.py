from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from GraphInterface import GraphInterface
from json import loads,dump
from Position import Position

class GraphAlgo(GraphAlgoInterface):
    def __init__(self,graph=None) -> None:
        self.graph = graph
        self.discovery = [-1 for i in self.graph.nodes]
        self.lower = [-1 for i in self.graph.nodes]
        self.Time = 0
        self.stack = [False for i in self.graph.nodes]
    
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
    def SCCUtil(self,u, low, disc, stackMember, st): 
  
        # Initialize discovery time and low value 
        disc[u] = self.Time 
        low[u] = self.Time 
        self.Time += 1
        stackMember[u] = True
        st.append(u) 
  
        # Go through all vertices adjacent to this 
        for v in self.graph[u]: 
              
            # If v is not visited yet, then recur for it 
            if disc[v] == -1 : 
              
                self.SCCUtil(v, low, disc, stackMember, st) 
  
                # Check if the subtree rooted with v has a connection to 
                # one of the ancestors of u 
                # Case 1 (per above discussion on Disc and Low value) 
                low[u] = min(low[u], low[v]) 
                          
            elif stackMember[v] == True:  
  
                '''Update low value of 'u' only if 'v' is still in stack 
                (i.e. it's a back edge, not cross edge). 
                Case 2 (per above discussion on Disc and Low value) '''
                low[u] = min(low[u], disc[v]) 
  
        # head node found, pop the stack and print an SCC 
        w = -1 #To store stack extracted vertices 
        if low[u] == disc[u]: 
            while w != u: 
                w = st.pop() 
                print w, 
                stackMember[w] = False
                  
            print"" 
    
def main():
    ga = GraphAlgo()
    print(ga.load_from_json("./data/A1"))
    print(ga.graph)
    print(ga.save_to_json("./src/test.json"))



if  __name__ == "__main__":
    main()