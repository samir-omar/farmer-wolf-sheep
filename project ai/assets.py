import pygame
import os

def draw_background(screen):
    screen.fill((135, 206, 235))

    pygame.draw.rect(screen, (139, 69, 19), (0, 350, 250, 200))
    pygame.draw.rect(screen, (139, 69, 19), (550, 350, 250, 200))

    pygame.draw.rect(screen, (0, 105, 148), (250, 380, 300, 170))


def load_images():
    names = ['farmer', 'wolf', 'sheep', 'cabbage', 'boat']
    images = {}

    base_path = os.path.dirname(__file__)

    for name in names:
        try:
            path = os.path.join(base_path, f"{name}.png")
            img = pygame.image.load(path).convert_alpha()

            if name == 'boat':
                images[name] = pygame.transform.scale(img, (200, 100))
            else:
                images[name] = pygame.transform.scale(img, (70, 70))

        except Exception as e:
            print(f"Error loading {name}: {e}")

            surf = pygame.Surface((70, 70))
            surf.fill((200, 0, 0))
            images[name] = surf

    return images