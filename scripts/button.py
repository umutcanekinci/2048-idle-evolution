import pygame
from scripts.image import *

class Button(Image):

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
            textPosition: tuple = None,
            selectedTextPosition: tuple = None,
            font: pygame.font.Font = None,
            size: tuple = None,
            selectedSize: tuple = None
        ) -> None:
        

        imagePath = ImagePath(color+"_button00", "gui")
        super().__init__(imagePath, position, screenPosition, size)
        
        if not selectedSize: selectedSize = self.size
        if not selectedColor: selectedColor = color
        if not screenPosition: screenPosition = position

        selectedImagePath = ImagePath(selectedColor+"_button00", "gui")
        self.selectedImage = Image(selectedImagePath, self.position - Vector2(0, (selectedSize[1] - self.height)/2), self.screenPosition - Vector2(0, (selectedSize[1] - self.height)/2), selectedSize)
        
        if text:
            self.DrawText(self, text, textColor, textPosition, font)
            self.DrawText(self.selectedImage, selectedText, selectedTextColor, selectedTextPosition, font)

        self.selected = False

    def DrawText(self, surface: pygame.Surface, text: str, textColor: tuple, textPosition: tuple, font: pygame.font.Font) -> None:

        text = font.render(text, False, textColor)
        surface.blit(text, textPosition)
    
    def Draw(self, surface: pygame.Surface) -> None:

        if self.selected:

            self.selectedImage.Draw(surface)

        else:

            super().Draw(surface)
