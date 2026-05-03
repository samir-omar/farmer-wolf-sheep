import pygame

def draw_background(screen):
    # رسم السماء
    screen.fill((135, 206, 235)) 
    # رسم اليابسة (بني) - كبرنا الارتفاع شوية عشان الصور تاخد راحتها
    pygame.draw.rect(screen, (139, 69, 19), (0, 350, 250, 200))   # يسار
    pygame.draw.rect(screen, (139, 69, 19), (550, 350, 250, 200)) # يمين
    # رسم النهر
    pygame.draw.rect(screen, (0, 105, 148), (250, 380, 300, 170))

def load_images():
    names = ['farmer', 'man2', 'wolf', 'sheep', 'cabbage', 'boat']
    images = {}
    for name in names:
        try:
            img = pygame.image.load(f'{name}.png').convert_alpha()
            if name == 'boat':
                images[name] = pygame.transform.scale(img, (200, 100)) # قارب أكبر
            else:
                images[name] = pygame.transform.scale(img, (70, 70)) # صور أوضح
        except:
            surf = pygame.Surface((70, 70))
            surf.fill((200, 0, 0))
            images[name] = surf
    return images