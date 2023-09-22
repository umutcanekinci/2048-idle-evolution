import pygame
from scripts.default.color import White
from scripts.default.object import *
from scripts.default.color import *

class Text(Object):

    def __init__(self, position, text, textSize, antialias=True, color=White, backgorundColor=None, fontPath = None, isCentered=True) -> None:
        
        
        self.position, self.text, self.textSize, self.antialias, self.color, self.backgroundColor, self.fontPath = position, text, textSize, antialias, color, backgorundColor, fontPath
        self.isCentered = isCentered

        super().__init__(position)

        self.Update("Normal", self.text)

    def Update(self, status, text) -> None:

        self.AddText(status, text, self.textSize, self.antialias, self.color, self.backgroundColor, self.fontPath)

    def SetStatus(self, status: str, surfacePosition = (0, 0), surfaceSize = (0, 0)):
        
        super().SetStatus(status)

        if self.isCentered and status in self.surfaces:
            
            rect = self.surfaces[status].get_rect(center=(surfacePosition[0] + surfaceSize[0]/2, surfacePosition[1] + surfaceSize[1]/2))

            self.SetPosition(rect.topleft)

    def HandleEvents(self, event: pygame.event.Event, surface: pygame.Surface) -> None:

        pass