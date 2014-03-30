import sys
import math
import pygame

class Plane(pygame.sprite.Sprite):
	def __init__(self, image, rect, key=None):
		'''
		Set up Plane image, rect, position, etc.

		@param image, filename of image to use
		@param rect, pygame.Rect(x, y, width, height)
		@param key, pygame.key.K_KEYNAME #chooses control key for plane, otherwise is AI
		'''
		super(Plane, self).__init__()
		# load image
		self.image = pygame.image.load(image).convert_alpha()
		self.image_def = self.image # default, unrotated image
		#! set initial stuff
		self.rect = rect
		self.width = rect[2]
		self.height = rect[3]
		self.direc = 1
		self.mspeed = 10.0
		self.rspeed = 10.0
		self.angle = 180.0
		self.moving = False
		if key:
			self.key = key
		else:
			self.key = None
	def move(self):
		'''
		Moves the plane forward until plane.moving == False
		'''
		pass
	def rotate(self, dt):
		'''
		Constantly rotates the plane in the plane.direc direction
		'''
		if not self.moving:
			ex = self.rect.x
			dy = self.rect.y
			self.angle += dt * self.direc * self.rspeed
			self.angle = self.angle % 360
			self.image = pygame.transform.rotate(self.image_def, self.angle)
	def draw(self, display):
		'''
		Draws/animates the Plane
		'''
		dx = self.image.get_rect().width - self.width
		dy = self.image.get_rect().height - self.height
		#print("angle: {}, dx: {}, dy: {}".format(self.angle, dx, dy))
		fixed_rect = pygame.Rect(self.rect)
		fixed_rect.x -= dx/2
		fixed_rect.y -= dy/2
		#pygame.draw.rect(display, (231, 51, 62), fixed_rect)
		display.blit(self.image, fixed_rect)
	def update(self, dt, display):
		'''
		Update the Plane's variables (rotation, position, etc.)
		and check keypresses
		'''
		# draw sprite
		self.draw(display)
		self.rotate(dt)
		# check keypresses
		if self.key:
			keys = pygame.key.get_pressed()
			if keys[self.key]:
				self.moving = True
				self.rect.y += dt * self.mspeed * math.sin(math.radians(270-self.angle))
				self.rect.x += dt * self.mspeed * math.cos(math.radians(270-self.angle))
			else:
				if self.moving:
					self.direc *= -1
					self.moving = False

def main():
	# set up window and bg
	display = pygame.display.set_mode((500,500))
	pygame.display.set_caption("planegame")
	colors = {'black': (0,0,0),
			'white': (255,255,255)}
	display.fill(colors['white'])
	# set up clock
	clock = pygame.time.Clock()
	fps = 30
	# create players
	p1 = Plane('plane.png', pygame.Rect(0,0,64,64), pygame.K_SPACE)
	p2 = Plane('plane2.png', pygame.Rect(100,100,64,64), pygame.K_RETURN)
	planes = pygame.sprite.Group()
	planes.add(p1, p2)
	
	# main game loop
	running = True
	while running:
		dt = clock.tick(fps) / 30.0

		display.fill(colors['white'])
		planes.update(dt, display)
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

if __name__ == '__main__':
	main()
