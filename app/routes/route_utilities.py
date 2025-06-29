from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))
    # dynamically detect the primary key instead of hardcoding .id
    primary_key_column = list(cls.__mapper__.primary_key)[0]

    query = db.select(cls).where(primary_key_column == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))
    
    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as e:
        response = {"message": f"Invalid request: missing {e.args[0]}"}
        abort(make_response(response, 400))

    # Extra check for blank required fields
    for field in ["title", "owner"]:
        if field in model_data and isinstance(model_data[field], str):
            if model_data[field].strip() == "":
                response = {"message": f"Invalid request: '{field}' cannot be blank"}
                abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

    primary_key_column = list(cls.__mapper__.primary_key)[0]
    query = query.order_by(primary_key_column)

    models = db.session.scalars(query).all()
    models_response = [model.to_dict() for model in models]

    return models_response