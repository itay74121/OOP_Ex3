

class Edge:
    def __init__(self,src,dest,weight) -> None:
        super().__init__()
        self.src = src
        self.dest = dest
        self.setweight(weight)

    def setweight(self,weight) -> None:
        if weight>0:
            self.__weight = weight
        else:
            self.__weight = 0
    def getweight(self) -> int:
        return self.__weight

    def __str__(self) -> str:
        return f"({self.src} {self.dest} {self.__weight})"
    def __repr__(self) -> str:
        return self.__str__()
    def __eq__(self, o: object) -> bool:
        return o.src == self.src and o.dest == self.dest and o.getweight()==self.__weight
    
      