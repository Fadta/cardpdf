from typing import List
import os.path as osp
import os

class ResourceManager:
    def __init__(self, baseDir: str, imgDirectory: str):
        self.baseDir = baseDir
        self.imgDir = osp.join(self.baseDir, imgDirectory)


    def getImages(self) -> List[str]:
        images = []
        for dirpath, _, filenames in os.walk(self.imgDir):
            images = [osp.join(dirpath, file) for file in filenames if file != '.gitkeep']
            break

        return images
