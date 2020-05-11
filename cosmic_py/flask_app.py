from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import orm
import models
import config
import repository

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    batches = repository.SqlAlchemyRepository(session).list()
    line = models.OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"]
    )

    if not is_valid_sku(line.sku, batches):
        return jsonify({"message": f"Invalid sku {line.sku}"}), 400
    try:
        batchref = models.allocate(line, batches)
    except models.OutOfStock as e:
        return jsonify({"message": str(e)}), 400
    session.commit()
    return jsonify({"batchref": batchref}), 201
