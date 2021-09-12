import sys
import typing
from typing import Callable

import typer

ExceptionType = "typing.Type[Exception]"
ErrorHandlingCallback = Callable[[Exception], int]


class GUtilsException(Exception):
    pass


def gutil_callback(e):
    error_message = str(e)
    typer.echo(typer.style(f"Error: {error_message}", fg=typer.colors.BRIGHT_RED))
    return 1


class GUtilTyper(typer.Typer):
    error_handlers: typing.Dict[ExceptionType, ErrorHandlingCallback] = {
        GUtilsException: gutil_callback
    }

    def error_handler(self, exc: ExceptionType):
        def decorator(
            f: ErrorHandlingCallback,
        ):
            self.error_handlers[exc] = f
            return f

        return decorator

    def __call__(self, *args, **kwargs):
        try:
            super(GUtilTyper, self).__call__(*args, **kwargs)
        except Exception as e:
            try:
                callback = self.error_handlers[type(e)]
                exit_code = callback(e)
                raise typer.Exit(code=exit_code)
            except typer.Exit as e:
                sys.exit(e.exit_code)
            except KeyError:
                raise
