import pygame as pg
from constans import *


class Piece:
    def __init__(self, color: str, x: int, y: int, image: pg.Surface):
        self._color = color
        self._x = x
        self._y = y  # координаты клетки на поле
        self._image = image
        self._possible_moves = []
        self._possible_kills = []



    def __str__(self):
        return f"Местоположение:{(self._x, self._y)} Цвет:{self._color} Тип:{type(self)}"

    def draw(self, screen: pg.Surface):
        current_rect = BOARD_RECTS[self._y][self._x]
        screen.blit(self._image, (current_rect.x, current_rect.y))

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def draw_direction(self, screen: pg.Surface):
        pg.draw.rect(screen, "yellow", BOARD_RECTS[self._y][self._x])
        pg.draw.rect(screen, "brown", BOARD_RECTS[self._y][self._x],3)
        for x, y in self._possible_moves:
            pg.draw.rect(screen, "yellow", BOARD_RECTS[y][x],)
            pg.draw.rect(screen,"brown", BOARD_RECTS[y][x], 3)
        for x, y in self._possible_kills:
            pg.draw.rect(screen, "red", BOARD_RECTS[y][x])
            pg.draw.rect(screen, "brown", BOARD_RECTS[y][x], 3)
    def is_in_possible_moves(self, board_x, board_y):
        if (board_x, board_y) in self._possible_moves:
            return True
        else:
            return False

    def is_in_possible_kills(self, board_x, board_y):
        if (board_x, board_y) in self._possible_kills:
            return True
        else:
            return False

    def is_black(self):
        return self._color == "black"

    def is_white(self):
        return self._color == "white"

    def no_moves(self):
        if not self._possible_moves and not self._possible_kills:
            return True
        else:
            return False

    def update(self, board):
        self.calculate_possible_moves(board)
        old_possible_moves = self._possible_moves.copy()
        new_possible_moves = []
        for x, y in old_possible_moves:
            real_x = self._x
            real_y = self._y
            self._x = x
            self._y = y
            if not board.pseudo_check():
                new_possible_moves.append((x, y))
            self._x = real_x
            self._y = real_y
        self._possible_moves = new_possible_moves
        old_possible_kills = self._possible_kills.copy()
        new_possible_kills = []

        for x, y in old_possible_kills:
            real_x = self._x
            real_y = self._y
            phantom_piece = board.get_piece(x, y)
            self._x = x
            self._y = y
            if not board.pseudo_check(phantom_piece):
                new_possible_kills.append((x, y))
            self._x = real_x
            self._y = real_y
        self._possible_kills = new_possible_kills

    def calculate_possible_moves(self, board):
        pass


class Rook(Piece):  # ладья
    def __init__(self, color: str, x: int, y: int, image: pg.Surface):
        Piece.__init__(self, color, x, y, image)
        self.is_moved = False

    def calculate_possible_moves(self, board):
        self._possible_moves = []
        self._possible_kills = []

        for left in range(self._x - 1, -1, -1):
            piece = board.get_piece(left, self._y)
            # если нет фигуры
            if piece is None:
                self._possible_moves.append((left, self._y))
            # если другого цвета
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((left, self._y))
                break
            # если того же цвета
            else:
                break

        for right in range(self._x + 1, 8):
            piece = board.get_piece(right, self._y)
            # если нет фигуры
            if piece is None:
                self._possible_moves.append((right, self._y))
            # если другого цвета
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((right, self._y))
                break
            # если того же цвета
            else:
                break

        for up in range(self._y - 1, -1, -1):
            piece = board.get_piece(self._x, up)
            # если нет фигуры
            if piece is None:
                self._possible_moves.append((self._x, up))
            # если другого цвета
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((self._x, up))
                break
            # если того же цвета
            else:
                break

        for down in range(self._y + 1, 8):
            piece = board.get_piece(self._x, down)
            # если нет фигуры
            if piece is None:
                self._possible_moves.append((self._x, down))
            # если другого цвета
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((self._x, down))
                break
            # если того же цвета
            else:
                break


class Knight(Piece):  # конь

    def calculate_possible_moves(self, board):
        self._possible_moves = []
        self._possible_kills = []

        moves = (-1, -2), (-2, -1), (-1, 2), (-2, 1), (1, 2), (2, 1), (2, -1), (1, -2)
        for x, y in moves:
            if 7 >= self._x - x >= 0 and 7 >= self._y - y >= 0:
                piece = board.get_piece(self._x - x, self._y - y)
                # если нет фигуры
                if piece is None:
                    self._possible_moves.append((self._x - x, self._y - y))
                # если другого цвета
                elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                    self._possible_kills.append((self._x - x, self._y - y))


class Queen(Piece):

    def calculate_possible_moves(self, board):
        self._possible_moves = []
        self._possible_kills = []

        for left in range(self._x - 1, -1, -1):
            piece = board.get_piece(left, self._y)
            # если нет фигуры
            if piece is None:
                self._possible_moves.append((left, self._y))
            # если другого цвета
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((left, self._y))
                break
            # если того же цвета
            else:
                break

        for right in range(self._x + 1, 8):
            piece = board.get_piece(right, self._y)
            # если нет фигуры
            if piece is None:
                self._possible_moves.append((right, self._y))
            # если другого цвета
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((right, self._y))
                break
            # если того же цвета
            else:
                break

        for up in range(self._y - 1, -1, -1):
            piece = board.get_piece(self._x, up)
            # если нет фигуры
            if piece is None:
                self._possible_moves.append((self._x, up))
            # если другого цвета
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((self._x, up))
                break
            # если того же цвета
            else:
                break

        for down in range(self._y + 1, 8):
            piece = board.get_piece(self._x, down)
            # если нет фигуры
            if piece is None:
                self._possible_moves.append((self._x, down))
            # если другого цвета
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((self._x, down))
                break
            # если того же цвета
            else:
                break
        shift = 1
        while self._x - shift >= 0 and self._y - shift >= 0:
            piece = board.get_piece(self._x - shift, self._y - shift)
            if piece is None:
                self._possible_moves.append((self._x - shift, self._y - shift))
                shift += 1
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((self._x - shift, self._y - shift))
                break
            else:
                break
        shift = 1
        while self._x - shift >= 0 and self._y + shift <= 7:
            piece = board.get_piece(self._x - shift, self._y + shift)
            if piece is None:
                self._possible_moves.append((self._x - shift, self._y + shift))
                shift += 1
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((self._x - shift, self._y + shift))
                break
            else:
                break

        shift = 1
        while self._x + shift <= 7 and self._y - shift >= 0:
            piece = board.get_piece(self._x + shift, self._y - shift)
            if piece is None:
                self._possible_moves.append((self._x + shift, self._y - shift))
                shift += 1
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((self._x + shift, self._y - shift))
                break
            else:
                break

        shift = 1
        while self._x + shift <= 7 and self._y + shift <= 7:
            piece = board.get_piece(self._x + shift, self._y + shift)
            if piece is None:
                self._possible_moves.append((self._x + shift, self._y + shift))
                shift += 1
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((self._x + shift, self._y + shift))
                break
            else:
                break


class King(Piece):
    def __init__(self, color: str, x: int, y: int, image: pg.Surface):
        Piece.__init__(self, color, x, y, image)
        self.is_moved = False

    def calculate_possible_moves(self, board):
        self._possible_kills = []
        self._possible_moves = []
        for x in -1, 0, 1:
            for y in -1, 0, 1:
                new_x = self._x + x
                new_y = self._y + y
                if x == 0 and y == 0:
                    continue
                # continue - переходит на след шаг цикла
                if 7 >= new_x >= 0 and 7 >= new_y >= 0:
                    piece = board.get_piece(new_x, new_y)
                    if piece is None:
                        enemy_color = None
                        if self.is_black():
                            enemy_color = "white"
                        else:
                            enemy_color = "black"
                        if board.is_in_enemy_moves(enemy_color, new_x, new_y):
                            continue
                        self._possible_moves.append((new_x, new_y))
                    elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                        self._possible_kills.append((new_x, new_y))
        self.castle(board)
        kills_to_remove = []
        moves_to_remove = []
        for x, y in self._possible_moves:
            if self.is_king_around(x, y, board):
                moves_to_remove.append((x, y))
        for x, y in self._possible_kills:
            if self.is_king_around(x, y, board):
                kills_to_remove.append((x, y))
        for delete in kills_to_remove:
            self._possible_kills.remove(delete)
        for delete in moves_to_remove:
            self._possible_moves.remove(delete)
    def is_king_around(self, x, y, board):
        for around_x in -1, 0, 1:
            for around_y in -1, 0, 1:
                around_piece = board.get_piece(x + around_x, y + around_y)
                if type(around_piece) is King and self != around_piece:
                    return True
        return False

    def castle(self, board):
        if self.is_moved is False:
            if self.is_white():
                right_corner = board.get_piece(7, 7)
                if type(right_corner) is Rook and right_corner.is_white() and right_corner.is_moved is False:
                    if board.get_piece(self._x + 2, self._y) is None and board.get_piece(self._x + 1, self._y) is None:
                        self._possible_moves.append((self._x + 2, self._y))
                left_corner = board.get_piece(0, 7)
                if type(left_corner) is Rook and left_corner.is_white() and left_corner.is_moved is False:
                    if (board.get_piece(self._x - 2, self._y) is None and board.get_piece(self._x - 1, self._y) is None
                            and board.get_piece(self._x - 3, self._y) is None):
                        self._possible_moves.append((self._x - 2, self._y))
            else:
                right_corner = board.get_piece(7, 0)
                if type(right_corner) is Rook and right_corner.is_black() and right_corner.is_moved is False:
                    if board.get_piece(self._x + 2, self._y) is None and board.get_piece(self._x + 1, self._y) is None:
                        self._possible_moves.append((self._x + 2, self._y))
                left_corner = board.get_piece(0, 0)
                if type(left_corner) is Rook and left_corner.is_black() and left_corner.is_moved is False:
                    if (board.get_piece(self._x - 2, self._y) is None and board.get_piece(self._x - 1, self._y) is None
                            and board.get_piece(self._x - 3, self._y) is None):
                        self._possible_moves.append((self._x - 2, self._y))


class Bishop(Piece):  # слон
    def calculate_possible_moves(self, board):
        self._possible_kills = []
        self._possible_moves = []

        shift = 1
        while self._x - shift >= 0 and self._y - shift >= 0:
            piece = board.get_piece(self._x - shift, self._y - shift)
            if piece is None:
                self._possible_moves.append((self._x - shift, self._y - shift))
                shift += 1
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((self._x - shift, self._y - shift))
                break
            else:
                break
        shift = 1
        while self._x - shift >= 0 and self._y + shift <= 7:
            piece = board.get_piece(self._x - shift, self._y + shift)
            if piece is None:
                self._possible_moves.append((self._x - shift, self._y + shift))
                shift += 1
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((self._x - shift, self._y + shift))
                break
            else:
                break

        shift = 1
        while self._x + shift <= 7 and self._y - shift >= 0:
            piece = board.get_piece(self._x + shift, self._y - shift)
            if piece is None:
                self._possible_moves.append((self._x + shift, self._y - shift))
                shift += 1
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((self._x + shift, self._y - shift))
                break
            else:
                break

        shift = 1
        while self._x + shift <= 7 and self._y + shift <= 7:
            piece = board.get_piece(self._x + shift, self._y + shift)
            if piece is None:
                self._possible_moves.append((self._x + shift, self._y + shift))
                shift += 1
            elif self._color == "white" and piece.is_black() or self._color == "black" and piece.is_white():
                self._possible_kills.append((self._x + shift, self._y + shift))
                break
            else:
                break


class Pawn(Piece):  # пешка

    def calculate_possible_moves(self, board):
        self._possible_moves = []
        self._possible_kills = []

        # white
        if self._color == "white":
            piece = board.get_piece(self._x + 1, self._y - 1)
            if piece is not None and piece.is_black():
                self._possible_kills.append((self._x + 1, self._y - 1))

            piece_2 = board.get_piece(self._x - 1, self._y - 1)
            if piece_2 is not None and piece_2.is_black():
                self._possible_kills.append((self._x - 1, self._y - 1))
            piece_3 = board.get_piece(self._x - 1, self._y)
            # if piece_2 is None and piece_3 is Pawn and piece_3 is self._color == "black" and piece_3._y == 3 :
            #     self._possible_kills.append((self._x - 1, self._y))



            if board.get_piece(self._x, self._y - 1) is None:


                self._possible_moves.append((self._x, self._y - 1))
                if self._y == 6 and board.get_piece(self._x, self._y - 2) is None:
                    self._possible_moves.append((self._x, self._y - 2))

        # black
        else:
            piece = board.get_piece(self._x + 1, self._y + 1)
            if piece is not None and piece.is_white():
                self._possible_kills.append((self._x + 1, self._y + 1))
            piece_2 = board.get_piece(self._x - 1, self._y + 1)
            if piece_2 is not None and piece_2.is_white():
                self._possible_kills.append((self._x - 1, self._y + 1))
            if board.get_piece(self._x, self._y + 1) is None:
                self._possible_moves.append((self._x, self._y + 1))
                if self._y == 1 and board.get_piece(self._x, self._y + 2) is None:
                    self._possible_moves.append((self._x, self._y + 2))
