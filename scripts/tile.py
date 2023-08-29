#-# Import Packages #-#
import pygame
from pygame.math import Vector2
from scripts.color import *
from scripts.image import *

class Tile(object):
	
	def __init__(self, width, height, rowNumber, columnNumber):

		self.rowNumber, self.columnNumber = rowNumber, columnNumber
		
		self.position = self.x, self.y = self.RowNumberAndColumnNumberToPosition(self.rowNumber, self.columnNumber)
		self.image = Image(ImagePath("tile"), self.position)
		
		self.selected = False
		self.rect = self.image.GetRect()
		self.selectedRect = self.rect.copy()
		self.unselectedRect = self.rect.copy()
		self.selectedRect.y -= 10

		self.position = Vector2(self.x, self.y)


		self.size = self.width, self.height = width, height
		
		
		self.surface = self.unselectedSurface = self.image
		self.selectedSurface = self.unselectedSurface.__copy__()
		self.isEmpty = True

		self.cornersOfUnselectedPolygon =  [(0, (self.rect.height/2) - 16),
		    (self.rect.width/2, 0),
			(self.rect.width, (self.rect.height/2) - 16),
			(self.rect.width/2, self.rect.height - 34)]
		
		pygame.draw.polygon(self.selectedSurface, White, self.cornersOfUnselectedPolygon, 1)
		pygame.draw.polygon(self.unselectedSurface, Gray, self.cornersOfUnselectedPolygon, 1)

		#-# real coordinates of polyon #-#
		self.cornersOfUnselectedPolygon[0] = self.cornersOfUnselectedPolygon[0][0] + self.rect.x, self.cornersOfUnselectedPolygon[0][1] + self.rect.y
		self.cornersOfUnselectedPolygon[1] = self.cornersOfUnselectedPolygon[1][0] + self.rect.x, self.cornersOfUnselectedPolygon[1][1] + self.rect.y
		self.cornersOfUnselectedPolygon[2] = self.cornersOfUnselectedPolygon[2][0] + self.rect.x, self.cornersOfUnselectedPolygon[2][1] + self.rect.y
		self.cornersOfUnselectedPolygon[3] = self.cornersOfUnselectedPolygon[3][0] + self.rect.x, self.cornersOfUnselectedPolygon[3][1] + self.rect.y

		#-# real coordinates of polygon of selected tile #-#
		self.cornersOfSelectedPolygon = self.cornersOfUnselectedPolygon
		self.cornersOfSelectedPolygon[0] = self.cornersOfSelectedPolygon[0][0], self.cornersOfSelectedPolygon[0][1] - self.y + self.selectedRect.y
		self.cornersOfSelectedPolygon[1] = self.cornersOfSelectedPolygon[1][0], self.cornersOfSelectedPolygon[1][1] - self.y + self.selectedRect.y
		self.cornersOfSelectedPolygon[2] = self.cornersOfSelectedPolygon[2][0], self.cornersOfSelectedPolygon[2][1] - self.y + self.selectedRect.y
		self.cornersOfSelectedPolygon[3] = self.cornersOfSelectedPolygon[3][0], self.cornersOfSelectedPolygon[3][1] - self.y + self.selectedRect.y

	def RowNumberAndColumnNumberToPosition(self, row, column) -> tuple:
		
		x = (column-row)*65 + 655
		y = (column+row)*32 + 258

		return x, y

	def getAreaOfTriangle(self, pointsOfTriangle) -> float:
		x1, y1 = pointsOfTriangle[0]
		x2, y2 = pointsOfTriangle[1]
		x3, y3 = pointsOfTriangle[2]
		return abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1-y2))/2

	def isPointInTriangle(self, pointsOfTriangle, point) -> bool:
		areaOfABC = self.getAreaOfTriangle(pointsOfTriangle)
		areaOfAPB = self.getAreaOfTriangle([pointsOfTriangle[0], point, pointsOfTriangle[1]])
		areaOfAPC = self.getAreaOfTriangle([pointsOfTriangle[0], point, pointsOfTriangle[2]])
		areaOfBPC = self.getAreaOfTriangle([pointsOfTriangle[1], point, pointsOfTriangle[2]])
		return (areaOfABC == areaOfAPB + areaOfAPC + areaOfBPC)

	def isPointInQuadrangle(self, pointsOfQuadrangle, point) -> bool:
		isMouseOverTopTriangle = self.isPointInTriangle([pointsOfQuadrangle[0], pointsOfQuadrangle[1], pointsOfQuadrangle[2]], point)
		isMouseOverBotTriangle = self.isPointInTriangle([pointsOfQuadrangle[2], pointsOfQuadrangle[3], pointsOfQuadrangle[0]], point)

		return isMouseOverTopTriangle or isMouseOverBotTriangle

	def isMouseOverSelected(self, mousePosition) -> bool:
		return self.isPointInQuadrangle(self.cornersOfSelectedPolygon, mousePosition)

	def isMouseOverUnselected(self, mousePosition) -> bool:
		return self.isPointInQuadrangle(self.cornersOfUnselectedPolygon, mousePosition)

	def isMouseOver(self, mousePosition) -> bool:
		return self.isMouseOverSelected(mousePosition) or self.isMouseOverUnselected(mousePosition)

	def Draw(self, Window: pygame.Surface) -> None:

		if self.selected:
			Window.blit(self.selectedSurface, self.rect)
		else:
			Window.blit(self.unselectedSurface, self.rect)
		