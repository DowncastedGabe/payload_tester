class Colors:

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def colorize(text: str, color: str) -> str:
        return f"{color}{text}{Colors.RESET}"

    @staticmethod
    def success(text: str) -> str:
        return Colors.colorize(text, Colors.GREEN)

    @staticmethod
    def error(text: str) -> str:
        return Colors.colorize(text, Colors.RED)
    
    @staticmethod
    def warning(text: str) -> str:
        return Colors.colorize(text, Colors.YELLOW)
    
    @staticmethod
    def info(text: str) -> str:
        return Colors.colorize(text, Colors.BLUE)
        