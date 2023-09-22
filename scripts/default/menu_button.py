#-# Importing Packages #-#
import pygame
from scripts.default.object import *
from scripts.default.text import *

#-# Menu Button Class #-#
class MenuButton(Object):

    def __init__(
            self,     
            color: str,
            position: tuple,
            screenPosition: tuple = None,
            selectedColor: str = None,
            text: str = None,
            selectedText: str = None,
            textColor: tuple = None,
            selectedTextColor: tuple = None,
            textBackgroundColor: tuple = None,
            selectedTextBackgroundColor: tuple = None,
            textPosition: tuple = None,
            selectedTextPosition: tuple = None,
            textSize: int = 10,
            fontPath: str = None,
            size: tuple = None,
            selectedSize: tuple = [0, 0]
        ) -> None:
        

        imagePath = ImagePath(color, "gui")
        if not selectedColor: selectedColor = color
        selectedImagePath = ImagePath(selectedColor, "gui")

        super().__init__(position, size, {"Unselected" : imagePath}, screenPosition=screenPosition)
        self.AddSurface("Selected", Images(selectedImagePath, selectedSize))
        self.status = "Unselected"
        # self.position - pygame.math.Vector2(0, (selectedSize[1] - self.height)/2), self.screenPosition - pygame.math.Vector2(0, (selectedSize[1] - self.height)/2)
        
        if text:

            self.DrawText(self.surfaces["Unselected"], text, textPosition, textSize, textColor, textBackgroundColor, fontPath)
            self.DrawText(self.surfaces["Selected"], selectedText, selectedTextPosition, textSize, selectedTextColor, selectedTextBackgroundColor, fontPath)

    def DrawText(self, surface: pygame.Surface, text: str, textPosition: tuple, textSize: int, color: tuple, backgroundColor, fontPath: pygame.font.Font = None) -> None:

        text = Text(textPosition, text, textSize, True, color, backgroundColor, fontPath, False)
        text.Draw(surface)

class Button(Object):

    def __init__(self, position: tuple = ..., size: tuple = ..., imagePaths=..., text: str = "", selectedText: str = "", textSize: int = 10, textColor: tuple = White, selectedTextColor: tuple = White, textFontPath: pygame.font.Font = None, surfaceSize: tuple = None, screenPosition: tuple = None, show=True):

        super().__init__(position, size, imagePaths, surfaceSize, screenPosition, show)

        if text:

            self.AddText("Normal", text, textSize, True, textColor, None, textFontPath)
            self.AddText("Mouse Over", selectedText, textSize, True, selectedTextColor, None, textFontPath)

    def AddText(self, status, text: str, textSize: int, antialias: bool, color: tuple, backgroundColor, fontPath: pygame.font.Font = None) -> None:

        if not hasattr(self, "text"):

            self.text = Text((0, 0), text, textSize, True, color, backgroundColor, fontPath)

        else:
            
            self.text.AddText(status, text, textSize, antialias, color, backgroundColor, fontPath)
         
    def Draw(self, surface):

        super().Draw(surface)

        if hasattr(self, "text"):

            self.text.SetStatus(self.status, self.position, self.size)
            
            self.text.Draw(surface)


