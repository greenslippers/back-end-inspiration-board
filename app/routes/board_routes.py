from flask import Blueprint, abort, make_response, request
from ..models.board import Board
from ..db import db

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@boards_bp.post("")
def create_board():
    request_body = request.get_json()

    try:
        new_board = Board.from_dict(request_body)     
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_board)
    db.session.commit()

    return {"board": new_board.to_dict()}, 201

@boards_bp.get("")
def get_all_boards():
    query = db.select(Board)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Board.title.ilike(f"%{title_param}%"))
    
    owner_param = request.args.get("owner")
    if owner_param:
        # In case there are boards with similar titles, we can also filter by owner
        query = query.where(Board.owner.ilike(f"%{owner_param}%"))

    # Handle sorting
    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Board.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Board.title.desc())
    else:
        query = query.order_by(Board.board_id)
    
    # Execute query
    boards = db.session.scalars(query).all()  

    boards_response = []

    for board in boards:
        boards_response.append(board.to_dict())

    return boards_response, 200
    

