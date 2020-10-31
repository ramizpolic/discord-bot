from rich.console import Console
console = Console()

class msg:
    """Handles cli logging controller"""
    @staticmethod
    def title(text):
        console.print(f'\n🎯 [underline bold white on bright_black]{text}\n')

    @staticmethod
    def subtitle(text):
        console.print(f'   [bold white]{text}')

    @staticmethod
    def success(text):
        console.print(f'✔️ [bold white]{text}')

    @staticmethod
    def error(text):
        console.print(f'❌ [white]Error: [bold]{text}')

    @staticmethod
    def warn(text):
        console.print(f'⚠️ [bright_black italic]{text}')

    @staticmethod
    def print(text):
        console.print(text)

    @staticmethod
    def listitem(text):
        console.print(f'   [orange3 bold]>[/] {text}')

    @staticmethod
    def item(name, value):
        console.print(f'   [bold]{name}: [/]{value}')
