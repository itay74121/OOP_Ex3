

class Position:
    def __init__(self,x=None,y=None,z=None) -> None:
        self.x = x if x else 0
        self.y = y if y else 0
        self.z = z if z else 0
    def __str__(self) -> str:
        return f"{self.x},{self.y},{self.z}"
    def __repr__(self) -> str:
        return self.__str__()
def main():
    pass
if __name__ == "__main__":
    main()