import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.spritesheet = pygame.image.load("assets/explosion_sprite_sheet_fixed.png").convert_alpha()
        self.frames = []
        frame_width, frame_height = 128, 128
        for i in range(12):  # 12 klatek
            frame = self.spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            self.frames.append(frame)

        self.current_frame = 0
        self.position = position
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=position)
        self.animation_speed = 0.1  # Czas pomiędzy klatkami
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.animation_speed:
            self.timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.kill()  # Usunięcie obiektu po zakończeniu animacji
            else:
                self.image = self.frames[self.current_frame]
