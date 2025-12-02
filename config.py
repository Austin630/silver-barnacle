# config.py
"""
系统配置文件
"""

# 应用配置
APP_CONFIG = {
    'name': '工作进度管理系统',
    'version': '2.0.0',
    'company': 'TechCorp Inc.',
    'description': '企业级工作进度管理与协作平台'
}

# 主题配置
THEME_CONFIG = {
    'primary_color': '#6366f1',
    'dark_mode': False,
    'animations_enabled': True,
    'shadow_effects': True
}

# 功能配置
FEATURE_CONFIG = {
    'enable_analytics': True,
    'enable_backup': True,
    'enable_sync': False,
    'max_file_size': 100  # MB
}

# 默认用户配置
DEFAULT_USER_CONFIG = {
    'language': 'zh_CN',
    'timezone': 'Asia/Shanghai',
    'date_format': 'YYYY-MM-DD',
    'notifications': True
}