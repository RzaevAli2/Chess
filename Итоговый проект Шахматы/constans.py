import pygame as pg
START_Y = 41
START_X = 42
BOARD_SIZE = 612
RECT_WIDTH = (BOARD_SIZE - (START_X + START_Y)) // 8
BOARD_RECTS = []
for i in range(8):  # i-номер ряда
    BOARD_RECTS.append([])
    for j in range(8):  # номер клетки в ряду(номер столбца)
        # добавляем прямоугольник в последний ряд
        BOARD_RECTS[-1].append(pg.Rect(START_X + RECT_WIDTH * j, START_Y + RECT_WIDTH * i, RECT_WIDTH, RECT_WIDTH))
