def get_material_style():
    """
    Creates a Material Design-inspired stylesheet for the application.
    The color scheme uses a modern palette with primary and accent colors.
    """
    return """
    /* Main Window Styling */
    QMainWindow {
        background-color: #f5f5f5;
    }

    /* Button Styling */
    QPushButton {
        background-color: #6200ee;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
        min-height: 36px;
    }

    QPushButton:hover {
        background-color: #7722ff;
    }

    QPushButton:pressed {
        background-color: #3700b3;
    }

    QPushButton:disabled {
        background-color: #e0e0e0;
        color: #9e9e9e;
    }

    /* Color Button Special Styling */
    QPushButton#colorButton {
        min-width: 80px;
        min-height: 80px;
        border-radius: 8px;
        margin: 4px;
        border: 1px solid rgba(0, 0, 0, 0.12);
    }

    QPushButton#colorButton:hover {
        border: 2px solid #6200ee;
    }

    /* ComboBox Styling */
    QComboBox {
        background-color: white;
        border: 2px solid #e0e0e0;
        border-radius: 4px;
        padding: 6px;
        min-height: 24px;
    }

    QComboBox:hover {
        border-color: #6200ee;
    }

    QComboBox::drop-down {
        border: none;
    }

    QComboBox::down-arrow {
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 6px solid #6200ee;
        margin-right: 8px;
    }

    /* SpinBox Styling */
    QSpinBox {
        background-color: white;
        border: 2px solid #e0e0e0;
        border-radius: 4px;
        padding: 6px;
        min-height: 24px;
    }

    QSpinBox:hover {
        border-color: #6200ee;
    }

    /* Label Styling */
    QLabel {
        color: #202020;
        font-size: 14px;
    }

    /* Card-like Widget Styling */
    QWidget#card {
        background-color: white;
        border-radius: 8px;
        padding: 16px;
    }

    /* Message Box Styling */
    QMessageBox {
        background-color: white;
    }

    QMessageBox QPushButton {
        min-width: 64px;
    }
    """
