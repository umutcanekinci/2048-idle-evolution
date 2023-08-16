import pygame
from images import *

class Button(Image):

    def __init__(
            self,     
            color: str,
            selectedColor: str,
            text: str,
            selectedText: str,
            textColor: tuple,
            selectedTextColor: tuple,
            textPosition: tuple,
            selectedTextPosition: tuple,
            font: pygame.font.Font,
            position: tuple,
            screenPosition: tuple = None,
            size: tuple = None,
            selectedSize: tuple = None
        ) -> None:
        
        imagePath = ImagePath(color+"_button00", "gui")
        selectedImagePath = ImagePath(selectedColor+"_button00", "gui")
        
        super().__init__(imagePath, position, screenPosition, size)

        self.selectedImage = Image(selectedImagePath, self.position - Vector2(0, (selectedSize[1] - size[1])/2), self.screenPosition - Vector2(0, (selectedSize[1] - size[1])/2), selectedSize)
        
        if text:
            self.DrawText(self, text, textColor, textPosition, font)
            self.DrawText(self.selectedImage, selectedText, selectedTextColor, selectedTextPosition, font)

        self.selected = False

    def DrawText(self, surface, text, textColor, textPosition, font) -> None:

        text = font.render(text, False, textColor)
        surface.blit(text, textPosition)
    
    def Draw(self, surface: pygame.Surface) -> None:

        if self.selected:

            self.selectedImage.Draw(surface)

        else:

            super().Draw(surface)

        