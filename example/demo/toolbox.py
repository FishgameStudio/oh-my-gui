"""
Toolbox demo: Task runner with timer & printing progress.
"""
from time import sleep
from ohmygui.terminal import conio

def run_task(total=20):
    io = conio.ConsoleIO()
    io.print("Toolbox: Running task...", fg=0x00cc66)
    for i in range(total+1):
        io.make_progress("Processing", total, i)
        sleep(0.05)
    io.print("Task completed!", fg=0x00cc66)

if __name__ == '__main__':
    run_task(50)
