# start.py - 专用启动脚本
import os
import sys
import warnings

# 在导入任何 PyQt5 模块之前设置环境变量
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.*.debug=false'

# 抑制所有警告
warnings.filterwarnings("ignore")

# 现在导入主程序
from main import main

if __name__ == "__main__":
    main()