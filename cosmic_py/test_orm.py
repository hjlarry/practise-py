import models


def test_orderline_mapper_can_load_lines(session):  # (1)
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty) VALUES "
        '("order1", "RED-CHAIR", 12),'
        '("order1", "RED-TABLE", 13),'
        '("order2", "BLUE-LIPSTICK", 14)'
    )
    expected = [
        models.OrderLine("order1", "RED-CHAIR", 12),
        models.OrderLine("order1", "RED-TABLE", 13),
        models.OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]
    assert session.query(models.OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    new_line = models.OrderLine("order1", "DECORATIVE-WIDGET", 12)
    session.add(new_line)
    session.commit()

    rows = list(session.execute('SELECT orderid, sku, qty FROM "order_lines"'))
    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]
