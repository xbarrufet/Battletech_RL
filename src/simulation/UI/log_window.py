from collections import deque

import pygame




class LogWindow:

    def __init__(self,origin_x, origin_y, screen_width,screen_height, height_log=20) -> None:
        self.log_strings = deque(maxlen=int(screen_height/height_log))
        self.font = pygame.font.Font('freesansbold.ttf', 12)
        self.log_rects = []
        self.origin_x=origin_x
        self.origin_y=origin_y
        self.screen_width=screen_width
        self.screen_height=screen_height
        self.height_log=height_log


    def add_log(self,log:str):
        self.log_strings.append(log)

    def draw_logs(self, screen:pygame.Surface):
        for i,log in enumerate(self.log_strings):
            text = self.font.render(log, True,(0,0,0),(255,255,255))
            textRect = text.get_rect()
            textRect.midleft= (self.origin_x,self.origin_y + i *self.height_log)
            screen.blit(text, textRect)