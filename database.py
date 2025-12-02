# database.py
import sqlite3
from datetime import datetime, timedelta


class Database:
    def __init__(self):
        self.conn = None
        self.connect()
        self.create_tables()
        self.create_default_admin()



        def validate_user_registration(self, username, email):
            """验证用户注册信息"""
            try:
                cursor = self.conn.cursor()

                # 检查用户名是否存在
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    return False, "用户名已存在"

                # 检查邮箱是否存在
                cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
                if cursor.fetchone():
                    return False, "邮箱已被注册"

                return True, "验证通过"
            except sqlite3.Error as e:
                print(f"验证用户注册信息失败: {e}")
                return False, "验证过程中发生错误"

        def update_user_password(self, user_id, new_password):
            """更新用户密码"""
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "UPDATE users SET password = ? WHERE id = ?",
                    (new_password, user_id)
                )
                self.conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"更新用户密码失败: {e}")
                return False

        def deactivate_user(self, user_id):
            """停用用户"""
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "UPDATE users SET is_active = 0 WHERE id = ?",
                    (user_id,)
                )
                self.conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"停用用户失败: {e}")
                return False

    def connect(self):
        """连接数据库"""
        try:
            self.conn = sqlite3.connect('work_system.db', check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            print("数据库连接成功")
        except sqlite3.Error as e:
            print(f"数据库连接失败: {e}")

    def create_tables(self):
        """创建数据表"""
        try:
            cursor = self.conn.cursor()

            # 用户表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT,
                    role TEXT NOT NULL DEFAULT 'user',
                    department TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')

            # 项目表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'planning',
                    priority TEXT DEFAULT 'medium',
                    start_date TEXT,
                    end_date TEXT,
                    budget REAL DEFAULT 0,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')

            # 任务表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'todo',
                    priority TEXT DEFAULT 'medium',
                    assignee_id INTEGER,
                    due_date TEXT,
                    estimated_hours REAL DEFAULT 0,
                    actual_hours REAL DEFAULT 0,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id),
                    FOREIGN KEY (assignee_id) REFERENCES users (id),
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')

            # 项目成员表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS project_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    user_id INTEGER,
                    role TEXT DEFAULT 'member',
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id),
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    UNIQUE(project_id, user_id)
                )
            ''')

            self.conn.commit()
            print("数据表创建成功")

        except sqlite3.Error as e:
            print(f"创建表失败: {e}")

    def create_default_admin(self):
        """创建默认管理员账户"""
        try:
            cursor = self.conn.cursor()
            # 检查是否已存在管理员
            cursor.execute("SELECT * FROM users WHERE username=?", ('admin',))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO users (username, password, role, department) VALUES (?, ?, ?, ?)",
                    ('admin', '123456', 'admin', '系统管理部')
                )
                self.conn.commit()
                print("默认管理员账户创建成功: admin/123456")
        except sqlite3.Error as e:
            print(f"创建默认管理员失败: {e}")

    # 用户管理方法
    def create_user(self, username, password, email=None, role='user', department=None):
        """创建新用户"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """INSERT INTO users (username, password, email, role, department) 
                VALUES (?, ?, ?, ?, ?)""",
                (username, password, email, role, department)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"创建用户失败: {e}")
            return None

    def get_user_by_credentials(self, username, password):
        """根据用户名密码获取用户"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username=? AND password=? AND is_active=1",
                (username, password)
            )
            user = cursor.fetchone()
            return user
        except sqlite3.Error as e:
            print(f"查询用户失败: {e}")
            return None

    def get_all_users(self):
        """获取所有用户"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE is_active=1 ORDER BY username")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"获取用户列表失败: {e}")
            return []

    def get_user_by_id(self, user_id):
        """根据ID获取用户"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id=? AND is_active=1", (user_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"获取用户失败: {e}")
            return None

    # 项目管理方法
    def create_project(self, name, description, created_by, **kwargs):
        """创建新项目"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """INSERT INTO projects 
                (name, description, created_by, status, priority, start_date, end_date, budget) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (name, description, created_by,
                 kwargs.get('status', 'planning'),
                 kwargs.get('priority', 'medium'),
                 kwargs.get('start_date'),
                 kwargs.get('end_date'),
                 kwargs.get('budget', 0))
            )
            project_id = cursor.lastrowid
            self.conn.commit()
            return project_id
        except sqlite3.Error as e:
            print(f"创建项目失败: {e}")
            return None

    def get_projects(self, user_id=None):
        """获取项目列表"""
        try:
            cursor = self.conn.cursor()
            if user_id:
                # 获取用户参与的项目
                cursor.execute("""
                    SELECT p.*, u.username as creator_name 
                    FROM projects p
                    LEFT JOIN users u ON p.created_by = u.id
                    WHERE p.id IN (
                        SELECT project_id FROM project_members WHERE user_id = ?
                    ) OR p.created_by = ?
                    ORDER BY p.created_at DESC
                """, (user_id, user_id))
            else:
                # 获取所有项目（管理员）
                cursor.execute("""
                    SELECT p.*, u.username as creator_name 
                    FROM projects p
                    LEFT JOIN users u ON p.created_by = u.id
                    ORDER BY p.created_at DESC
                """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"获取项目列表失败: {e}")
            return []

    def get_project_by_id(self, project_id):
        """根据ID获取项目"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT p.*, u.username as creator_name 
                FROM projects p
                LEFT JOIN users u ON p.created_by = u.id
                WHERE p.id = ?
            """, (project_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"获取项目失败: {e}")
            return None

    # 任务管理方法
    def create_task(self, project_id, title, created_by, **kwargs):
        """创建新任务"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """INSERT INTO tasks 
                (project_id, title, description, status, priority, assignee_id, due_date, estimated_hours, created_by) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (project_id, title,
                 kwargs.get('description'),
                 kwargs.get('status', 'todo'),
                 kwargs.get('priority', 'medium'),
                 kwargs.get('assignee_id'),
                 kwargs.get('due_date'),
                 kwargs.get('estimated_hours', 0),
                 created_by)
            )
            task_id = cursor.lastrowid
            self.conn.commit()
            return task_id
        except sqlite3.Error as e:
            print(f"创建任务失败: {e}")
            return None

    def get_tasks(self, user_id=None, project_id=None):
        """获取任务列表"""
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT t.*, p.name as project_name, u1.username as assignee_name, u2.username as creator_name
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                LEFT JOIN users u1 ON t.assignee_id = u1.id
                LEFT JOIN users u2 ON t.created_by = u2.id
                WHERE 1=1
            """
            params = []

            if user_id:
                query += " AND t.assignee_id = ?"
                params.append(user_id)

            if project_id:
                query += " AND t.project_id = ?"
                params.append(project_id)

            query += " ORDER BY t.created_at DESC"

            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"获取任务列表失败: {e}")
            return []

    def get_task_by_id(self, task_id):
        """根据ID获取任务"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT t.*, p.name as project_name, u1.username as assignee_name, u2.username as creator_name
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                LEFT JOIN users u1 ON t.assignee_id = u1.id
                LEFT JOIN users u2 ON t.created_by = u2.id
                WHERE t.id = ?
            """, (task_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"获取任务失败: {e}")
            return None

    def update_task_status(self, task_id, status):
        """更新任务状态"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (status, task_id)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"更新任务状态失败: {e}")
            return False

    # 项目成员管理方法
    def add_project_member(self, project_id, user_id, role='member'):
        """添加项目成员"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO project_members (project_id, user_id, role) VALUES (?, ?, ?)",
                (project_id, user_id, role)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"添加项目成员失败: {e}")
            return False

    def get_project_members(self, project_id):
        """获取项目成员"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT u.id, u.username, u.email, u.role, u.department, pm.role as project_role
                FROM project_members pm
                JOIN users u ON pm.user_id = u.id
                WHERE pm.project_id = ? AND u.is_active = 1
            """, (project_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"获取项目成员失败: {e}")
            return []

    # 统计方法
    def get_user_stats(self, user_id):
        """获取用户统计信息"""
        try:
            cursor = self.conn.cursor()

            # 总任务数
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE assignee_id=?", (user_id,))
            total_tasks = cursor.fetchone()[0]

            # 已完成任务
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE assignee_id=? AND status='done'", (user_id,))
            completed_tasks = cursor.fetchone()[0]

            # 进行中任务
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE assignee_id=? AND status='in_progress'", (user_id,))
            in_progress_tasks = cursor.fetchone()[0]

            # 逾期任务
            cursor.execute(
                "SELECT COUNT(*) FROM tasks WHERE assignee_id=? AND status != 'done' AND due_date < date('now')",
                (user_id,))
            overdue_tasks = cursor.fetchone()[0]

            return {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'in_progress_tasks': in_progress_tasks,
                'overdue_tasks': overdue_tasks
            }

        except sqlite3.Error as e:
            print(f"获取用户统计失败: {e}")
            return {}

    def get_project_stats(self, project_id):
        """获取项目统计信息"""
        try:
            cursor = self.conn.cursor()

            # 项目总任务数
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE project_id=?", (project_id,))
            total_tasks = cursor.fetchone()[0]

            # 项目已完成任务
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE project_id=? AND status='done'", (project_id,))
            completed_tasks = cursor.fetchone()[0]

            # 项目进度百分比
            progress = 0
            if total_tasks > 0:
                progress = int((completed_tasks / total_tasks) * 100)

            return {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'progress': progress
            }

        except sqlite3.Error as e:
            print(f"获取项目统计失败: {e}")
            return {}

    # 通用方法
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            print("数据库连接已关闭")

    def __del__(self):
        """析构函数，确保连接关闭"""
        self.close()


# 测试代码
if __name__ == "__main__":
    db = Database()

    # 测试用户创建
    user_id = db.create_user("test_user", "test_password", "test@example.com", "user", "测试部门")
    if user_id:
        print(f"测试用户创建成功，ID: {user_id}")

    # 测试用户查询
    user = db.get_user_by_credentials("test_user", "test_password")
    if user:
        print(f"用户查询成功: {user['username']}")

    # 测试项目创建
    project_id = db.create_project("测试项目", "这是一个测试项目", 1)
    if project_id:
        print(f"测试项目创建成功，ID: {project_id}")

    # 测试任务创建
    task_id = db.create_task(project_id, "测试任务", 1, description="这是一个测试任务")
    if task_id:
        print(f"测试任务创建成功，ID: {task_id}")

    # 测试统计信息
    stats = db.get_user_stats(1)
    print(f"用户统计: {stats}")

    db.close()