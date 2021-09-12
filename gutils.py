import typer

from commands import all_commands

app = typer.Typer()

for sub_command in all_commands:
    app.registered_commands += sub_command.registered_commands

if __name__ == "__main__":
    app()
