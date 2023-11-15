from ninja import Schema

error_codes = frozenset({404, 503})


class ErrorSchema(Schema):
    message: str
