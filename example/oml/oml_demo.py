"""
OML demo: Demonstrate how to convert an OML string to QML and load it through an Application (if QML is supported).
"""
from ohmygui.oml.parser import convert_oml_to_qml
from ohmygui.core.application import App

SAMPLE_OML = '''
$WIN_TITLE = "OML Demo";

Window {
    width: 640px; height: 360px;
    TextLabel("Hello OML", 24em);
}
'''

def main():
    qml = convert_oml_to_qml(SAMPLE_OML)
    print("--- GENERATED QML ---")
    print(qml)
    # Load if the environ support QML
    try:
        app = App()
        # load_qml_from expects a path; write to a temp qml file
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".qml", delete=False, encoding="utf-8") as f:
            f.write(qml)
            tmp = f.name
        app.load_qml_from(tmp)
    except Exception as e:
        print(f"Cannot load QML: {e}")

if __name__ == '__main__':
    main()
