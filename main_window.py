# main_window.py - 修复版本
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QListWidget, QStackedWidget, QFrame,
                             QSizePolicy, QApplication, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 直接导入各个页面模块
try:
    from pages.dashboard import DashboardPage
    from pages.projects import ProjectsPage
    from pages.tasks import TasksPage
    from pages.users import UsersPage

    print("所有页面模块导入成功")
except ImportError as e:
    print(f"导入页面模块失败: {e}")


    # 如果导入失败，创建空页面作为回退
    class FallbackPage(QWidget):
        def __init__(self, title, db=None, user_info=None):
            super().__init__()
            layout = QVBoxLayout()
            label = QLabel(f"{title} - 模块加载失败")
            layout.addWidget(label)
            self.setLayout(layout)

        def load_data(self):
            """空方法，避免调用时出错"""
            pass


    DashboardPage = lambda db, user_info: FallbackPage("工作台", db, user_info)
    ProjectsPage = lambda db, user_info: FallbackPage("项目管理", db, user_info)
    TasksPage = lambda db, user_info: FallbackPage("任务管理", db, user_info)
    UsersPage = lambda db, user_info: FallbackPage("用户管理", db, user_info)


class MainWindow(QMainWindow):
    def __init__(self, user_info, db):
        super().__init__()
        self.user_info = user_info
        self.db = db
        self.pages = {}  # 初始化页面字典
        print(f"主窗口初始化，用户: {user_info['username']}")
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle(f'工作进度管理系统 - {self.user_info["username"]}')

        # 设置窗口初始大小和缩放策略
        screen = QApplication.primaryScreen().geometry()
        initial_width = min(1400, int(screen.width() * 0.8))
        initial_height = min(900, int(screen.height() * 0.8))
        self.setGeometry(100, 100, initial_width, initial_height)

        # 设置最小尺寸，确保界面不会太小
        self.setMinimumSize(1000, 650)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8fafc;
                font-family: 'Segoe UI', 'Microsoft YaHei', system-ui, sans-serif;
            }
        """)

        # 创建中央部件
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(main_layout)

        # 创建侧边栏
        self.create_sidebar(main_layout)

        # 创建内容区域
        self.create_content_area(main_layout)

        # 启用高DPI缩放
        self.setup_scaling()

        # 默认显示工作台页面
        self.menu_list.setCurrentRow(0)
        self.switch_page(0)

    def setup_scaling(self):
        """设置窗口缩放策略"""
        try:
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        except:
            pass

    def create_sidebar(self, main_layout):
        """创建侧边栏"""
        sidebar = QWidget()
        sidebar.setStyleSheet("""
            QWidget {
                background: white;
                border-right: 1px solid #e2e8f0;
            }
        """)
        sidebar.setFixedWidth(280)
        sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(0)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)

        # 用户信息区域
        user_info_widget = QWidget()
        user_info_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                           stop: 0 #2563eb, stop: 1 #1d4ed8);
                border-bottom: 1px solid #1a252f;
            }
        """)
        user_info_widget.setFixedHeight(120)

        user_layout = QVBoxLayout()
        user_layout.setContentsMargins(20, 15, 20, 15)
        user_layout.setSpacing(8)

        # 用户名
        username_label = QLabel(self.user_info['username'])
        username_label.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        username_label.setWordWrap(True)

        # 用户角色
        role_label = QLabel(
            f"{self.get_role_text(self.user_info['role'])} · {self.user_info.get('department', '未设置部门')}")
        role_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 13px;")
        role_label.setWordWrap(True)

        user_layout.addWidget(username_label)
        user_layout.addWidget(role_label)
        user_layout.addStretch()

        user_info_widget.setLayout(user_layout)
        sidebar_layout.addWidget(user_info_widget)

        # 菜单列表
        self.menu_list = QListWidget()
        self.menu_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                outline: none;
                font-size: 14px;
            }
            QListWidget::item {
                color: #1e293b;
                background: transparent;
                padding: 12px 16px;
                border-bottom: 1px solid #e2e8f0;
                border-radius: 0px;
            }
            QListWidget::item:selected {
                background: #2563eb;
                color: white;
                border-left: 4px solid #10b981;
            }
            QListWidget::item:hover {
                background: #f8fafc;
            }
        """)

        # 定义菜单项
        menus = [
            {'icon': '📊', 'text': '工作台概览', 'page': 'dashboard'},
            {'icon': '📁', 'text': '项目管理', 'page': 'projects'},
            {'icon': '✅', 'text': '任务管理', 'page': 'tasks'}
        ]

        # 如果是管理员，添加用户管理菜单
        if self.user_info['role'] == 'admin':
            menus.append({'icon': '👥', 'text': '用户管理', 'page': 'users'})

        # 添加菜单项
        for menu in menus:
            item_text = f"{menu['icon']}  {menu['text']}"
            self.menu_list.addItem(item_text)

        self.menu_list.currentRowChanged.connect(self.switch_page)
        sidebar_layout.addWidget(self.menu_list)

        # 底部信息
        bottom_widget = QWidget()
        bottom_widget.setStyleSheet("background: #f8fafc; padding: 12px; border-top: 1px solid #e2e8f0;")
        bottom_layout = QVBoxLayout()
        version_label = QLabel('v2.0.0')
        version_label.setStyleSheet("color: #64748b; font-size: 12px;")
        version_label.setAlignment(Qt.AlignCenter)
        bottom_layout.addWidget(version_label)
        bottom_widget.setLayout(bottom_layout)

        sidebar_layout.addWidget(bottom_widget)
        sidebar.setLayout(sidebar_layout)

        main_layout.addWidget(sidebar)

    def create_content_area(self, main_layout):
        """创建内容区域"""
        content_widget = QWidget()
        content_widget.setStyleSheet("background: #f8fafc;")
        content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 使用堆叠窗口管理不同页面
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 创建各个页面
        self.pages = {}

        try:
            self.pages['dashboard'] = DashboardPage(self.db, self.user_info)
            self.pages['projects'] = ProjectsPage(self.db, self.user_info)
            self.pages['tasks'] = TasksPage(self.db, self.user_info)

            # 如果是管理员，添加用户管理页面
            if self.user_info['role'] == 'admin':
                self.pages['users'] = UsersPage(self.db, self.user_info)

            print("所有页面创建成功")

        except Exception as e:
            print(f"创建页面失败: {e}")
            QMessageBox.warning(self, "错误", f"创建页面失败: {str(e)}")

        # 添加页面到堆叠窗口
        for page in self.pages.values():
            page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.stacked_widget.addWidget(page)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.stacked_widget)

        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)

    def get_role_text(self, role):
        """获取角色文本"""
        role_map = {
            'admin': '管理员',
            'user': '普通用户'
        }
        return role_map.get(role, role)

    def switch_page(self, index):
        """切换页面"""
        if index >= 0:
            page_keys = list(self.pages.keys())
            if index < len(page_keys):
                page_key = page_keys[index]
                self.stacked_widget.setCurrentWidget(self.pages[page_key])

                # 刷新页面数据
                try:
                    if hasattr(self.pages[page_key], 'load_data'):
                        self.pages[page_key].load_data()
                except Exception as e:
                    print(f"刷新页面数据失败: {e}")