import pygame
from scripts.default.image import *
from scripts.default.object import *

class Buttonxx(Object):

	def __init__(
			self,
			Text="Button",
			position: tuple = ("CENTER", "CENTER"),
			size: tuple = (None, None),
			Color="white",
			ActiveColor="white",
			CornerRadius=0,
			BorderSize=2,
			BorderColor="black",
			FontSize=23,
			FontColor="white",
			ActiveFontColor="white",
			FontSide="Center",
			FontMargin=20,
			IconPath=None,
			IconSize=[10, 10],
			IconSide="LeftCenter",
			IconMargin=20,
			surfaceSize: tuple = None,
			show = True
			):
		
		super().__init__(position, size, {}, surfaceSize, show)
		
		#-# Button Proporties #-#
		self.Rect = pygame.Rect(self.position[0] - CornerRadius, self.position[1] - CornerRadius, self.size[0] + CornerRadius*2, self.size[1] + CornerRadius*2)
		self.Color, self.ActiveColor, self.CornerRadius, self.BorderSize, self.BorderColor = pygame.Color(Color), pygame.Color(ActiveColor), CornerRadius, BorderSize, pygame.Color(BorderColor)

		#-# Text And Font Proporties #-#
		self.Text, self.Font, self.FontSize, self.FontColor, self.ActiveFontColor = Text, pygame.font.Font("fonts/comic.ttf", FontSize), FontSize, pygame.Color(FontColor), pygame.Color(ActiveFontColor)
		self.Text, self.Text2 = self.Font.render(self.Text, True, self.FontColor), self.Font.render(self.Text, True, self.ActiveFontColor)

		#-# Icon Proporties #-#
		self.IconPath, self.IconSize, self.IconMargin =  IconPath, IconSize, IconMargin

		#-# Sides #-#
		self.FontSide = self.GetSide(FontSide, self.Text.get_size(), FontMargin)
		if self.IconPath != None: self.IconSide = self.GetSide(IconSide, IconSize, IconMargin)
		#-# Creating Button #-#
		self.Surface = pygame.Surface(self.Rect.size, pygame.SRCALPHA)
		self.MouseOverSurface = self.Surface.copy()
		
		
		pygame.draw.rect(self.Surface, self.Color, ((0, 0), self.Rect.size), 0, self.CornerRadius)
		pygame.draw.rect(self.MouseOverSurface, self.ActiveColor, ((0, 0), self.Rect.size), 0, self.CornerRadius)
		
		if self.BorderSize > 0:
			pygame.draw.rect(self.Surface, self.BorderColor, ((0, 0), (self.Rect.width - self.BorderSize, self.Rect.height - self.BorderSize)), self.BorderSize, self.CornerRadius)
			pygame.draw.rect(self.MouseOverSurface, self.BorderColor, ((0, 0), (self.Rect.width - self.BorderSize, self.Rect.height - self.BorderSize)), self.BorderSize, self.CornerRadius)
			
		if self.IconPath != None:
			Images((self.IconSide, self.IconSize), self.IconPath).Draw(self.Surface)
			Images((self.IconSide, self.IconSize), self.IconPath).Draw(self.MouseOverSurface)
		
		self.Surface.blit(self.Text, self.FontSide)
		self.MouseOverSurface.blit(self.Text2, self.FontSide)
		
		self.ActiveSurface = self.Surface.copy()
		self.MouseOverActiveSurface = self.MouseOverSurface.copy()
		
		pygame.draw.rect(self.ActiveSurface, self.FontColor, ((0, 0), self.Rect.size), 1, self.CornerRadius)		
		pygame.draw.rect(self.MouseOverActiveSurface, self.FontColor, ((0, 0), self.Rect.size), 1, self.CornerRadius)
		
		self.Active, self.Style = False, "Normal"

	def GetSide(self, Side, Size, Margin):

		#-# Sides #-#
		self.Left = self.BorderSize + Margin
		self.CenterX = (self.Rect.width - Size[0])/2
		self.Right = self.Rect.width - Size[0] - self.BorderSize - Margin
		self.Top = self.BorderSize + Margin
		self.CenterY = (self.Rect.height - Size[1])/2
		self.Bottom = self.Rect.height - Size[1] - self.BorderSize - Margin

		return {"TopLeft" : (self.Left, self.Top),
		 "TopCenter" : (self.CenterX, self.Top),
		 "RightCenter" : (self.Right, self.Top),
		 "LeftCenter" : (self.Left, self.CenterY),
		 "Center" : (self.CenterX, self.CenterY),
		 "RightCenter" : (self.Right, self.CenterY),
		 "BottomLeft" : (self.Left , self.Bottom ),
		 "BottomCenter" : (self.CenterX, self.Bottom),
		 "BottomCenter" : (self.Right, self.Bottom)}.get(Side)

	def HandleEvent(self, Event, MousePosition):

		if self.isMouseOver(MousePosition):
			
			self.Style = "MouseOverActive" if self.Style == "Active" else "MouseOver"		
		else:
			
			self.Style = "Active" if self.Style == "MouseOverActive" else "Normal"		
			
		if Event.type == pygame.MOUSEBUTTONUP:
			
			self.Style = "Normal"

		if self.isMouseClick(Event, MousePosition):
			
			self.Style = "MouseOverActive" if self.Style == "MouseOver" else "MouseOver"

	def Draw(self, surface):

		if self.show:

			if self.Style == "Normal": surface.blit(self.Surface, self.Rect)
			elif self.Style == "Active": surface.blit(self.ActiveSurface, self.Rect)
			elif self.Style == "MouseOver": surface.blit(self.MouseOverSurface, [self.Rect.x, self.Rect.y - 5])		
			elif self.Style == "MouseOverActive": surface.blit(self.MouseOverActiveSurface, [self.Rect.x, self.Rect.y - 5])
