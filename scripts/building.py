#-# Import Packages #-#
import pygame
from images import *
from scripts.tile import *

#-# Building Class #-#
class Building(Image):

    def __init__(self, level, tile: Tile) -> None:
        
        self.tile = tile
        self.selected = False
        self.destroy = False
        self.cooldown = 2
        self.lastTime = None
        self.level = level
        self.speed = (self.level * 2) - 1 # cash per second
        self.sellPrice = self.level*80
        self.SetSize()
        self.SetPositionFromTile(self.tile)
        super().__init__(self.GetImagePath(), self.unselectedPosition, size=self.size)
        self.rect = self.GetRect()
        self.SetVelocity((0, 0))

    def GetImagePath(self) -> str:
        return ImagePath("level" + str(self.level), "buildings")

    def SetSize(self):

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

    def Move(self) -> None:

        if (self.targetPosition.x < self.position.x < self.targetPosition.x + self.velocity.x or self.targetPosition.x > self.position.x > self.targetPosition.x + self.velocity.x) and (self.targetPosition.y < self.position.y < self.targetPosition.y + self.velocity.y or self.targetPosition.y > self.position.y > self.targetPosition.y + self.velocity.y):
            self.velocity = Vector2(0, 0)

        self.position += self.velocity

    def SetTargetTile(self, targetTile: Tile) -> None:

        self.tile = targetTile
        self.SetPositionFromTile(targetTile)
        self.targetPosition = self.selectedPosition
        direction = self.targetPosition - self.position # This vector points from the mouse pos to the target.
        self.velocity = direction.normalize() * 8 # The velocity is the normalized direction vector scaled to the desired length.

    def LevelUp(self, sacrificialBuilding):
        sacrificialBuilding.SetTargetTile(self.tile)
        sacrificialBuilding.Destroy(self)

    def Destroy(self, newBuilding):
        self.newBuilding = newBuilding
        self.destroy = True

    def Draw(self, surface: pygame.Surface, buildings: list) -> None:
        
        if self.velocity == Vector2(0, 0):
            if self.destroy:
                buildings.remove(self)
                buildings.remove(self.newBuilding)
                buildings.append(Building(self.level + 1, self.tile))
                buildings.sort(key=lambda building: building.tile.columnNumber)

            else:
                if self.tile.selected:
                    self.position = self.selectedPosition
                else:
                    self.position = self.unselectedPosition
        else:

            self.Move()
        
        super().Draw(surface)
