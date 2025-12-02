# login_window.py - 修复版本
import sys
import re
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QCheckBox,
                             QTabWidget, QWidget, QFormLayout, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class RegisterDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('用户注册')
        self.setMinimumSize(400, 500)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 设置窗口样式
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                           stop: 0 #2563eb, stop: 1 #1d4ed8);
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # 标题
        title_label = QLabel('用户注册')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: 600;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title_label)

        # 副标题
        subtitle_label = QLabel('创建您的工作账户')
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                margin-bottom: 30px;
            }
        """)
        layout.addWidget(subtitle_label)

        # 表单容器
        form_container = QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(15)

        # 创建表单字段 - 直接使用 QLineEdit
        self.username_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.confirm_password_edit = QLineEdit()
        self.department_edit = QLineEdit()

        # 设置输入框属性
        self.setup_input_field(self.username_edit, "用户名", "请输入用户名")
        self.setup_input_field(self.email_edit, "邮箱", "请输入邮箱地址")
        self.setup_input_field(self.password_edit, "密码", "请输入密码", True)
        self.setup_input_field(self.confirm_password_edit, "确认密码", "请再次输入密码", True)
        self.setup_input_field(self.department_edit, "部门", "请输入所在部门")

        # 添加到布局
        form_layout.addWidget(self.create_input_widget("用户名", self.username_edit))
        form_layout.addWidget(self.create_input_widget("邮箱", self.email_edit))
        form_layout.addWidget(self.create_input_widget("密码", self.password_edit))
        form_layout.addWidget(self.create_input_widget("确认密码", self.confirm_password_edit))
        form_layout.addWidget(self.create_input_widget("部门", self.department_edit))

        # 注册按钮
        register_btn = QPushButton('注册账户')
        register_btn.setStyleSheet("""
            QPushButton {
                background: #10b981;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: 600;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: #059669;
            }
            QPushButton:disabled {
                background: #9ca3af;
            }
        """)
        register_btn.clicked.connect(self.register)
        form_layout.addWidget(register_btn)

        # 返回登录
        back_layout = QHBoxLayout()
        back_layout.addStretch()
        back_label = QLabel('已有账户？')
        back_label.setStyleSheet("color: #6b7280; font-size: 13px;")
        back_btn = QPushButton('立即登录')
        back_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #2563eb;
                border: none;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                color: #1d4ed8;
                text-decoration: underline;
            }
        """)
        back_btn.clicked.connect(self.accept)

        back_layout.addWidget(back_label)
        back_layout.addWidget(back_btn)
        back_layout.addStretch()
        form_layout.addLayout(back_layout)

        layout.addWidget(form_container)
        self.setLayout(layout)

    def setup_input_field(self, edit, label_text, placeholder, is_password=False):
        """设置输入字段属性"""
        edit.setPlaceholderText(placeholder)
        if is_password:
            edit.setEchoMode(QLineEdit.Password)

        edit.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                padding: 10px 12px;
                font-size: 14px;
                color: #1f2937;
            }
            QLineEdit:focus {
                border-color: #2563eb;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
        """)

    def create_input_widget(self, label_text, input_field):
        """创建带标签的输入组件"""
        container = QWidget()
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        container.setStyleSheet("QWidget { background: transparent; }")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # 标签
        label = QLabel(label_text)
        label.setStyleSheet("color: #374151; font-size: 13px; font-weight: 500;")
        layout.addWidget(label)
        layout.addWidget(input_field)

        return container

    def validate_input(self):
        """验证输入数据"""
        username = self.username_edit.text().strip()
        email = self.email_edit.text().strip()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()
        department = self.department_edit.text().strip()

        # 检查必填字段
        if not username:
            self.show_error("请输入用户名")
            return False

        if not email:
            self.show_error("请输入邮箱地址")
            return False

        if not password:
            self.show_error("请输入密码")
            return False

        if not confirm_password:
            self.show_error("请确认密码")
            return False

        # 验证用户名格式
        if len(username) < 3:
            self.show_error("用户名至少需要3个字符")
            return False

        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            self.show_error("用户名只能包含字母、数字和下划线")
            return False

        # 验证邮箱格式
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.show_error("请输入有效的邮箱地址")
            return False

        # 验证密码强度
        if len(password) < 6:
            self.show_error("密码至少需要6个字符")
            return False

        # 验证密码匹配
        if password != confirm_password:
            self.show_error("两次输入的密码不一致")
            return False

        return {
            'username': username,
            'email': email,
            'password': password,
            'department': department
        }

    def show_error(self, message):
        """显示错误信息"""
        QMessageBox.warning(self, '输入错误', message)

    def show_success(self, message):
        """显示成功信息"""
        QMessageBox.information(self, '注册成功', message)

    def register(self):
        """处理用户注册"""
        data = self.validate_input()
        if not data:
            return

        try:
            # 检查用户名是否已存在
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (data['username'],))
            if cursor.fetchone():
                self.show_error("用户名已存在，请选择其他用户名")
                return

            # 检查邮箱是否已存在
            cursor.execute("SELECT id FROM users WHERE email = ?", (data['email'],))
            if cursor.fetchone():
                self.show_error("邮箱地址已被注册")
                return

            # 创建用户
            user_id = self.db.create_user(
                username=data['username'],
                password=data['password'],
                email=data['email'],
                role='user',
                department=data['department']
            )

            if user_id:
                self.show_success(f"注册成功！欢迎 {data['username']}")
                self.accept()
            else:
                self.show_error("注册失败，请稍后重试")

        except Exception as e:
            print(f"注册错误: {e}")
            self.show_error("注册过程中发生错误，请稍后重试")


class LoginWindow(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.user_info = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('工作进度管理系统 - 登录')
        self.setMinimumSize(450, 600)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                           stop: 0 #2563eb, stop: 1 #1d4ed8);
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # 标题
        title_label = QLabel('工作进度管理系统')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: 600;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title_label)

        # 副标题
        subtitle_label = QLabel('高效协作，精准管理')
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                margin-bottom: 40px;
            }
        """)
        layout.addWidget(subtitle_label)

        # 登录表单容器
        form_container = QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 12px;
                padding: 30px;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)

        # 登录标题
        login_title = QLabel('用户登录')
        login_title.setAlignment(Qt.AlignCenter)
        login_title.setStyleSheet("""
            QLabel {
                color: #1f2937;
                font-size: 20px;
                font-weight: 600;
                margin-bottom: 10px;
            }
        """)
        form_layout.addWidget(login_title)

        # 输入字段 - 直接使用 QLineEdit
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()

        self.setup_input_field(self.username_edit, "用户名", "请输入用户名")
        self.setup_input_field(self.password_edit, "密码", "请输入密码", True)

        form_layout.addWidget(self.create_input_widget("用户名", self.username_edit))
        form_layout.addWidget(self.create_input_widget("密码", self.password_edit))

        # 记住我选项
        remember_layout = QHBoxLayout()
        self.remember_check = QCheckBox('记住登录状态')
        self.remember_check.setStyleSheet("""
            QCheckBox {
                color: #6b7280;
                font-size: 13px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #d1d5db;
                border-radius: 3px;
                background: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #2563eb;
                border-radius: 3px;
                background: #2563eb;
            }
        """)
        remember_layout.addWidget(self.remember_check)
        remember_layout.addStretch()
        form_layout.addLayout(remember_layout)

        # 登录按钮
        login_btn = QPushButton('登录系统')
        login_btn.setStyleSheet("""
            QPushButton {
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: 600;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: #1d4ed8;
            }
            QPushButton:disabled {
                background: #9ca3af;
            }
        """)
        login_btn.clicked.connect(self.login)
        form_layout.addWidget(login_btn)

        # 注册链接
        register_layout = QHBoxLayout()
        register_layout.addStretch()
        register_label = QLabel('没有账户？')
        register_label.setStyleSheet("color: #6b7280; font-size: 13px;")
        register_btn = QPushButton('立即注册')
        register_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #2563eb;
                border: none;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                color: #1d4ed8;
                text-decoration: underline;
            }
        """)
        register_btn.clicked.connect(self.show_register)

        register_layout.addWidget(register_label)
        register_layout.addWidget(register_btn)
        register_layout.addStretch()
        form_layout.addLayout(register_layout)

        layout.addWidget(form_container)
        self.setLayout(layout)

        # 设置回车键登录
        self.username_edit.returnPressed.connect(self.login)
        self.password_edit.returnPressed.connect(self.login)

    def setup_input_field(self, edit, label_text, placeholder, is_password=False):
        """设置输入字段属性"""
        edit.setPlaceholderText(placeholder)
        if is_password:
            edit.setEchoMode(QLineEdit.Password)

        edit.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                padding: 10px 12px;
                font-size: 14px;
                color: #1f2937;
            }
            QLineEdit:focus {
                border-color: #2563eb;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
        """)

    def create_input_widget(self, label_text, input_field):
        """创建带标签的输入组件"""
        container = QWidget()
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        container.setStyleSheet("QWidget { background: transparent; }")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # 标签
        label = QLabel(label_text)
        label.setStyleSheet("color: #374151; font-size: 13px; font-weight: 500;")
        layout.addWidget(label)
        layout.addWidget(input_field)

        return container

    def show_register(self):
        """显示注册窗口"""
        register_dialog = RegisterDialog(self.db, self)
        if register_dialog.exec_() == QDialog.Accepted:
            # 注册成功后可以自动填充用户名
            pass

    def login(self):
        """处理用户登录"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()

        if not username:
            QMessageBox.warning(self, '输入错误', '请输入用户名')
            self.username_edit.setFocus()
            return

        if not password:
            QMessageBox.warning(self, '输入错误', '请输入密码')
            self.password_edit.setFocus()
            return

        # 验证用户凭据
        user = self.db.get_user_by_credentials(username, password)
        if user:
            self.user_info = {
                'id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'department': user['department'],
                'email': user['email']
            }
            self.accept()
        else:
            QMessageBox.warning(self, '登录失败', '用户名或密码错误')
            self.password_edit.clear()
            self.password_edit.setFocus()