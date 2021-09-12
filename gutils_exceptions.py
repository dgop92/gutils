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
                typer.echo(typer.style(f"Error: {str(e)}", fg=typer.colors.BRIGHT_RED))
                raise typer.Exit(code=exit_code)

        return wrapper

    return decorator
