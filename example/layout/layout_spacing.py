import ohmygui.core as core
import ohmygui.widget as widget
import ohmygui.layout as layout

app = core.App()
win = core.Window("Layout Stretch", (360, 340))
win.set_bg("#ffffff")

lay = layout.VerticalLayout()
lay.add_margin(16)
lay.set_common_spacing(10)

title = widget.Text("Vertical Layout Demo", "#ffffff", "#1f5fa6")
title.set_size((320, 50))

info = widget.Text("This layout uses spacing, margin, and stretch to arrange widgets.", "#000000", "#f0f0f0")
info.set_size((320, 80))

close_btn = widget.Button("Close Window", "#ffffff", "#1f5fa6")
close_btn.set_size((320, 50))
close_btn.on_click(lambda _: win.close())

lay.add_widget(title)
lay.add_widget(info)
lay.add_stretch()
lay.add_widget(close_btn)

win.set_layout(lay)
win.show()
app.run()
