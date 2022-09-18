import os
import importlib

from dotenv import load_dotenv


load_dotenv()

def load_connection():
    if db_host := os.environ.get("DB_HOST"):
        return db_host
    return input("[CONFIG] Enter DB Host: ")

def load_commands():
    return [
        filename.replace('.py', '')
        for filename in os.listdir("./commands")
        if filename.endswith(".py") and not filename.startswith("__")
    ] + ["cls", "clear", "exit", "commands", "help"]

def get_command(command):
    try:
        mod = importlib.import_module(f".{command}", "commands")
    except ImportError:
        return

    if "run" in dir(mod):
        return mod.run
    return


if __name__ == '__main__':

    host = load_connection()
    available_commands = load_commands()
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        input_command = input("> ").lower().strip()

        command_parts = input_command.split()

        if command_parts[0] not in available_commands:
            print("[ERROR] Command not found")
            continue

        if command_parts[0] == 'exit':
            break

        if command_parts[0] in ['clear', 'cls']:
            os.system('cls' if os.name == 'nt' else 'clear')
            continue

        if command_parts[0] in ["commands", "help"]:
            msg = "List of commands\n" + "\n".join(
                [f"- {command}" for command in available_commands]
            )
            print(msg)
            continue

        try:
            command = get_command(command_parts[0])
            command(host, *command_parts[1:])
        except Exception as e:
            print(f"[ERROR] {e}")
