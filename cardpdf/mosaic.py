from typing import  Tuple
from reportlab.pdfgen.canvas import Canvas
from PIL import Image
from layouts import DirectionalLayout


class Mosaic(Canvas):
    def __init__(self, filename, pagesize:Tuple[float, float], cardSize:Tuple[float, float], padBox: Tuple[float, float], excessBox: Tuple[float, float], **kwargs):
        super().__init__(filename, pagesize, **kwargs)
        self._cardSize = cardSize
        self._pageSize = pagesize
        self._padBox = padBox
        self._excessBox = excessBox

        self._layout = DirectionalLayout(self._pageSize, self._cardSize, self._padBox, self._excessBox)
        self._iter_index = 0
        self._page_count = 0

        # self._layout.printLayoutInfo()


    def showPage(self) -> None:
        self._page_count += 1
        print(f"Page {self._page_count} Finished")
        self._iter_index = 0
        super().showPage()

    
    def addCard(self, imgPath: str) -> None:
        if(self._iter_index >= self._layout.length()):
            self.showPage()

        print(f"Adding card {self._iter_index+1}", end="\r")
        img = Image.open(imgPath)
        if(self._layout.isRotated):
            img = img.rotate(90, expand=True)

        slot = self._layout.getSlot(self._iter_index)
        self._iter_index += 1
        self.drawInlineImage(img, slot.x, slot.y, slot.width, slot.height)  # Using drawInlineImage instead of drawImage, because of an exception I can't comprehend and couldn't find googling
