import pygame
import os

def draw_background(screen):
    # السماء
    screen.fill((135, 206, 235))

    # الأرض
    pygame.draw.rect(screen, (139, 69, 19), (0, 350, 250, 200))
    pygame.draw.rect(screen, (139, 69, 19), (550, 350, 250, 200))

    # النهر
    pygame.draw.rect(screen, (0, 105, 148), (250, 380, 300, 170))


def load_images():
    # ✅ ضفنا man2 هنا
    names = ['farmer', 'wolf', 'sheep', 'cabbage', 'boat']
    images = {}

    base_path = os.path.dirname(__file__)  # مكان الملف

    for name in names:
        try:
            path = os.path.join(base_path, f"{name}.png")
            img = pygame.image.load(path).convert_alpha()

            # حجم الصور
            if name == 'boat':
                img = pygame.transform.scale(img, (200, 100))
            else:
                img = pygame.transform.scale(img, (70, 70))

            images[name] = img

        except Exception as e:
            print(f"[WARNING] Failed to load {name}.png → {e}")

            # fallback شكل بديل
            surf = pygame.Surface((70, 70), pygame.SRCALPHA)

            # ألوان مختلفة لكل عنصر عشان تميّزهم
            colors = {
                'farmer': (255, 255, 0),
                'wolf': (200, 0, 0),
                'sheep': (255, 255, 255),
                'cabbage': (0, 200, 0),
                'boat': (150, 75, 0),
                'man2': (0, 0, 255),
            }

            pygame.draw.circle(surf, colors.get(name, (200, 200, 200)), (35, 35), 30)

            images[name] = surf

    return images