import pygame,sys
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups,collision_sprites):
        super().__init__(groups)

        # Image
        self.import_asset()
        self.frame_index = 0
        self.status = 'up'
        # self.image = self.animation[self.frame_index]
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        # Float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 200

        # Collisions
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(0,-self.rect.height // 2)

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite,'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()

                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        self.pos.x = self.hitbox.centerx
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.pos.x = self.hitbox.centerx

        else:
            # Vertical collision
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite,'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.pos.y = self.hitbox.centery
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.pos.y = self.hitbox.centery

    def import_asset(self):
        self.animations = {}
        for index, folder in enumerate(walk('./graphics/player')):
            # print(f"Folder: {folder}")
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in folder[2]:
                    # print(file_name, folder[2])
                    path = folder[0].replace('\\','/') + '/' + file_name 
                    # print(f"Path: {path}")
                    surf = pygame.image.load(path).convert_alpha()
                    # print(f"Folder[0]: {folder[0]}")
                    # key = folder[0].split('\\')[1]
                    key = folder[0].split('/')[3]
                    # print(f"Key: {key}")
                    self.animations[key].append(surf)

    def move(self,dt):

        # normalize a vector -> the length of a vector is going to be 1
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Horizontal movement + collision
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        # Horizontal Collision
        self.collision('horizontal')

        # Vertical movement + collision
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        # Vertical Collision
        self.collision('Vertical')

    def input(self):
        keys = pygame.key.get_pressed()

        # Horizontal input
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        # Vertical Input
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

    def animate(self,dt):
        current_animation = self.animations[self.status]

        if self.direction.magnitude() != 0:
            self.frame_index += 10 * dt
            if self.frame_index >= len(current_animation):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]

    def restrict(self):
        if self.rect.left < 649:
            self.pos.x = 640 + self.rect.width / 2
            self.hitbox.left = 640
            self.rect.left = 640
        if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.right = 2560
        if self.rect.bottom > 3500:
            self.pos.y = 3500 - self.rect.height / 2
            self.hitbox.bottom = 3500
            self.rect.bottom = self.rect.centery
        

    def update(self,dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.restrict()