from commands import all_commands
from core.gutils_core import GUtilTyper

app = GUtilTyper()

for sub_command in all_commands:
    app.registered_commands += sub_command.registered_commands

if __name__ == "__main__":
    app()
