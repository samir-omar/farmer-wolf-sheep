# import pygame
# import sys

# # محاولة تحميل الصور أو استخدام البدائل
# try:
#     from assets import draw_background, load_images
# except ImportError:
#     def draw_background(screen):
#         screen.fill((135, 206, 235))
#         pygame.draw.rect(screen, (139, 69, 19), (0, 400, 200, 150))
#         pygame.draw.rect(screen, (139, 69, 19), (600, 400, 200, 150))
#         pygame.draw.rect(screen, (0, 105, 148), (200, 420, 400, 130))
#     def load_images():
#         imgs = {}
#         for n in ['boat', 'farmer', 'wolf', 'sheep', 'cabbage']:
#             s = pygame.Surface((60, 60), pygame.SRCALPHA)
#             pygame.draw.circle(s, (200, 200, 200), (30, 30), 25)
#             imgs[n] = s
#         return imgs

# class RiverGame:
#     def __init__(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode((800, 550))
#         pygame.display.set_caption("AI Project: Farmer, Fox & Goat")
#         self.images = load_images()
#         self.font = pygame.font.SysFont('Arial', 22, bold=True)
#         self.score = 0 
#         self.reset_game()

#     def reset_game(self):
#         self.side = {'wolf': 0, 'sheep': 0, 'cabbage': 0}
#         self.boat_side = 0
#         self.passengers = [] 
#         self.game_over = False
#         self.mission_complete = False 
#         self.message = "Goal: Use the men to protect everyone!"

#     def check_victory(self):
#         # شرط الفوز: الكل في الضفة اليمين (1) والقارب فاضي
#         everyone_on_right = all(v == 1 for v in self.side.values())
#         boat_empty = len(self.passengers) == 0
#         if everyone_on_right and boat_empty:
#             self.mission_complete = True
#             self.message = "YOU ARE WIN!"
#             return True
#         return False

#     def check_failure(self):
#         boat_zone = self.passengers + ['farmer']
#         left_bank = [k for k, v in self.side.items() if v == 0 and k not in self.passengers]
#         right_bank = [k for k, v in self.side.items() if v == 1 and k not in self.passengers]
#         if self.boat_side == 0: left_bank.append('farmer')
#         else: right_bank.append('farmer')

#         for area in [boat_zone, left_bank, right_bank]:
#             has_human = 'farmer' in area
#             if not has_human:
#                 if 'wolf' in area and 'sheep' in area:
#                     return True, "Game Over! Wolf ate the Sheep!"
#                 if 'sheep' in area and 'cabbage' in area:
#                     return True, "Game Over! Sheep ate the Cabbage!"
#         return False, ""

#     def run(self):
#         while True:
#             draw_background(self.screen)
#             boat_pos = [(200, 360), (430, 360)]
#             bx, by = boat_pos[self.boat_side]
#             self.screen.blit(self.images['boat'], (bx, by))
#             self.screen.blit(self.images['farmer'], (bx + 5, by - 55))

#             items_list = ['wolf', 'sheep', 'cabbage']
#             for item in items_list:
#                 if item in self.passengers:
#                     idx = self.passengers.index(item)
#                     self.screen.blit(self.images[item], (bx + (65 if idx == 0 else 110), by - 45))
#                 else:
#                     base_x = 20 if self.side[item] == 0 else 620
#                     off = {'wolf': 0, 'sheep': 55, 'cabbage': 110}
#                     self.screen.blit(self.images[item], (base_x + off[item], 320))

#             score_surf = self.font.render(f"SCORE: {self.score}", True, (0, 0, 0))
#             self.screen.blit(score_surf, (20, 20))

#             retry_rect = pygame.Rect(350, 220, 100, 50)
#             add_score_rect = pygame.Rect(325, 220, 150, 50) 

#             if self.game_over:
#                 pygame.draw.rect(self.screen, (50, 50, 50), retry_rect, border_radius=5)
#                 self.screen.blit(self.font.render("RETRY", True, (255, 255, 255)), (365, 232))
#             elif self.mission_complete:
#                 pygame.draw.rect(self.screen, (0, 100, 200), add_score_rect, border_radius=5)
#                 self.screen.blit(self.font.render("ADD SCORE", True, (255, 255, 255)), (340, 232))
#             else:
#                 go_rect = pygame.Rect(300, 480, 90, 45)
#                 pygame.draw.rect(self.screen, (0, 150, 0), go_rect, border_radius=8)
#                 self.screen.blit(self.font.render("GO", True, (255, 255, 255)), (330, 490))
#                 down_rect = pygame.Rect(410, 480, 90, 45)
#                 pygame.draw.rect(self.screen, (200, 0, 0), down_rect, border_radius=8)
#                 self.screen.blit(self.font.render("DOWN", True, (255, 255, 255)), (420, 490))

#             msg_color = (255, 50, 50) if self.game_over else (0, 200, 0) if self.mission_complete else (255, 255, 255)
#             msg_surf = self.font.render(self.message, True, msg_color)
#             self.screen.blit(msg_surf, (400 - msg_surf.get_width()//2, 70))

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT: pygame.quit(); sys.exit()
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     mx, my = event.pos
                    
#                     if self.game_over and retry_rect.collidepoint(mx, my):
#                         self.reset_game()
#                     elif self.mission_complete and add_score_rect.collidepoint(mx, my):
#                         self.score += 10 
#                         self.reset_game()

#                     elif not self.game_over and not self.mission_complete:
#                         if go_rect.collidepoint(mx, my):
#                             self.boat_side = 1 - self.boat_side
#                             for p in self.passengers: self.side[p] = self.boat_side
#                             failed, msg = self.check_failure()
#                             if failed: self.game_over, self.message = True, msg
#                             # فحص الفوز بعد الحركة مباشرة
#                             self.check_victory()
                        
#                         elif down_rect.collidepoint(mx, my):
#                             self.passengers = []
#                             # فحص الفوز بعد تنزيل الكل
#                             self.check_victory()
                        
#                         else:
#                             for item in items_list:
#                                 if item in self.passengers:
#                                     idx = self.passengers.index(item)
#                                     rect = pygame.Rect(bx + (65 if idx == 0 else 110), by - 45, 60, 60)
#                                 else:
#                                     base_x = 20 if self.side[item] == 0 else 620
#                                     off = {'wolf': 0, 'sheep': 55, 'cabbage': 110}
#                                     rect = pygame.Rect(base_x + off[item], 320, 60, 60)
#                                 if rect.collidepoint(mx, my):
#                                     if item in self.passengers: 
#                                         self.passengers.remove(item)
#                                         # فحص الفوز فور إنزال العنصر
#                                         self.check_victory()
#                                     elif len(self.passengers) < 2 and self.side[item] == self.boat_side:
#                                         self.passengers.append(item)
#                                     break

#             pygame.display.flip()

# if __name__ == "__main__":
#     RiverGame().run()

import pygame
import sys
from ai_solver import get_solutions

# fallback assets
try:
    from assets import draw_background, load_images
except ImportError:
    def draw_background(screen):
        screen.fill((135, 206, 235))
        pygame.draw.rect(screen, (139, 69, 19), (0, 400, 200, 150))
        pygame.draw.rect(screen, (139, 69, 19), (600, 400, 200, 150))
        pygame.draw.rect(screen, (0, 105, 148), (200, 420, 400, 130))

    def load_images():
        imgs = {}
        for n in ['boat', 'farmer', 'wolf', 'sheep', 'cabbage']:
            s = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.circle(s, (200, 200, 200), (30, 30), 25)
            imgs[n] = s
        return imgs


class RiverGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 550))
        pygame.display.set_caption("AI Project: Farmer, Wolf & Sheep")

        self.images = load_images()
        self.font = pygame.font.SysFont('Arial', 22, bold=True)

        self.score = 0

        # AI control
        self.solution_steps = []
        self.solving = False
        self.current_step = 0
        self.last_update = 0

        self.reset_game()

    # ================= FIXED =================
    def get_item_rect(self, item, bx, by):
        if item in self.passengers:
            idx = self.passengers.index(item)
            return pygame.Rect(bx + (65 if idx == 0 else 110), by - 45, 60, 60)
        else:
            base_x = 20 if self.side[item] == 0 else 620
            off = {'wolf': 0, 'sheep': 55, 'cabbage': 110}
            return pygame.Rect(base_x + off[item], 320, 60, 60)

    def reset_game(self):
        self.side = {'wolf': 0, 'sheep': 0, 'cabbage': 0}
        self.boat_side = 0
        self.passengers = []
        self.game_over = False
        self.mission_complete = False
        self.message = "Goal: Move everyone safely!"

    def get_state_for_ai(self):
        return {
            'farmer': self.boat_side,
            'wolf': self.side['wolf'],
            'sheep': self.side['sheep'],
            'cabbage': self.side['cabbage']
        }

    def check_victory(self):
        if all(v == 1 for v in self.side.values()) and len(self.passengers) == 0:
            self.mission_complete = True
            self.message = "YOU WIN!"
            return True
        return False

    def check_failure(self):
        left = [k for k, v in self.side.items() if v == 0]
        right = [k for k, v in self.side.items() if v == 1]

        if self.boat_side == 0:
            left.append('farmer')
        else:
            right.append('farmer')

        for area in [left, right]:
            if 'farmer' not in area:
                if 'wolf' in area and 'sheep' in area:
                    return True, "Wolf ate sheep!"
                if 'sheep' in area and 'cabbage' in area:
                    return True, "Sheep ate cabbage!"
        return False, ""

    def run(self):
        while True:
            draw_background(self.screen)

            # ===== boat =====
            boat_pos = [(200, 360), (430, 360)]
            bx, by = boat_pos[self.boat_side]

            self.screen.blit(self.images['boat'], (bx, by))
            self.screen.blit(self.images['farmer'], (bx + 5, by - 55))
            
            # ===== رسم الركاب داخل القارب =====
            drawn=set()
            
            for i,item in enumerate(self.passengers):
                if item in drawn: continue
                self.screen.blit(
                    self.images[item],
                    (bx + 60 + i * 50, by - 10)
                )
                drawn.add(item)
            # ===== items =====
            items_list = ['wolf', 'sheep', 'cabbage']

            for item in items_list:
                
            # لو في القارب → ارسمه في القارب فقط
                if item in self.passengers:
                    idx = self.passengers.index(item)
                    self.screen.blit(
                    self.images[item],
                    (bx + 60 + idx * 50, by - 10)
                )

            # لو مش في القارب → ارسمه في البر فقط
                else:
                    base_x = 20 if self.side[item] == 0 else 620
                    off = {'wolf': 0, 'sheep': 55, 'cabbage': 110}
                    self.screen.blit(self.images[item], (base_x + off[item], 320))

            # ===== buttons =====
            go_rect = pygame.Rect(250, 480, 100, 45)
            pygame.draw.rect(self.screen, (0, 150, 0), go_rect, border_radius=8)
            self.screen.blit(self.font.render("GO", True, (255, 255, 255)), (280, 490))

            down_rect = pygame.Rect(370, 480, 100, 45)
            pygame.draw.rect(self.screen, (200, 0, 0), down_rect, border_radius=8)
            self.screen.blit(self.font.render("DOWN", True, (255, 255, 255)), (385, 490))

            solve_rect = pygame.Rect(490, 480, 100, 45)
            pygame.draw.rect(self.screen, (0, 120, 255), solve_rect, border_radius=8)
            self.screen.blit(self.font.render("SOLVE", True, (255, 255, 255)), (500, 490))

            # ===== message =====
            if self.solving:
                self.message = "AI is solving..."

            msg = self.font.render(self.message, True, (255, 255, 255))
            self.screen.blit(msg, (400 - msg.get_width() // 2, 70))

            # ===== AI animation =====
            if self.solving and self.solution_steps:
                now = pygame.time.get_ticks()
                if now - self.last_update > 800:
                    if self.current_step < len(self.solution_steps):
                        step = self.solution_steps[self.current_step]

                        self.boat_side = step['farmer']
                        self.side['wolf'] = step['wolf']
                        self.side['sheep'] = step['sheep']
                        self.side['cabbage'] = step['cabbage']

                        self.current_step += 1
                        self.last_update = now
                    else:
                        self.solving = False
                        self.check_victory()

            # ===== EVENTS =====
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    # ================= SOLVE =================
                    if solve_rect.collidepoint(mx, my):

                        class Logic:
                            def is_win(_, state):
                                return all(v == 1 for v in state.values())

                            def is_valid(_, state):
                                left = [k for k, v in state.items() if v == 0]
                                right = [k for k, v in state.items() if v == 1]

                                for area in [left, right]:
                                    if 'farmer' not in area:
                                        if 'wolf' in area and 'sheep' in area:
                                            return False
                                        if 'sheep' in area and 'cabbage' in area:
                                            return False
                                return True

                        solution = get_solutions(self.get_state_for_ai(), Logic())

                        if solution:
                            self.solution_steps = solution
                            self.current_step = 0
                            self.solving = True
                            self.last_update = pygame.time.get_ticks()

                    # ================= GO =================
                    elif go_rect.collidepoint(mx, my) and not self.solving:
                        self.boat_side = 1 - self.boat_side

                        for p in self.passengers:
                            self.side[p] = self.boat_side

                        self.passengers = []

                        failed, msg = self.check_failure()
                        if failed:
                            self.game_over = True
                            self.message = msg

                        self.check_victory()

                    # ================= DOWN =================
                    elif down_rect.collidepoint(mx, my) and not self.solving:
                        self.passengers = []
                        self.check_victory()

                    # ================= FIXED CLICK LOGIC =================
                    else:
                        for item in items_list:
                            rect = self.get_item_rect(item, bx, by)

                            if rect.collidepoint(mx, my) and not self.solving:

                                if item in self.passengers:
                                    self.passengers.remove(item)

                                elif len(self.passengers) < 2 and self.side[item] == self.boat_side:
                                    if item not in self.passengers:
                                        self.passengers.append(item)

                                break

            pygame.display.flip()


if __name__ == "__main__":
    RiverGame().run()