class Vertix:
    """This class demonstrates the vertices (nodes) in the graph we are working on.

    Attributes:
        x: latitude
        y: longitude   
        id: vertix's id (number)
        sectorId: sectorId
    """

    def getsectorId(self):
        return self.sectorId

    def __init__(self, sectorId, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.sectorId = sectorId

    def setsectorId(self, value = int):
        self.sectorId = value
        return 0

    def setx(self, value):
        self.x = value
        return 0

    def getx(self):
        return self.x

    def sety(self, value):
        self.y = value

    def gety(self):
        return self.y

    def setid(self, value):
        self.id = value
        return 0

    def getid(self):
        return self.id