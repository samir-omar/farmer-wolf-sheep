import pygame
import sys

# محاولة تحميل الصور أو استخدام البدائل الملونة
try:
    from assets import draw_background, load_images
except ImportError:
    def draw_background(screen):
        screen.fill((135, 206, 235)) # سماء
        pygame.draw.rect(screen, (139, 69, 19), (0, 350, 250, 200))   # يابسة يسار
        pygame.draw.rect(screen, (139, 69, 19), (550, 350, 250, 200)) # يابسة يمين
        pygame.draw.rect(screen, (0, 105, 148), (250, 380, 300, 170)) # نهر

    def load_images():
        imgs = {}
        # تم حذف man2 من القائمة تماماً
        colors = {
            'boat': (100, 50, 0), 'farmer': (255, 224, 189), 
            'wolf': (128, 128, 128), 'sheep': (255, 255, 255), 
            'cabbage': (0, 255, 0)
        }
        for name, color in colors.items():
            try:
                img = pygame.image.load(f'{name}.png').convert_alpha()
                if name == 'boat': imgs[name] = pygame.transform.scale(img, (200, 100))
                else: imgs[name] = pygame.transform.scale(img, (70, 70))
            except:
                surf = pygame.Surface((70, 70), pygame.SRCALPHA)
                pygame.draw.circle(surf, color, (35, 35), 30)
                pygame.draw.circle(surf, (0, 0, 0), (35, 35), 30, 2)
                imgs[name] = surf
        return imgs

class RiverGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 550))
        pygame.display.set_caption("Farmer, Wolf & Sheep Game")
        
        self.images = load_images()
        self.font = pygame.font.SysFont('Arial', 22, bold=True)
        
        self.score = 0
        self.solving = False
        self.solution_steps = []
        self.step_index = 0
        self.step_timer = 0
        
        self.reset_game()

    def reset_game(self):
        # تم حذف man2 من الحالة
        self.side = {'wolf': 0, 'sheep': 0, 'cabbage': 0}
        self.boat_side = 0
        self.passengers = [] 
        self.game_over = False
        self.mission_complete = False
        self.message = "Goal: Move everyone safely!"

    def check_victory(self):
        if all(v == 1 for v in self.side.values()) and not self.passengers and self.boat_side == 1:
            self.mission_complete = True
            self.message = "YOU ARE WIN!"
            return True
        return False

    def check_failure(self):
        boat_zone = self.passengers + ['farmer']
        left_bank = [k for k, v in self.side.items() if v == 0 and k not in self.passengers]
        right_bank = [k for k, v in self.side.items() if v == 1 and k not in self.passengers]
        
        if self.boat_side == 0: left_bank.append('farmer')
        else: right_bank.append('farmer')

        for area in [boat_zone, left_bank, right_bank]:
            if 'farmer' not in area:
                if 'wolf' in area and 'sheep' in area:
                    return True, "Wolf ate the Sheep!"
                if 'sheep' in area and 'cabbage' in area:
                    return True, "Sheep ate the Cabbage!"
        return False, ""

    def start_solve(self):
        self.reset_game()
        self.solving = True
        # خطوات الحل الكلاسيكية (بدون الرجل الثاني)
        self.solution_steps = [
            ("sheep", "load"), ("go", ""), ("sheep", "unload"),
            ("go", ""),
            ("wolf", "load"), ("go", ""), ("wolf", "unload"),
            ("sheep", "load"), ("go", ""), ("sheep", "unload"),
            ("cabbage", "load"), ("go", ""), ("cabbage", "unload"),
            ("go", ""),
            ("sheep", "load"), ("go", ""), ("sheep", "unload")
        ]
        self.step_index = 0

    def run_step(self):
        if self.step_index >= len(self.solution_steps):
            self.solving = False
            self.check_victory()
            return
        item, action = self.solution_steps[self.step_index]
        if action == "load": self.passengers.append(item)
        elif action == "unload" and item in self.passengers:
            self.passengers.remove(item)
            self.side[item] = self.boat_side
        elif item == "go":
            self.boat_side = 1 - self.boat_side
            for p in self.passengers: self.side[p] = self.boat_side
        self.step_index += 1

    def run(self):
        clock = pygame.time.Clock()
        while True:
            draw_background(self.screen)
            boat_pos = [(180, 360), (420, 360)]
            bx, by = boat_pos[self.boat_side]
            self.screen.blit(self.images['boat'], (bx, by))
            self.screen.blit(self.images['farmer'], (bx + 10, by - 60))

            items_list = ['wolf', 'sheep', 'cabbage']
            for item in items_list:
                if item in self.passengers:
                    idx = self.passengers.index(item)
                    self.screen.blit(self.images[item], (bx + 70 + idx * 60, by - 30))
                else:
                    x_pos = 30 if self.side[item] == 0 else 650
                    y_off = {'wolf': 0, 'sheep': 75, 'cabbage': 150}
                    final_x = x_pos + y_off[item] if x_pos == 30 else x_pos - y_off[item] + 120
                    self.screen.blit(self.images[item], (final_x, 320))

            score_surf = self.font.render(f"SCORE: {self.score}", True, (0, 0, 0))
            self.screen.blit(score_surf, (20, 20))
            msg_color = (255, 0, 0) if self.game_over else (0, 150, 0) if self.mission_complete else (255, 255, 255)
            msg_surf = self.font.render(self.message, True, msg_color)
            self.screen.blit(msg_surf, (400 - msg_surf.get_width()//2, 50))

            go_rect = pygame.Rect(250, 480, 90, 45)
            down_rect = pygame.Rect(355, 480, 90, 45)
            solve_rect = pygame.Rect(460, 480, 90, 45)
            retry_rect = pygame.Rect(325, 220, 150, 50)

            if not self.solving:
                if self.game_over or self.mission_complete:
                    pygame.draw.rect(self.screen, (50, 50, 50), retry_rect, border_radius=8)
                    txt = "RETRY" if self.game_over else "ADD SCORE"
                    self.screen.blit(self.font.render(txt, True, (255,255,255)), (retry_rect.x+20, retry_rect.y+10))
                else:
                    pygame.draw.rect(self.screen, (0, 150, 0), go_rect, border_radius=8)
                    pygame.draw.rect(self.screen, (200, 0, 0), down_rect, border_radius=8)
                    pygame.draw.rect(self.screen, (0, 0, 150), solve_rect, border_radius=8)
                    self.screen.blit(self.font.render("GO", True, (255,255,255)), (280, 490))
                    self.screen.blit(self.font.render("DOWN", True, (255,255,255)), (370, 490))
                    self.screen.blit(self.font.render("SOLVE", True, (255,255,255)), (475, 490))

            if self.solving:
                self.step_timer += 1
                if self.step_timer > 40:
                    self.run_step()
                    self.step_timer = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not self.solving:
                    mx, my = event.pos
                    if (self.game_over or self.mission_complete) and retry_rect.collidepoint(mx, my):
                        if self.mission_complete: self.score += 10
                        self.reset_game()
                    elif not self.game_over and not self.mission_complete:
                        if go_rect.collidepoint(mx, my):
                            self.boat_side = 1 - self.boat_side
                            for p in self.passengers: self.side[p] = self.boat_side
                            failed, err = self.check_failure()
                            if failed: self.game_over, self.message = True, err
                            self.check_victory()
                        elif down_rect.collidepoint(mx, my):
                            self.passengers = []
                            self.check_victory()
                        elif solve_rect.collidepoint(mx, my):
                            self.start_solve()
                        else:
                            for item in items_list:
                                if item in self.passengers:
                                    idx = self.passengers.index(item)
                                    rect = pygame.Rect(bx + 70 + idx * 60, by - 30, 70, 70)
                                else:
                                    x = 30 if self.side[item] == 0 else 650
                                    y_o = {'wolf': 0, 'sheep': 75, 'cabbage': 150}
                                    final_x = x + y_o[item] if x == 30 else x - y_o[item] + 120
                                    rect = pygame.Rect(final_x, 320, 70, 70)
                                
                                if rect.collidepoint(mx, my):
                                    if item in self.passengers: self.passengers.remove(item)
                                    elif len(self.passengers) < 2 and self.side[item] == self.boat_side:
                                        self.passengers.append(item)
                                    self.check_victory()
                                    break

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    RiverGame().run()