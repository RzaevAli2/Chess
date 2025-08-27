from constans import *
class Button:
    def __init__(self, image, board_x, board_y, color,piece):
        self.image = image
        self.board_x = board_x
        self.board_y = board_y
        self.color = color
        self.piece = piece

    def draw(self, screen:pg.Surface):
        current_rect = BOARD_RECTS[self.board_y][self.board_x]
        screen.blit(self.image, (current_rect.x, current_rect.y))

