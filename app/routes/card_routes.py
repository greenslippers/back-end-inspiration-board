from flask import Blueprint, abort, make_response, request, Response
from ..models.card import Card
from ..models.board import Board
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@cards_bp.post("")
def create_card():
    request_body = request.get_json()

    board_id = request_body.get("board_id")
    if board_id:
        validate_model(Board, board_id)

    return create_model(Card, request_body)

@cards_bp.get("")
def get_all_cards():
    return get_models_with_filters(Card, request.args)

@cards_bp.get("/<card_id>")
def get_one_card(card_id):
    card = validate_model(Card, card_id)
    return card.to_dict()

@cards_bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return "", 204

@cards_bp.get("/board/<board_id>")
def get_cards_by_board(board_id):
    board = validate_model(Board, board_id)
    response = [card.to_dict() for card in board.cards]
    return response

@cards_bp.patch("/<card_id>/like")
def like_card(card_id):
    card = validate_model(Card, card_id)

    card.likes_count += 1
    db.session.commit()

    return card.to_dict(), 200