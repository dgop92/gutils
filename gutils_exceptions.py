from functools import wraps

import typer

cli = typer.Typer()


class GUtilsException(Exception):
    pass


def catch_exception(which_exception, exit_code=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except which_exception as e:
                typer.echo(str(e))
                raise typer.Exit(code=exit_code)

        return wrapper

    return decorator
