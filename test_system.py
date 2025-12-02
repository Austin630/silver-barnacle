# test_system.py
import sys
import os

# 设置环境变量抑制警告
os.environ['QT_LOGGING_RULES'] = '*.debug=false'


def test_database():
    """测试数据库功能"""
    print("=== 测试数据库功能 ===")

    from database import Database
    db = Database()

    try:
        # 测试用户认证
        user = db.get_user_by_credentials("admin", "123456")
        if user:
            print(f"✓ 管理员登录测试成功: {user['username']}")
        else:
            print("✗ 管理员登录测试失败")

        # 测试用户列表
        users = db.get_all_users()
        print(f"✓ 获取用户列表成功: {len(users)} 个用户")

        # 测试项目列表
        projects = db.get_projects()
        print(f"✓ 获取项目列表成功: {len(projects)} 个项目")

        # 测试任务列表
        tasks = db.get_tasks()
        print(f"✓ 获取任务列表成功: {len(tasks)} 个任务")

        # 测试统计信息
        stats = db.get_user_stats(1)
        print(f"✓ 获取用户统计成功: {stats}")

        print("✓ 所有数据库测试通过")

    except Exception as e:
        print(f"✗ 数据库测试失败: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if hasattr(db, 'close'):
            db.close()


def test_login():
    """测试登录功能"""
    print("\n=== 测试登录功能 ===")

    from database import Database
    from login_window import LoginWindow
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    db = Database()

    try:
        # 创建登录窗口但不显示
        login_window = LoginWindow(db)

        # 测试有效登录
        login_window.login_username.setText("admin")
        login_window.login_password.setText("123456")
        login_window.handle_login()

        if hasattr(login_window, 'user_info') and login_window.user_info:
            print(f"✓ 登录测试成功: {login_window.user_info['username']}")
        else:
            print("✗ 登录测试失败")

    except Exception as e:
        print(f"✗ 登录测试失败: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if hasattr(db, 'close'):
            db.close()


if __name__ == "__main__":
    print("开始系统测试...")
    test_database()
    test_login()
    print("\n=== 测试完成 ===")
    input("按回车键退出...")