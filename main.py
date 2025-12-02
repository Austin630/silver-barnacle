# main.py
import sys
import os
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox

# 设置环境变量抑制警告
os.environ['QT_LOGGING_RULES'] = '*.debug=false'


def handle_exception(exc_type, exc_value, exc_traceback):
    """全局异常处理"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    print(f"未处理的异常: {exc_type.__name__}: {exc_value}")
    traceback.print_exception(exc_type, exc_value, exc_traceback)

    # 显示错误对话框
    try:
        error_msg = f"程序发生错误：\n{exc_type.__name__}: {exc_value}\n\n请检查控制台获取详细信息。"
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        QMessageBox.critical(None, "程序错误", error_msg)
    except:
        pass


# 设置全局异常处理
sys.excepthook = handle_exception


def main():
    try:
        # 创建应用
        app = QApplication(sys.argv)

        # 设置应用属性
        app.setApplicationName("工作进度管理系统")
        app.setApplicationVersion("2.0.0")

        # 初始化数据库
        from database import Database
        db = Database()

        # 显示登录窗口
        from login_window import LoginWindow
        login_window = LoginWindow(db)

        if login_window.exec_() == LoginWindow.Accepted:
            # 登录成功，显示主窗口
            user_info = login_window.user_info
            from main_window import MainWindow
            main_window = MainWindow(user_info, db)
            main_window.show()

            # 运行应用
            sys.exit(app.exec_())
        else:
            # 登录失败或取消，退出程序
            if hasattr(db, 'close'):
                db.close()
            sys.exit(0)

    except Exception as e:
        print(f"程序启动错误: {e}")
        traceback.print_exc()

        # 显示启动错误对话框
        try:
            error_msg = f"程序启动失败：\n{str(e)}\n\n请检查控制台获取详细信息。"
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "启动错误", error_msg)
            sys.exit(1)
        except:
            sys.exit(1)


if __name__ == "__main__":
    main()