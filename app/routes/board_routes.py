from flask import Blueprint, abort, make_response, request, Response
from ..models.board import Board
from ..models.card import Card
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@boards_bp.post("")
def create_board():
    request_body = request.get_json()

    return create_model(Board, request_body)

@boards_bp.get("")
def get_all_boards():
    return get_models_with_filters(Board, request.args)

@boards_bp.get("/<board_id>")
def get_one_board(board_id):
    board = validate_model(Board, board_id)

    return board.to_dict()

# not required but standard CRUD route 
# can be used if we decide to add Delete board button
@boards_bp.delete("/<board_id>")
def delete_board(board_id):
    board = validate_model(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    return "", 204

# ! tests don't pass since Card doesn't have 'from_dict'
# ! re-test when Natasha pushes Card model
@boards_bp.post("/<board_id>/cards")
def create_card_to_board(board_id):
    board = validate_model(Board, board_id)
    
    request_body = request.get_json()
    request_body["board_id"] = board.board_id

    return create_model(Card, request_body)

# ! tests don't pass - AttributeError: 
# 'Card' object has no attribute 'to_dict'
# Re-test when Natasha pushes Card model
@boards_bp.get("/<board_id>/cards")
def get_cards_by_board(board_id):
    board = validate_model(Board, board_id)
    response = [card.to_dict() for card in board.cards]
    return response