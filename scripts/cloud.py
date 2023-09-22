#-# Import Packages #-#
from scripts.default.object import *
import random

class Cloud(Object):
    
    def __init__(self, imagePath: FilePath, surfaceSize: tuple, size=(100, 100)):
        
        x = random.randint(0, surfaceSize[0] - 101)
        y = random.randint(0, surfaceSize[1] - 101)
        
        self.SetVelocity((random.choice([1/2, 1/3, 1/4, 1/5,-1/2, -1/3, -1/4, -1/5]), 0))

        super().__init__((x, y), size, {"Normal" : imagePath})

class GameClouds(list[Cloud]):

    def __init__(self, count, surfaceSize) -> None:
        
        super().__init__()

        self.surfaceSize = surfaceSize
        self.count = count

        self.CreateClouds()

    def CreateClouds(self):
        
        for i in range(self.count):

            cloud = Cloud(ImagePath("cloud"), self.surfaceSize)
            self.append(cloud)

    def HandleEvents(self, event, mousePosition):

        pass

    def Draw(self, surface) -> None:

        for cloud in self:

            if self.surfaceSize[0] - cloud.width + cloud.velocity[0] >= cloud.position.x > self.surfaceSize[0] - cloud.width and cloud.velocity[0] > 0:

                newCloud = Cloud(ImagePath("cloud"), self.surfaceSize)
                newCloud.SetPosition((cloud.position.x - self.surfaceSize[0], cloud.position.y))
                newCloud.velocity = cloud.velocity
                self.append(newCloud)

            elif cloud.velocity[0] <= cloud.position.x < 0 and cloud.velocity[0] < 0:

                newCloud = Cloud(ImagePath("cloud"), self.surfaceSize)
                newCloud.SetPosition((cloud.position.x + self.surfaceSize[0], cloud.position.y))
                newCloud.velocity = cloud.velocity
                self.append(newCloud)

            if cloud.position.x >= self.surfaceSize[0] or cloud.position.x < -cloud.width:

                self.remove(cloud)

            cloud.Draw(surface)

class CloudAnimation(list[Cloud]):

    def __init__(self, surfaceSize):

        super().__init__()
        
        self.surfaceSize = surfaceSize

    def CreateClouds(self):

        for i in range(100):

            cloud = Cloud(ImagePath("cloud"), self.surfaceSize, (200, 200))
            
            #cloud.SetVelocity((random.choice((-4, 4)), 0))
            
            if cloud.position.x <= self.surfaceSize[0]/2:

                cloud.SetVelocity((-10, 0))

            else:

                cloud.SetVelocity((10, 0))
            
            self.append(cloud)

    def HandleEvents(self, event, mousePosition):
        
        pass

    def Draw(self, surface):
            
        for cloud in self:

            cloud.Draw(surface)

            if cloud.position.x >= self.surfaceSize[0] or cloud.position.x <= -cloud.width:

                self.remove(cloud)
