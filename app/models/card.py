from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Card(db.Model):
    __tablename__ = "card"

    card_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(nullable=False)
    likes_count: Mapped[int] = mapped_column(default=0)
    card_color: Mapped[str]
    board_id: Mapped[int] = mapped_column(db.ForeignKey("board.board_id"))
    board: Mapped["Board"] = relationship("Board", back_populates="cards")

    def to_dict(self):
        return {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id,
            "card_color": self.card_color
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            message=data["message"],
            likes_count=data.get("likes_count", 0),
            board_id=data["board_id"],
            card_color=data["card_color"]
        )