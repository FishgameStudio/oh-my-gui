"""
Terminal demo: Show output, input & progress bar from ConsoleIO.
"""
from ohmygui import *
from time import sleep

def main():
    io = ConsoleIO()
    io.print("OhMyGUI Terminal Demo", fg=0xffcc00, bold=True)
    name = io.input("Enter your name: ", fg=0x00ccff)
    io.print(f"Hello, {name}", fg=0x00ff88)
    for i in range(0, 101, 5):
        io.make_progress("Downloading", 100, i)
        sleep(0.02)
    io.print("Done", fg=0x00ff00)

if __name__ == '__main__':
    main()
