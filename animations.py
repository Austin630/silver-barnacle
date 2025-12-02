# animations.py - 简化版
"""
简化版动画效果工具类
"""

from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QWidget


class FadeAnimation(QPropertyAnimation):
    """淡入淡出动画"""

    def __init__(self, widget, duration=300):
        super().__init__(widget, b"windowOpacity")
        self.widget = widget
        self.setDuration(duration)
        self.setEasingCurve(QEasingCurve.OutCubic)

    def fade_in(self):
        """淡入"""
        self.setStartValue(0)
        self.setEndValue(1)
        self.start()

    def fade_out(self):
        """淡出"""
        self.setStartValue(1)
        self.setEndValue(0)
        self.start()