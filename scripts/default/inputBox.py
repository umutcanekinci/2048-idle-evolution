#-# Import Packages #-#
import pygame

#-# Input Box Class #-#
class InputBox:

	def __init__(self, x, y, w, h, text=''):

		self.rect = pygame.Rect(x, y, w, h)
		self.color = pygame.Color('dodgerblue2') # ('lightskyblue3')
		self.text = text
		self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)
		self.active = True # False

	def HandleEvents(self, event, mousePosition):

		if event.type == pygame.MOUSEBUTTONDOWN:

			# If the user clicked on the input_box rect.
			if self.rect.collidepoint(mousePosition):

				# Toggle the active variable.
				self.active = True #not self.active

			else:

				self.active = False

			# Change the current color of the input box.
			self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')

		if event.type == pygame.KEYDOWN:

			if self.active:

				if event.key == pygame.K_BACKSPACE:

					self.text = self.text[:-1]

				else:

					self.text += event.unicode

				# Re-render the text.
				self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)

	def update(self):
		# Resize the box if the text is too long.
		width = max(200, self.txt_surface.get_width()+10)
		if self.rect.w < width:        
			self.rect.w = width

	def Draw(self, screen):
		# Blit the text.
		screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
		# Blit the rect.
		pygame.draw.rect(screen, self.color, self.rect, 2)