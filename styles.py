# styles.py
"""
现代化样式定义 - 简洁实用风格
"""

# 主题配色
THEME_COLORS = {
    "primary": "#2563eb",
    "primary_dark": "#1d4ed8",
    "secondary": "#64748b",
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "dark": "#1e293b",
    "light": "#f8fafc",
    "border": "#e2e8f0"
}

# 主窗口样式
MAIN_WINDOW_STYLE = f"""
QMainWindow {{
    background-color: {THEME_COLORS['light']};
    font-family: 'Segoe UI', 'Microsoft YaHei', system-ui, sans-serif;
}}
"""

# 登录窗口样式
LOGIN_STYLE = f"""
QWidget {{
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                               stop: 0 {THEME_COLORS['primary']}, stop: 1 {THEME_COLORS['primary_dark']});
    color: white;
}}

QLabel#title {{
    font-size: 28px;
    font-weight: 600;
    color: white;
}}

QLabel {{
    font-size: 14px;
    color: rgba(255, 255, 255, 0.9);
}}

QLineEdit {{
    background: rgba(255, 255, 255, 0.15);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
    color: white;
    selection-background-color: {THEME_COLORS['primary']};
}}

QLineEdit:focus {{
    border: 2px solid rgba(255, 255, 255, 0.4);
    background: rgba(255, 255, 255, 0.2);
}}

QLineEdit::placeholder {{
    color: rgba(255, 255, 255, 0.6);
}}

QPushButton#primary_btn {{
    background: {THEME_COLORS['success']};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    font-weight: 600;
}}

QPushButton#primary_btn:hover {{
    background: #059669;
}}

QPushButton#secondary_btn {{
    background: transparent;
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 6px;
    padding: 10px;
    font-size: 13px;
}}

QPushButton#secondary_btn:hover {{
    background: rgba(255, 255, 255, 0.1);
}}
"""

# 侧边栏样式
SIDEBAR_STYLE = f"""
QWidget#sidebar {{
    background: white;
    border-right: 1px solid {THEME_COLORS['border']};
}}

QWidget#user_info {{
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                               stop: 0 {THEME_COLORS['primary']}, stop: 1 {THEME_COLORS['primary_dark']});
    border-bottom: 1px solid {THEME_COLORS['border']};
}}

QLabel#username {{
    color: white;
    font-size: 16px;
    font-weight: 600;
}}

QLabel#role {{
    color: rgba(255, 255, 255, 0.8);
    font-size: 13px;
}}

QListWidget#menu_list {{
    background: transparent;
    border: none;
    outline: none;
    font-size: 14px;
}}

QListWidget#menu_list::item {{
    color: {THEME_COLORS['dark']};
    background: transparent;
    padding: 12px 16px;
    border-bottom: 1px solid {THEME_COLORS['border']};
    border-radius: 0px;
}}

QListWidget#menu_list::item:selected {{
    background: {THEME_COLORS['primary']};
    color: white;
    border-left: 4px solid {THEME_COLORS['success']};
}}

QListWidget#menu_list::item:hover {{
    background: {THEME_COLORS['light']};
}}
"""

# 内容区域样式
CONTENT_STYLE = f"""
QWidget#content_area {{
    background: {THEME_COLORS['light']};
}}

/* 页面标题 */
QLabel#page_title {{
    color: {THEME_COLORS['dark']};
    font-size: 24px;
    font-weight: 600;
    margin: 0;
    padding: 0;
}}

QLabel#page_subtitle {{
    color: {THEME_COLORS['secondary']};
    font-size: 14px;
    margin: 0;
    padding: 0;
}}

/* 卡片样式 */
QWidget#card {{
    background: white;
    border: 1px solid {THEME_COLORS['border']};
    border-radius: 8px;
    padding: 0px;
}}

QLabel#card_title {{
    color: {THEME_COLORS['dark']};
    font-size: 16px;
    font-weight: 600;
    margin: 0;
    padding: 0;
}}

/* 按钮样式 */
QPushButton.primary-btn {{
    background: {THEME_COLORS['primary']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
}}

QPushButton.primary-btn:hover {{
    background: {THEME_COLORS['primary_dark']};
}}

QPushButton.secondary-btn {{
    background: white;
    color: {THEME_COLORS['dark']};
    border: 1px solid {THEME_COLORS['border']};
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
}}

QPushButton.secondary-btn:hover {{
    background: {THEME_COLORS['light']};
    border-color: {THEME_COLORS['primary']};
}}

/* 表格样式 */
QTableWidget {{
    background: white;
    border: 1px solid {THEME_COLORS['border']};
    border-radius: 8px;
    gridline-color: {THEME_COLORS['border']};
    outline: none;
}}

QTableWidget::item {{
    padding: 8px;
    border-bottom: 1px solid {THEME_COLORS['border']};
}}

QTableWidget::item:selected {{
    background: {THEME_COLORS['primary']};
    color: white;
}}

QHeaderView::section {{
    background: {THEME_COLORS['light']};
    color: {THEME_COLORS['dark']};
    padding: 12px 8px;
    border: none;
    border-bottom: 1px solid {THEME_COLORS['border']};
    font-weight: 600;
}}

/* 表单样式 */
QLineEdit.form-input {{
    background: white;
    border: 1px solid {THEME_COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    color: {THEME_COLORS['dark']};
}}

QLineEdit.form-input:focus {{
    border-color: {THEME_COLORS['primary']};
    outline: none;
}}

QTextEdit.form-input {{
    background: white;
    border: 1px solid {THEME_COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    color: {THEME_COLORS['dark']};
}}

QComboBox.form-input {{
    background: white;
    border: 1px solid {THEME_COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    color: {THEME_COLORS['dark']};
    min-height: 20px;
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid {THEME_COLORS['border']};
}}

QComboBox QAbstractItemView {{
    border: 1px solid {THEME_COLORS['border']};
    border-radius: 6px;
    background: white;
    selection-background-color: {THEME_COLORS['primary']};
}}
"""

# 状态标签样式
STATUS_STYLES = {
    'todo': f"color: {THEME_COLORS['secondary']}; background: #f1f5f9; padding: 4px 8px; border-radius: 4px;",
    'in_progress': f"color: {THEME_COLORS['warning']}; background: #fef3c7; padding: 4px 8px; border-radius: 4px;",
    'review': f"color: {THEME_COLORS['primary']}; background: #dbeafe; padding: 4px 8px; border-radius: 4px;",
    'done': f"color: {THEME_COLORS['success']}; background: #d1fae5; padding: 4px 8px; border-radius: 4px;",
    'planning': f"color: {THEME_COLORS['secondary']}; background: #f1f5f9; padding: 4px 8px; border-radius: 4px;",
    'active': f"color: {THEME_COLORS['primary']}; background: #dbeafe; padding: 4px 8px; border-radius: 4px;",
    'completed': f"color: {THEME_COLORS['success']}; background: #d1fae5; padding: 4px 8px; border-radius: 4px;",
    'cancelled': f"color: {THEME_COLORS['error']}; background: #fee2e2; padding: 4px 8px; border-radius: 4px;"
}