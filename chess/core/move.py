from typing import Optional
from core.piece import Piece, PieceType
from core.square import Square

class Move:
    """Represents a generic move."""
    from_: Square
    to_: Square
    moved_piece: Piece
    captured_piece: Optional[Piece]
    previous_en_passant_square: Optional[Square]
    def __init__(self, from_: Square, to_: Square, previous_en_passant_square: Optional[Square]):
        self.from_ = from_
        self.to_ = to_
        self.moved_piece = from_.piece
        self.captured_piece = to_.piece
        self.previous_en_passant_square = previous_en_passant_square

    def __repr__(self) -> str:
        return f"From {str(self.from_)} | To {str(self.to_)}\n"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.from_ == other.from_) and (self.to_ == other.to_)
        return NotImplemented
    
    def make(self) -> None:
        self.to_.piece = self.moved_piece
        self.from_.piece = None

    def undo(self) -> None:
        self.from_.piece = self.moved_piece
        self.to_.piece = self.captured_piece


class PromotionMove(Move):
    """Represents a move where a pawn promotes to a given PieceType."""
    promotion_piece: Optional[Piece]
    def __init__(self, from_: Square, to_: Square, previous_en_passant_square: Optional[Square], promotion_piece_type: PieceType):
        super().__init__(from_, to_, previous_en_passant_square)
        self.promotion_piece = Piece(promotion_piece_type, self.moved_piece.colour_type)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.from_ == other.from_) and (self.to_ == other.to_) and (self.promotion_piece == other.promotion_piece)
        return NotImplemented
    
    def make(self) -> None:
        self.to_.piece = self.promotion_piece
        self.from_.piece = None


class EnPassantMove(Move):
    """Represents a move where a pawn makes an en-passant capture."""
    capture_square: Square
    def __init__(self, from_: Square, to_: Square, previous_en_passant_square: Optional[Square], capture_square: Square):
        super().__init__(from_, to_, previous_en_passant_square)
        self.capture_square = capture_square
        self.captured_piece = capture_square.piece

    def __repr__(self) -> str:
        return f"From {str(self.from_)} | To {str(self.to_)} | Captured {str(self.capture_square)}\n"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.from_ == other.from_) and (self.to_ == other.to_) and (self.capture_square == other.capture_square)
        return NotImplemented

    def make(self) -> None:
        super().make()
        self.capture_square.piece = None
    
    def undo(self) -> None:
        self.from_.piece = self.moved_piece
        self.capture_square.piece = self.captured_piece
        self.to_.piece = None


# class PawnMove(Move):
#     capture_square: Square
#     promotion_piece: Optional[Piece]
#     def __init__(self, from_: Square, to_: Square, previous_en_passant_square: Optional[Square], capture_square: Square = None, promotion_piece: Piece = None):
#         super().__init__(from_, to_, previous_en_passant_square)
#         self.promotion_piece = promotion_piece
#         if is_en_passant(to_, previous_en_passant_square):
#             # print("en-passant!")
#             pass
#         if capture_square is None:
#             self.capture_square = to_
#             self.captured_piece = to_.piece
#         else:
#             # specify different capture square. Used for en-passant.
#             self.capture_square = capture_square
#             self.captured_piece = capture_square.piece

#     def __repr__(self) -> str:
#         move_str = f"From {str(self.from_)} To {str(self.to_)}\n"
#         if self.capture_square != self.to_:
#             move_str += f"Captured {self.captured_piece}"
#         return move_str

#     def __eq__(self, other: object) -> bool:
#         if isinstance(other, type(self)):
#             return (self.from_ == other.from_) and (self.to_ == other.to_) and (self.promotion_piece == other.promotion_piece)
#         return NotImplemented