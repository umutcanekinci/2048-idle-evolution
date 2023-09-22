#-# Import Packages #-#
import pygame
from images import *
from scripts.tile import *

ages = ["wood", "rock", "sand", "stone"]

#-# Building Class #-#
class Building(Object):

    def __init__(self, level, ageNumber, tile: Tile) -> None:
        
        self.tile = tile
        self.ageNumber = ageNumber
        self.age = ages[ageNumber]
        self.selected = False
        self.destroy = False
        self.cooldown = 2
        self.lastTime = None
        self.level = level
        self.speed = (self.level * 2 * (ageNumber + 1)) - 1 # cash per second
        self.sellPrice = self.level*(self.ageNumber+1)*70
        self.__SetSize()
        self.SetPositionFromTile(self.tile)
        super().__init__(self.unselectedPosition, self.size, {"Normal" : self.GetImagePath()})
        #self.rect = self.GetRect()
        self.SetVelocity((0, 0))

    def GetImagePath(self) -> str:
        
        return ImagePath("level" + str(self.level), "buildings/" + self.age)

    def __SetSize(self) -> None:

        if self.level == 1 or self.level == 2:
            self.floorCount = 1
        elif self.level == 3 or self.level == 4:
            self.floorCount = 2
        elif self.level == 5 or self.level == 6:
            self.floorCount = 3
        
        self.size = self.width, self.height = (50, 75 + (self.floorCount - 1) * 23)        

    def SetPositionFromTile(self, tile: Tile) -> None:

        x, y = tile.x + 43, tile.y - 23 - (self.floorCount - 1) * 23
        
        self.unselectedPosition = Vector2(x, y)
        self.selectedPosition = Vector2(x, y - 10)

    def __Move(self) -> None:

        if (self.targetPosition.x < self.position.x < self.targetPosition.x + self.velocity.x or self.targetPosition.x > self.position.x > self.targetPosition.x + self.velocity.x) and (self.targetPosition.y < self.position.y < self.targetPosition.y + self.velocity.y or self.targetPosition.y > self.position.y > self.targetPosition.y + self.velocity.y):
            
            self.velocity = Vector2(0, 0)

        self.position += self.velocity

    def SetTargetTile(self, targetTile: Tile) -> None:

        self.tile = targetTile
        self.SetPositionFromTile(targetTile)
        self.targetPosition = self.selectedPosition
        direction = self.targetPosition - self.position # This vector points from the mouse pos to the target.
        self.velocity = direction.normalize() * 8 # The velocity is the normalized direction vector scaled to the desired length.

    def LevelUp(self, sacrificialBuilding) -> None:
        sacrificialBuilding.SetTargetTile(self.tile)
        sacrificialBuilding.Destroy(self)

    def Destroy(self, newBuilding) -> None:
        self.newBuilding = newBuilding
        self.destroy = True

    def Draw(self, surface: pygame.Surface, buildings: list ={}) -> None:
        
        if self.velocity == Vector2(0, 0):

            if self.destroy:

                buildings.remove(self)
                buildings.remove(self.newBuilding)
                buildings.append(Building(self.level + 1, self.ageNumber, self.tile))
                buildings.sort(key=lambda building: building.tile.columnNumber)

            else:

                if self.tile.selected and self.tile.rect == self.tile.selectedRect:

                    self.position = self.selectedPosition

                else:

                    self.position = self.unselectedPosition
        else:

            self.__Move()
        
        super().Draw(surface)

class Buildings(list[Building]):

    def __init__(self) -> None:

        super().__init__()

    def SetAge(self, ageNumber):

        self.ageNumber = ageNumber

        for i, building in enumerate(self):

            self[i] = Building(building.level, self.ageNumber, building.tile)

    def HandleEvents(self, event, mousePosition) -> None:

        pass

    def Draw(self, surface):

        for building in self:

            building.Draw(surface)