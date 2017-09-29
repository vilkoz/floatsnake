import pygame
from snake import Dojo
from Snake import Snake

class SupervisedDojo(Dojo):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((900,680))
        self.snakes = []
        self.snakes.append(Snake(320, 240, (255, 9, 0), self.screen))
        self.genetics.the_best = self.snakes[0]
        self.genetics.second_best = self.snakes[0]
        self.player_snake = self.snakes[0]
        self.mode = 1
        self.data = []
        self.last_player_snake_dir = None
        self.running = True
        self.pause = 0

    def draw_snakes(self):
        for snake in self.snakes:
            if snake == self.player_snake:
                snake.draw((255, 10, 255))

    def display_info(self):
        pygame.draw.line(self.screen, (255,255,255), (640, 0), (640, 480))
        label = self.font.render((" Points: %0.0f" % self.player_snake.points), 1, (255,255,255))
        self.screen.blit(label, (640, 50))
        label = self.font.render((" Health: %0.0f" % self.player_snake.health), 1, (255,255,255))
        self.screen.blit(label, (640, 70))
        label = self.font.render((" Data smaples: %0f" % len(self.data)), 1, (255,255,255))
        self.screen.blit(label, (640, 90))
        if len(self.data) > 1000:
            label = self.font.render((" Press ESC to start train"), 1, (255,0,0))
            self.screen.blit(label, (640, 100))

    def handle_key_press(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.KEYS['left'] = 1
                if event.key == pygame.K_RIGHT:
                    self.KEYS['right'] = 1
                if event.key == pygame.K_p:
                    self.pause ^= 1
                if event.key == pygame.K_ESCAPE:
                    with open('data.txt', 'w') as f:
                        f.write(str(self.data) + '\n')
                    pygame.display.quit()
                    pygame.quit()
                    self.running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.KEYS['left'] = 0
                if event.key == pygame.K_RIGHT:
                    self.KEYS['right'] = 0

    def save_io(self):
        angle = -self.player_snake.calc_angle(self.last_player_snake_dir)
        print(angle, angle / 15)
        angle = angle / 15
        angle_arr = [0.5 + angle, 0.5]
        self.data.append([self.player_snake.gen_inputs(self.food_list), angle_arr])
    def display_snake_inputs(self):
        inputs = self.player_snake.gen_inputs(self.food_list)
        inputs = [-(x - 10000) if i < 16 else x for i, x in enumerate(inputs)]
        inputs = [200 if x > 200 else x for x in inputs]
        inputs = [((-x + 200) / 200) * 255 for x in inputs]
        colors = [(1, 1, 0), (1, 0, 1), (1, 0, 0)]
        step_x = 900 / 16
        step_y = 200 / 3
        for j in range(3):
            for i in range(16):
                draw_color = [int(x1 * inputs[j * 16 + i]) for x1 in colors[j]]
                pygame.draw.rect(self.screen, draw_color,
                    pygame.Rect(
                        (step_x * i, 480 + step_y * j),
                        (step_x, step_y)
                        )
                )
                label = self.font.render(
                        '%2.2f' % (inputs[j * 16 + i]),
                        1,
                        (255,255,255)
                        )
                self.screen.blit(label, (step_x * i, 480 + step_y * j))

    def game_loop(self):
        while self.running:
            self.screen.fill((0,20,0))
            self.last_player_snake_dir = self.player_snake.dir
            if self.pause == 0:
                self.move_snakes()
            self.check_all_snakes_collisions()
            if self.snakes[0] != self.player_snake:
                self.player_snake = self.snakes[0]
            self.genetics.update_current_best()
            self.draw_snakes()
            self.food_list.draw()
            self.display_info()
            self.display_snake_inputs()
            self.handle_key_press()
            self.save_io()
            if not self.running:
                break
            self.update_ticks()
            pygame.display.update()
        return [self.data]

def main():
    dojo = SupervisedDojo()
    dojo.game_loop()

if __name__ == "__main__":
    main()
