"""
Full demo: 综合展示 core、widget、layout、terminal、oml 使用。
运行此脚本会展示一个窗口并在终端打印演示信息。
"""
import sys
from ohmygui import core, widget, layout, terminal, oml

def terminal_demo():
    io = terminal.ConsoleIO()
    io.print("Starting full demo", fg=0x00ff00, bold=True)
    name = io.input("Your name: ", fg=0x00ccff)
    io.print(f"Hello, {name}", fg=0xffff00)

def gui_demo():
    app = core.App()
    win = core.Window("Full Demo - OhMyGUI", (900, 700))

    # Basic widgets
    lbl = widget.Text("Full Demo: Widgets", "#000000", "#ddddff")
    lbl.set_size((300, 40))

    btn = widget.Button("Say Hi", "#ffffff", "#0077cc")
    btn.set_size((120, 40))

    entry = widget.InputEntry("Enter message", "Hello")
    entry.set_size((300, 30))

    log = widget.Text("Event Log", "#000000", "#ffffff")
    log.set_size((400, 120))

    def on_click(_=None):
        txt = entry.value
        log.set_text(f"Clicked: {txt}\n{log.text}")

    btn.on_click(on_click)

    # Layout: horizontal box example
    hbox = layout.HorizontalLayout()
    hbox.add_widget(lbl)
    hbox.add_widget(entry)
    hbox.add_widget(btn)

    win.set_layout(hbox)

    # Bind log as floating widget
    win.bind_widget(log, (20, 120))

    win.show()
    app.run()

def oml_demo():
    # Simple OML string demo (renders QML via internal converter)
    simple = '''
    @template TextLabel(txt, font_sz) {
        Text {
            text = txt;
            font_size = font_sz;
        }
    }
    TextLabel("OML Demo", 20);

    Window {
    
    }
    '''
    app = core.App()
    try:
        app.load_oml_string(simple)
    except Exception:
        # If QML not available in this env, skip
        pass

if __name__ == '__main__':
    # Terminal portion
    terminal_demo()
    # GUI portion
    try:
        gui_demo()
    except Exception as e:
        print(f"GUI demo failed: {e}")
    # OML demo (optional)
    try:
        oml_demo()
    except Exception:
        pass
