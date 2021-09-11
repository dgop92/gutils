import typer
from commands import all_commands

app = typer.Typer()

for sub_command in all_commands:
    app.add_typer(sub_command)

if __name__ == "__main__":
    app()