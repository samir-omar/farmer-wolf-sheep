import pygame
import sys
from ai_solver import get_solutions
from assets import draw_background, load_images


class RiverGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 550))
        pygame.display.set_caption("AI River Crossing Game")

        self.images = load_images()
        self.font = pygame.font.SysFont('Arial', 22, bold=True)

        self.solution_steps = []
        self.solving = False
        self.current_step = 0
        self.last_update = 0

        self.reset_game()

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

            boat_pos = [(200, 360), (430, 360)]
            bx, by = boat_pos[self.boat_side]

            # القارب والفلاح
            self.screen.blit(self.images['boat'], (bx, by))
            self.screen.blit(self.images['farmer'], (bx + 5, by - 55))

            # الركاب في القارب
            for i, item in enumerate(self.passengers):
                self.screen.blit(self.images[item], (bx + 60 + i * 50, by - 10))

            # العناصر على الأرض
            for item in ['wolf', 'sheep', 'cabbage']:
                if item not in self.passengers:
                    base_x = 20 if self.side[item] == 0 else 620
                    off = {'wolf': 0, 'sheep': 55, 'cabbage': 110}
                    self.screen.blit(self.images[item], (base_x + off[item], 320))

            # أزرار
            go_rect = pygame.Rect(250, 480, 100, 45)
            down_rect = pygame.Rect(370, 480, 100, 45)
            solve_rect = pygame.Rect(490, 480, 100, 45)

            pygame.draw.rect(self.screen, (0, 150, 0), go_rect)
            pygame.draw.rect(self.screen, (200, 0, 0), down_rect)
            pygame.draw.rect(self.screen, (0, 120, 255), solve_rect)

            self.screen.blit(self.font.render("GO", True, (255, 255, 255)), (280, 490))
            self.screen.blit(self.font.render("DOWN", True, (255, 255, 255)), (385, 490))
            self.screen.blit(self.font.render("SOLVE", True, (255, 255, 255)), (500, 490))

            # رسالة
            if self.solving:
                self.message = "AI is solving..."

            msg = self.font.render(self.message, True, (255, 255, 255))
            self.screen.blit(msg, (400 - msg.get_width() // 2, 70))

            # AI Animation
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

            # الأحداث
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    # SOLVE
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

                    # GO
                    elif go_rect.collidepoint(mx, my) and not self.solving:
                        self.boat_side = 1 - self.boat_side

                        for p in self.passengers:
                            self.side[p] = self.boat_side

                        self.passengers = []

                        failed, msg = self.check_failure()
                        if failed:
                            self.message = msg

                        self.check_victory()

                    # DOWN
                    elif down_rect.collidepoint(mx, my):
                        self.passengers = []

                    # اختيار العناصر
                    else:
                        for item in ['wolf', 'sheep', 'cabbage']:
                            rect = self.get_item_rect(item, bx, by)

                            if rect.collidepoint(mx, my):
                                if item in self.passengers:
                                    self.passengers.remove(item)
                                elif len(self.passengers) < 2 and self.side[item] == self.boat_side:
                                    self.passengers.append(item)
                                break

            pygame.display.flip()


if __name__ == "__main__":
    RiverGame().run()