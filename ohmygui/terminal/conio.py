# Console i/o module.

from typing import Callable, Self

class ConsoleIO:
    def __init__(self, fg: int = 0xffffff, bg: int = 0x000000): 
        self.fg = fg
        self.bg = bg

    @staticmethod
    def hex2ansi(rgb: int, *, bg: bool = False, highlight: bool = False, bold: bool = False, italic: bool = False, underline: bool = False) -> str:
        """Returns the ANSI escape text from the hex digit `rgb`."""
        r = (rgb >> 16) & 0xFF + 60 if highlight else 0
        g = (rgb >> 8) & 0xFF + 60 if highlight else 0
        b = rgb & 0xFF + 60 if highlight else 0
        code = 48 if bg else 38
        styles = []
        if bold:
            styles.append("1")
        if italic:
            styles.append("3")
        if underline:
            styles.append("4")
        style_str = ";".join(styles) + ";" if styles else ""

        return f"\033[{style_str}{code};2;{r};{g};{b}m"
     
    RESET = "\033[0m"

    def print(self, text: str, *, fg: int | None = None, bg: int | None = None, highlight: bool = False, bold: bool = False, italic: bool = False, underline: bool = False, end: str = "\n") -> Self:
        """Output text."""
        self.fg = fg if fg is not None else self.fg
        self.bg = bg if bg is not None else self.bg
        fg_ansi = self.hex2ansi(fg if isinstance(fg, int) else self.fg, highlight=highlight, bold=bold, italic=italic, underline=underline)
        bg_ansi = self.hex2ansi(bg if isinstance(bg, int) else self.bg, bg=True, highlight=highlight, bold=bold, italic=italic, underline=underline)

        print(f"{fg_ansi}{bg_ansi}{text}", end=f"{end}{self.RESET}")
        return self
    def input(self, prompt: str, *, fg: int | None = None, bg: int | None = None, highlight: bool = False, bold: bool = False, italic: bool = False, underline: bool = False, callback: Callable[[str], None] | None = None) -> str:
        """Input."""
        # print the prompt
        self.print(prompt, fg=fg, bg=bg, highlight=highlight, bold=bold, italic=italic, underline=underline, end="")
        # make input.
        res: str
        try:
            res = input("")
        except EOFError or KeyboardInterrupt:
            res = ""
        # Call callback
        if callback is not None: 
            callback(res)
        return res
    def make_progress(self, prompt: str, total: int, curr: int) -> Self:
        percent = curr / total
        CHAR_DONE  = "█" # Block
        CHAR_REST  = "░" # White block
        WIDTH = 30
        bar = int(percent * WIDTH)
        done = CHAR_DONE * bar
        rest = CHAR_REST * (WIDTH - bar)
        print(f"{prompt} [{done}{rest}]", end=f"{percent * 100:.2f}%       {"\n" if percent >= 1 else "\r"}")
        return self

# Test
if __name__ == '__main__':
    from time import sleep
    io = ConsoleIO()
    t = 100
    c = 0
    while c <= t:
        io.make_progress("prompt:", t, c)
        c += 1
        sleep(0.1)
    input("Done, press Enter to exit...")
        




    
        