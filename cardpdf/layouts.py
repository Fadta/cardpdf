from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Slot:
    # (x,y) is the bottom left corner of the rectangle
    x: float
    y: float 
    width: float
    length: float

    def printData(self):
        print(f"Slot @({self.x:2f}, {self.y:2f}): {self.width:2f}x{self.length:2f}")


class Layout:
    def __init__(self, pageSize: Tuple[float, float], cardSize: Tuple[float, float], padding: Tuple[float, float], excess: Tuple[float, float]):
        # in the tuples (T): T[0] -> TLength / T[1] -> TWidth
        self.layout = []
        self.pageSize = pageSize
        self.cardSize = cardSize
        self.padBox = padding
        self.excessBox = excess


    def getSlot(self, i: int) -> Slot:
        if i >= len(self.layout):
            raise Exception(f"LAYOUT access OUT OF BOUNDS: Tried to access slot {i} in a layout of {len(self.layout)} slots")
        return self.layout[i]


    def length(self) -> int:
        return len(self.layout)



class GridLayout(Layout):
    def __init__(self, pageSize: Tuple[float, float], cardSize: Tuple[float, float], padding: Tuple[float, float], excess: Tuple[float, float], rows: int=0, columns: int=0):
        super().__init__(pageSize, cardSize, padding, excess)
        self.rows = rows
        self.columns = columns
        self.layout = self._buildLayout()


    def _buildLayout(self) -> List[Slot]:
        layout = []
        for r in range(self.rows):
            for c in range(self.columns):
                layout.append(self._calculateSlot(r, c))

        return layout


    def _calculateSlot(self, row: int, column: int) -> Slot:
        if(not (0 < row <= self.rows)):
            raise Exception(f"GridLayout tried to CALCULATE OUT OF BOUNDS: {self.rows} rows available, but tried to get {row}")
        if(not (0 < column <= self.columns)):
            raise Exception(f"GridLayout tried to CALCULATE OUT OF BOUNDS: {self.columns} columns available, but tried to get {column}")

        # Calculate
        posX = self.excessBox[0] + row * (self.padBox[0] + self.cardSize[0])
        posY = self.excessBox[1] + column * (self.padBox[1] + self.cardSize[1])+ self.cardSize[1]

        # Validate
        if posY > (self.pageSize[1] - self.excessBox[1]):
            raise Exception(f"GridLayout tried to place Slot Y={posY:2f}, which is out of the border >@{(self.pageSize[1] - self.excessBox[1]):2f}")
        if (posX + self.cardSize[0]) > (self.pageSize[0] - self.excessBox[0]):
            raise Exception(f"GridLayout tried to place Slot X={(posX + self.cardSize[0]):2f}, which is out of the border >@{(self.pageSize[0] - self.excessBox[0]):2f}")
        
        # Build
        slot = Slot(x=posX, y=posY, length=self.cardSize[0], width=self.cardSize[1])

        return slot



class DirectionalLayout(GridLayout):
    def __init__(self, pageSize: Tuple[float, float], cardSize: Tuple[float, float], padding: Tuple[float, float], excess: Tuple[float, float]):
        super().__init__(pageSize, cardSize, padding, excess)

        self.isRotated = self._getOrientation()

        self.layout = self._buildLayout()


    def _getOrientation(self) -> bool:
        isRotated = False
        usablePageLength = self.pageSize[0] - 2 * self.excessBox[0]
        usablePageWidth = self.pageSize[1] - 2 * self.excessBox[1]
        paddedCardLength = self.cardSize[0] + 2 * self.padBox[0]
        paddedCardWidth = self.cardSize[1] + 2 * self.padBox[1]


        fixedCardRows = int(usablePageLength / paddedCardLength) 
        fixedCardColumns = int(usablePageWidth / paddedCardWidth) 

        paddedCardWidth, paddedCardLength = paddedCardLength, paddedCardWidth

        rotatedCardRows = int(usablePageLength / paddedCardLength) 
        rotatedCardColumns = int(usablePageWidth / paddedCardWidth) 

        fixedYield = fixedCardRows * fixedCardColumns
        rotatedYield = rotatedCardRows * rotatedCardColumns

        if((fixedYield) > (rotatedYield)):
            isRotated = False
            self.rows = fixedCardRows
            self.columns = fixedCardColumns
        else:
            isRotated = True
            self.cardSize = (self.cardSize[1], self.cardSize[0])
            self.rows = rotatedCardRows
            self.columns = rotatedCardColumns

        return isRotated
