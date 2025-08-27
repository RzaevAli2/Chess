import pygame as pg
from board import Board
from constans import *


def main():
    """
    создание окна,поля,основной игровой цикл
    :return: None
    """
    size = BOARD_SIZE, BOARD_SIZE
    screen = pg.display.set_mode(size)
    # картинки
    board_image = pg.image.load("Images/поле.jpg")
    board = Board(board_image)
    # основной цикл
    while True:
        board.draw(screen)
        pg.display.flip()
        # print(board.is_check())
        # обработка событий
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                place_mouse = pg.mouse.get_pos()
                x, y = place_mouse

                board_x = (x - START_X) // RECT_WIDTH
                board_y = (y - START_Y) // RECT_WIDTH
                if 7 >= board_x >= 0 and 7 >= board_y >= 0:
                    board.update(board_x, board_y)


            elif event.type == pg.QUIT:
                return


if __name__ == '__main__':
    main()
