#-# Import Packages #-#
from scripts.image import *
import random

class Cloud(Image):
    
    def __init__(self, imagePath: FilePath, windowWidth, windowHeight, size=(100, 100)):
        
        x = random.randint(0, windowWidth - 101)
        y = random.randint(0, windowHeight - 101)
        
        self.SetVelocity((random.choice([1/2, 1/3, 1/4, 1/5,-1/2, -1/3, -1/4, -1/5]), 0))

        super().__init__(imagePath, (x, y), None, size)
