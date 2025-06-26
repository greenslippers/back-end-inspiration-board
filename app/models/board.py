from sqlalchemy.orm import Mapped, mapped_column,relationship
from ..models.card import Card
from ..db import db

class Board(db.Model):
    board_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    owner: Mapped[str]

    cards: Mapped[list["Card"]] = relationship(back_populates="board", cascade="all, delete")

    # converts a Board instance into a dict 
    # for generating JSON response (GET)
    def to_dict(self):
        board_as_dict = {}
        board_as_dict["id"] = self.board_id
        board_as_dict["title"] = self.title
        board_as_dict["owner"] = self.owner
        
        return board_as_dict

    # creates a new Board model instance from a dictionary (for POST)
    @classmethod
    def from_dict(cls, board_data):
        new_board = Board(title=board_data["title"],
                          owner=board_data["owner"])

        return new_board