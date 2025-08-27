# for board_y in range(0, 8):
#     for board_x in range(0, 8):
#         rect = BOARD_RECTS[board_y][board_x]
#         if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
#             pg.draw.rect(screen, "green", rect)
#             pg.display.flip()
#             print(board_x,board_y)
#             pg.time.wait(1000)

# for row in BOARD_RECTS:
#     for rect in row:
#         for _x in range(rect.left, rect.right):
#             if x == _x:
#                 for _y in range(rect.top, rect.bottom):
#                     if y == _y:
#                         pg.draw.rect(screen, "green", rect)
#                         pg.display.flip()
#                         pg.time.wait(1000)
Rook("white", 7, 7, white_rook_image)
Knight("white", 1, 7, white_knight_image), Knight("white", 6, 7, white_knight_image),
Bishop("white", 2, 7, white_bishop_image), Bishop("white", 5, 7, white_bishop_image),
Queen("white", 3, 7, white_queen_image)