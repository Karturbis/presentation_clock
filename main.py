"""A simple stopwatch for presentations"""

import pygame
import time

#consts:
WINDOW_SIZE = (1920, 1000)
BG_COLOR = "black"
FG_COLOR = "green"
FG_COLOR_2 = "white"
FG_COLOR_WARNING = "yellow"
FG_COLOR_CRITICAL = "red"
BG_COLOR_TIME_OVER = "red"
FG_COLOR_TIME_OVER = "black"
DELTATIME_POSITION: tuple = (WINDOW_SIZE[0]/16, WINDOW_SIZE[1]/2)
# 3 min = 180s
# 4 min = 240s
# 5 min = 300s
# 9 min = 540s
# 9.5 min = 570s
# 10 min = 600s
# 15 min = 900s
WARNING_TIME_SEC = 560
CRITICAL_TIME_SEC = 585
TIME_OVER_SEC = 600
FPS = 60
TIME_JUMP_SMALL = 10
TIME_JUMP_BIG = 30
SCREEN = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Presentation Timer")


class Clock():

    def __init__(self):
        # initialize pygame:
        pygame.init()
        pygame.font.init()
        pygame.display.init()
        self.clock = pygame.time.Clock()
        icon = pygame.image.load("icon.png")
        pygame.display.set_icon(icon)
        # Initialize fonts:
        self.font = pygame.font.SysFont("mono", 200)
        self.font_big = pygame.font.SysFont("mono", 350)
        self.delta_time = 0
        # init placement variables:
        # variables:
        self.saved_times: list = [0, 0]
        self.localtime_position: tuple = (WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/4)
        self.savetime_positions: list[tuple] = [
            (WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/4),
            (WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/4),
            ]


    def draw_time(self):
        time_now = time.strftime("%H:%M:%S", time.localtime())
        text = self.font.render(str(time_now), True, FG_COLOR_2)
        SCREEN.blit(text, self.localtime_position)

    def draw_saved_times(self):
        for e, saved_time in enumerate(self.saved_times):
            if saved_time:
                text = self.font.render(saved_time, True, FG_COLOR_2)
                SCREEN.blit(text, self.savetime_positions[e])

    def draw_delta_time(self, delta_time, running):
        print_color = FG_COLOR_2
        if running:
            print_color = FG_COLOR
            if delta_time >= WARNING_TIME_SEC:
                print_color = FG_COLOR_WARNING
            if delta_time >= CRITICAL_TIME_SEC:
                print_color = FG_COLOR_CRITICAL
            if delta_time >= TIME_OVER_SEC:
                print_color = FG_COLOR_TIME_OVER
        delta_time = time.strftime("%H:%M:%S" , time.gmtime(delta_time))
        text = self.font_big.render(str(delta_time), True, print_color)
        SCREEN.blit(text, DELTATIME_POSITION)

    def main(self):
        start_time = 0
        end_time = 0
        running: bool = False
        while True:
            for event in pygame.event.get(): # event listener
                # making the window closable:
                if event.type == pygame.QUIT:
                    pygame.QUIT
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.QUIT
                        exit(0)
                    elif event.key == pygame.K_SPACE:
                        if not running:
                            start_time = int(time.time())-end_time+start_time # round, so both clocks update at the same time
                            running = True
                        else:
                            running = False
                            end_time = int(time.time())
                    elif event.key == pygame.K_r:
                        start_time = int(time.time())
                        end_time = int(time.time())
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                        start_time += TIME_JUMP_BIG
                        if int(time.time())-start_time < 0:
                            start_time = int(time.time())
                        if int(end_time-start_time) < 0 and not running:
                            start_time = end_time
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                        start_time -= TIME_JUMP_BIG
                    elif event.key == pygame.K_1:
                        # save the current stopwatch time to slot 1
                        if running:
                            self.saved_times[0] = str(time.strftime("%H:%M:%S" , time.gmtime(self.delta_time)))
                        else:
                            self.saved_times[0] = str(time.strftime("%H:%M:%S" , time.gmtime(end_time-start_time)))
                        # update clock positions
                        if self.saved_times[1]:
                            self.savetime_positions[0] = (WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/6)
                            self.savetime_positions[1] = (WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/3)
                            self.localtime_position = (WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/128)
                        else:
                            self.savetime_positions[0] = (WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/3)
                            self.localtime_position = (WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/8)
                    elif event.key == pygame.K_2:
                         # save the current stopwatch time to slot 2
                        if running:
                            self.saved_times[1] = str(time.strftime("%H:%M:%S" , time.gmtime(self.delta_time)))
                        else:
                            self.saved_times[1] = str(time.strftime("%H:%M:%S" , time.gmtime(end_time-start_time)))
                        # update clock positions
                        self.savetime_positions[0] = (WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/6)
                        self.savetime_positions[1] = (WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/3)
                        self.localtime_position = (WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/128)

            self.delta_time = time.time()-start_time
            if running and self.delta_time >= TIME_OVER_SEC:
                bg_color = BG_COLOR_TIME_OVER
            else:
                bg_color = BG_COLOR
            SCREEN.fill(bg_color)
            if running:
                self.draw_delta_time(self.delta_time, running)
            else:
                self.draw_delta_time(end_time-start_time, running)
            self.draw_time()
            self.draw_saved_times()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    clock = Clock()
    clock.main()
