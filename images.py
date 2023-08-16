import os
import pygame
from pygame.math import Vector2
from path import *


class Image(pygame.Surface):
    
    def __init__(self, path: FilePath, position: tuple, screenPosition: tuple = None, size: tuple = None, ) -> None:
        
        self.path = path
        self.SetImage(self.path)
        self.position = Vector2(position)
        
        if not screenPosition:
            self.screenPosition = self.position
        else:
            self.screenPosition = screenPosition
    
        if size and size[0] and size[1]:
            self.size = self.width, self.height = size
            self.__ResizeImage(self.size)
        else:
            self.size = self.width, self.height = self.image.get_rect().size

        super().__init__(self.size, pygame.SRCALPHA)
        self.ReblitImage()

    def SetVelocity(self, velocity):
        self.velocity = Vector2(velocity[0], velocity[1])

    def Move(self):
        self.position += self.velocity

    def GetRect(self):
        return pygame.Rect(self.position.x, self.position.y, self.width, self.height)

    def ReblitImage(self):
        self.blit(self.image, (0, 0))

    def isMouseOver(self, mousePosition: tuple):
        return pygame.Rect(self.screenPosition, self.size).collidepoint(mousePosition)

    def SetImage(self, path: str):
        self.image = pygame.image.load(path)

    def __ResizeImage(self, size: tuple):
        self.image = pygame.transform.scale(self.image, size).convert_alpha()

    def Resize(self, newSize: tuple):
        self = Image(self.name, self.position, self.screenPosition, newSize, self.extension, self.folder)

    def SetPosition(self, position: tuple):
        self.position = Vector2(position)

    def Draw(self, surface: pygame.Surface):
        surface.blit(self, self.position)