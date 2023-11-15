class StatusCodeNotOKError(Exception):
    """Статус код отличается от 200."""

    pass


class NotFoundError(Exception):
    """Объект не найден."""

    pass
