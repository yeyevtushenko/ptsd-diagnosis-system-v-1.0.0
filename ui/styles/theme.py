PRIMARY_COLOR = "#5A7D6A"
PRIMARY_DARK = "#3D5749"
PRIMARY_HOVER = "#496757"

BACKGROUND = "#F6F8F4"
SURFACE = "#FCFCFA"

TEXT_DARK = "#1F3328"
TEXT_MUTED = "#4A5C50"

BORDER = "#C8D2C5"

def button_style() -> str:
    return f"""
        QPushButton {{
            background-color: {PRIMARY_COLOR};
            color: white;
            border-radius: 10px;
            padding: 12px 18px;
            font-size: 14px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background-color: {PRIMARY_COLOR};
        }}
        QPushButton:pressed {{
            background-color: {PRIMARY_COLOR};
        }}
    """

def drop_area_style() -> str:
    return f"""
        QLabel {{
            border: 2px dashed {PRIMARY_DARK};
            border-radius: 12px;
            padding: 30px;
            font-size: 16px;
            color: {TEXT_DARK};
            background-color: {BACKGROUND};
        }}
    """

def title_style() -> str:
    return f"""
        QLabel {{
            font-size: 22px;
            font-weight: bold;
            color: {TEXT_DARK};
            margin: 10px;
        }}    
    """

def text_box_style() -> str:
    return f"""
        QTextEdit {{
            background-color: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 10px;
            padding: 12px;
            font-size: 14px;
            color: #1F1F1F;
        }}    
    """
