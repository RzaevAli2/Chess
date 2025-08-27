import sys
from button import Button
from pieces import *
from constans import *


class Board:
    def __init__(self, image):
        self.__current_piece: Piece | None = None
        self.__turn = "white"
        self.__image = image
        self.__is_check = False
        self.__end_pawn = (0, 0)
        # self.rects_quantity = 64
        # self.width = 1800
        # self.height = 900
        # self.size = (self.width, self.height)
        # фото коня
        self.black_knight_image = pg.image.load("Images/черный конь.png")
        self.black_knight_image = pg.transform.scale(self.black_knight_image, (60, 60))
        self.white_knight_image = pg.image.load("Images/белый конь.png")
        self.white_knight_image = pg.transform.scale(self.white_knight_image, (60, 60))
        # фото ладьи
        self.black_rook_image = pg.image.load("Images/черная ладья.png")
        self.black_rook_image = pg.transform.scale(self.black_rook_image, (60, 60))
        self.white_rook_image = pg.image.load("Images/белая ладья.png")
        self.white_rook_image = pg.transform.scale(self.white_rook_image, (60, 60))
        # фото слона
        self.black_bishop_image = pg.image.load("Images/черный слон.png")
        self.black_bishop_image = pg.transform.scale(self.black_bishop_image, (60, 60))
        self.white_bishop_image = pg.image.load("Images/белый слон.png")
        self.white_bishop_image = pg.transform.scale(self.white_bishop_image, (60, 60))
        # фото короля
        self.black_king_image = pg.image.load("Images/черныц король.png")
        self.black_king_image = pg.transform.scale(self.black_king_image, (60, 60))
        self.white_king_image = pg.image.load("Images/белый король.png")
        self.white_king_image = pg.transform.scale(self.white_king_image, (60, 60))
        # фото ферзя
        self.black_queen_image = pg.image.load("Images/черный ферзь.png")
        self.black_queen_image = pg.transform.scale(self.black_queen_image, (60, 60))
        self.white_queen_image = pg.image.load("Images/белый ферзь.png")
        self.white_queen_image = pg.transform.scale(self.white_queen_image, (60, 60))

        # фото пешки
        white_pawn_image = pg.image.load("Images/белая пешка.png")
        white_pawn_image = pg.transform.scale(white_pawn_image, (60, 60))
        black_pawn_image = pg.image.load("Images/черная пешка.png")
        black_pawn_image = pg.transform.scale(black_pawn_image, (60, 60))
        # фигуры
        self.__pieces = [Rook("white", 7, 7, self.white_rook_image), Rook("black", 0, 0, self.black_rook_image),
                         Rook("black", 7, 0, self.black_rook_image), Rook("white", 0, 7, self.white_rook_image),
                         Knight("black", 1, 0, self.black_knight_image), Knight("black", 6, 0, self.black_knight_image),
                         Rook("white", 7, 7, self.white_rook_image),
                         Knight("white", 1, 7, self.white_knight_image), Knight("white", 6, 7, self.white_knight_image),
                         Bishop("white", 2, 7, self.white_bishop_image), Bishop("white", 5, 7, self.white_bishop_image),
                         Queen("white", 3, 7, self.white_queen_image),
                         Bishop("black", 2, 0, self.black_bishop_image), Bishop("black", 5, 0, self.black_bishop_image),
                         King("black", 4, 0, self.black_king_image), King("white", 4, 7, self.white_king_image),
                         Queen("black", 3, 0, self.black_queen_image,)
                         ]

        for x in range(8):
            self.__pieces.append(Pawn("white", x, 6, white_pawn_image))
            self.__pieces.append(Pawn("black", x, 1, black_pawn_image))
        # кнопки выбора фигуры
        self.__buttons = []

    def draw(self, screen: pg.Surface):
        screen.blit(self.__image, (0, 0))
        if self.__current_piece is not None:
            self.__current_piece.draw_direction(screen)

        for piece in self.__pieces:
            piece.draw(screen)
        self.buttons(screen)


    def choose_piece(self, board_x: int, board_y: int):
        # print(self.__is_check)
        for piece in self.__pieces:
            if board_x == piece.get_x() and board_y == piece.get_y():
                if self.__current_piece == piece:
                    self.__current_piece = None
                elif self.__turn == "white" and piece.is_white():
                    self.__current_piece = piece
                    piece.update(self)

                elif self.__turn == "black" and piece.is_black():
                    self.__current_piece = piece
                    piece.update(self)

    def get_piece(self, board_x: int, board_y: int) -> Piece | None:
        for piece in self.__pieces:
            if board_x == piece.get_x() and board_y == piece.get_y():
                return piece
        return None

    def move(self, board_x: int, board_y: int):

        if self.__current_piece is not None:
            kill = self.__current_piece.is_in_possible_kills(board_x, board_y)
            if self.__current_piece.is_in_possible_moves(board_x, board_y) or kill:
                if kill:
                    killing_piece = self.get_piece(board_x, board_y)
                    self.__pieces.remove(killing_piece)
                if type(self.__current_piece) is Rook:
                    self.__current_piece.is_moved = True

                if type(self.__current_piece) is King:
                    self.__current_piece.is_moved = True
                    if self.__current_piece._x - board_x == 2:
                        left_corner = self.get_piece(self.__current_piece._x - 4, self.__current_piece._y)
                        left_corner._x += 3
                    elif self.__current_piece._x - board_x == -2:
                        right_corner = self.get_piece(self.__current_piece._x + 3, self.__current_piece._y)
                        right_corner._x -= 2
                self.__current_piece._x = board_x
                self.__current_piece._y = board_y
                if type(self.__current_piece) is Pawn:
                    if self.__current_piece._y == 7:
                        self.__buttons = []
                        self.__pieces.remove(self.__current_piece)
                        # self.__pieces.append(Queen("black", self.__current_piece._x, self.__current_piece._y,
                        #                            self.black_queen_image))
                        self.__end_pawn = (self.__current_piece.get_x(), self.__current_piece.get_y())
                        self.__buttons = [Button(self.black_queen_image, board_x, board_y, "black","queen")
                            , Button(self.black_bishop_image, board_x, board_y - 1, "black","bishop"),
                                          Button(self.black_rook_image, board_x, board_y - 2, "black","rook"),
                                          Button(self.black_knight_image, board_x, board_y - 3, "black","knight")]

                        self.__turn = None


                    elif self.__current_piece._y == 0:
                        self.__buttons = []
                        self.__pieces.remove(self.__current_piece)
                        # self.__pieces.append(Queen("white", self.__current_piece._x, self.__current_piece._y,
                        #                              self.white_queen_image))
                        self.__end_pawn = (self.__current_piece.get_x(), self.__current_piece.get_y())
                        self.__buttons = [Button(self.white_queen_image, board_x, board_y, "white","queen")
                            , Button(self.white_bishop_image, board_x, board_y + 1, "white","bishop"),
                                          Button(self.white_rook_image, board_x, board_y + 2, "white","rook"),
                                          Button(self.white_knight_image, board_x, board_y + 3, "white","knight")]

                        self.__turn = None

                self.__current_piece = None
                # проверка на шах
                self.__is_check = False
                self.check()
                if self.__turn == "white":
                    self.__turn = "black"
                    if self.no_moves():
                        if not self.is_check():
                            print(f"Пат!")
                        else:
                            print("Победа белых")
                        self.__init__(self.__image)
                elif self.__turn == "black":
                    self.__turn = "white"
                    if self.no_moves():
                        if not self.is_check():
                            print(f"Пат!")
                        else:
                            print(f"Победа черных!")
                        self.__init__(self.__image)

    def check(self):
        """
        Ход еще не передали,смотрим короля противоположного игрока и фигуры текущего
        :return:
        """
        # ищем короля
        king_x = None
        king_y = None
        for piece in self.__pieces:
            if type(piece) is King and (
                    self.__turn == "white" and piece.is_black() or self.__turn == "black" and piece.is_white()):
                king_x = piece.get_x()
                king_y = piece.get_y()
                break

        for piece in self.__pieces:
            # проверяем фигуру цвета self.__turn
            # вычислить возможные ходы
            # если можем съесть короля то print шах
            if self.__turn == "white" and piece.is_white() or self.__turn == "black" and piece.is_black():
                piece.calculate_possible_moves(self)
                if piece.is_in_possible_kills(king_x, king_y):
                    # print('Шах!')

                    self.__is_check = True

    def no_moves(self):
        for piece in self.__pieces:
            if self.__turn == "black" and piece.is_black() or self.__turn == "white" and piece.is_white():
                piece.update(self)
                if not piece.no_moves():
                    return False

        return True

    def pseudo_check(self, phantom_piece=None):
        if phantom_piece is not None:
            self.__pieces.remove(phantom_piece)

        king_x = None
        king_y = None
        for piece in self.__pieces:
            if type(piece) is King and (
                    self.__turn == "white" and piece.is_white() or self.__turn == "black" and piece.is_black()):
                king_x = piece.get_x()
                king_y = piece.get_y()
                break

        for piece in self.__pieces:

            # проверяем фигуру цвета self.__turn
            # вычислить возможные ходы
            # если можем съесть короля то print шах
            if self.__turn == "white" and piece.is_black() or self.__turn == "black" and piece.is_white():
                # print(piece)
                piece.calculate_possible_moves(self)
                if piece.is_in_possible_kills(king_x, king_y):
                    if phantom_piece is not None:
                        self.__pieces.append(phantom_piece)
                    return True
        if phantom_piece is not None:
            self.__pieces.append(phantom_piece)
        return False

    def is_check(self):
        return self.__is_check

    def is_in_enemy_moves(self, enemy_color, x, y):
        for piece in self.__pieces:
            if piece.is_white() and enemy_color == "white" or piece.is_black() and enemy_color == "black":
                if piece.is_in_possible_moves(x, y):
                    return True

        else:
            return False

    def buttons(self, screen):
        if self.__turn is None:

            if self.__end_pawn[1] == 0:
                pg.draw.rect(screen, "white", (START_X + RECT_WIDTH * self.__end_pawn[0], START_Y,
                                               RECT_WIDTH, RECT_WIDTH * 4))

            else:
                pg.draw.rect(screen, "white",
                             (START_X + RECT_WIDTH * self.__end_pawn[0], START_Y + RECT_WIDTH * 4, RECT_WIDTH,
                              RECT_WIDTH * 4))
            for button in self.__buttons:
                button.draw(screen)

    def update(self, board_x, board_y):
        if self.__turn is not None:
            self.choose_piece(board_x, board_y)
            self.move(board_x, board_y)
        else:
            for button in self.__buttons:
                if board_x == button.board_x and board_y == button.board_y:
                    if button.piece == "queen":
                        if button.color == "white":
                            self.__pieces.append(Queen("white",self.__end_pawn[0],self.__end_pawn[1],self.white_queen_image))
                            self.__turn = "black"
                        else:
                            self.__pieces.append(
                                Queen("black", self.__end_pawn[0], self.__end_pawn[1], self.black_queen_image))
                            self.__turn = "white"
                    elif button.piece == "knight":
                        if button.color == "white":
                            self.__pieces.append(
                                Knight("white", self.__end_pawn[0], self.__end_pawn[1], self.white_knight_image))
                            self.__turn = "black"
                        else:
                            self.__pieces.append(
                                Knight("black", self.__end_pawn[0], self.__end_pawn[1], self.black_knight_image))
                            self.__turn = "white"
                    elif button.piece == "bishop":
                        if button.color == "white":
                            self.__pieces.append(
                                Bishop("white", self.__end_pawn[0], self.__end_pawn[1], self.white_bishop_image))
                            self.__turn = "black"
                        else:
                            self.__pieces.append(
                                Bishop("black", self.__end_pawn[0], self.__end_pawn[1], self.black_bishop_image))
                            self.__turn = "white"
                    elif button.piece == "rook":
                        if button.color == "white":
                            self.__pieces.append(
                                Rook("white", self.__end_pawn[0], self.__end_pawn[1], self.white_rook_image))
                            self.__turn = "black"
                        else:
                            self.__pieces.append(
                                Rook("black", self.__end_pawn[0], self.__end_pawn[1], self.black_rook_image))
                            self.__turn = "white"



