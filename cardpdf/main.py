from mosaic import Mosaic
from resourcemanager import ResourceManager
import config as conf
import os

if __name__ == "__main__":
    rootDir = os.path.dirname(os.path.realpath(__file__))
    print(rootDir)
    resources = ResourceManager(rootDir, conf.IMG_DIR)
    mosaic = Mosaic(conf.OUTPUT_FILE,
                    (conf.PAGE_WIDTH, conf.PAGE_HEIGHT),
                    (conf.CARD_WIDTH, conf.CARD_HEIGHT),
                    (conf.PAD_WIDTH, conf.PAD_HEIGHT),
                    (conf.EXCESS_WIDTH, conf.EXCESS_HEIGHT)
                )

    for img in resources.getImages():
        mosaic.addCard(img)

    mosaic.showPage()
    print("Placed all cards")
    print("Saving, please do not close")
    mosaic.save()
