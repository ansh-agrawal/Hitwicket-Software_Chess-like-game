class Chess:
    def __init__(self):
        self.board = board.Board()
        self.turn = True
        self.white_ghost_piece = None
        self.black_ghost_piece = None

    def promotion(self, pos):
        pawn = None
        while pawn is None:
            if pos[0] == 0:
                choice = input("Promote to (Q, R, B, N): ")
                if choice == 'Q':
                    pawn = piece.Queen(True)
                elif choice == 'R':
                    pawn = piece.Rook(True)
                elif choice == 'B':
                    pawn = piece.Bishop(True)
                elif choice == 'N':
                    pawn = piece.Knight(True)
            else:
                pawn = piece.Pawn(True)
        self.board.board[pos[0]][pos[1]] = pawn

    def move(self, start, to):
        if self.board.board[start[0]][start[1]] is None:
            print("There is no piece to move at the start place")
            return

        target_piece = self.board.board[start[0]][start[1]]
        if self.turn != target_piece.color:
            print("That's not your piece to move")
            return

        end_piece = self.board.board[to[0]][to[1]]
        is_end_piece = end_piece is not None

        # Checks if a player's own piece is at the `to` coordinate
        if is_end_piece and target_piece.color == end_piece.color:
            print("There's a piece in the path.")
            return

        if target_piece.is_valid_move(self.board, start, to):
            # Special check for if the move is castling
            if target_piece.name == 'K' and abs(start[1] - to[1]) == 2:
                print("castled")

                if self.turn and self.black_ghost_piece:
                    self.board.board[self.black_ghost_piece[0]][self.black_ghost_piece[1]] = None
                elif not self.turn and self.white_ghost_piece:
                    self.board.board[self.white_ghost_piece[0]][self.white_ghost_piece[1]] = None
                self.turn = not self.turn
                return

            if self.board.board[to[0]][to[1]]:
                print(str(self.board.board[to[0]][to[1]]) + " taken.")
                # Special logic for ghost piece, deletes the actual pawn that is not in the `to`
                # coordinate from en passant
                if self.board.board[to[0]][to[1]].name == "GP":
                    if self.turn:
                        self.board.board[
                            self.black_ghost_piece[0] + 1
                        ][
                            self.black_ghost_piece[1]
                        ] = None
                        self.black_ghost_piece = None
                    else:
                        self.board.board[self.white_ghost_piece[0] - 1][self.black_ghost_piece[1]] = None
                        self.white_ghost_piece = None

            self.board.board[to[0]][to[1]] = target_piece
            self.board.board[start[0]][start[1]] = None
            print(str(target_piece) + " moved.")

            if self.turn and self.black_ghost_piece:
                self.board.board[self.black_ghost_piece[0]][self.black_ghost_piece[1]] = None
            elif not self.turn and self.white_ghost_piece:
                self.board.board[self.white_ghost_piece[0]][self.white_ghost_piece[1]] = None

            self.turn = not self.turn


def translate(s):
    """
    Translates the string into a move on the chessboard.
    """
    for move in s.split():
        start, to = move[:2], move[2:]
        start = (8 - int(start[1]), ord(start[0]) - ord('a'))
        to = (8 - int(to[1]), ord(to[0]) - ord('a'))

        if start is None or to is None:
            continue

        chess.move(start, to)

        # check for promotion pawns
        for i in range(8):
            if not chess.turn and chess.board.board[0][i] is not None and \
               chess.board.board[0][i].name == 'P':
                chess.promotion((0, i))
                break
            elif chess.turn and chess.board.board[7][i] is not None and \
                 chess.board.board[7][i].name == 'P':
                chess.promotion((7, i))
                break
