# 教案数据结构定义
from dataclasses import dataclass
from typing import Optional


@dataclass
class LessonData:
    """一份教案的全部内容"""

    title: str
    level: str
    duration: str
    materials: str
    objectives: str
    key_points: str
    difficult_points: str
    process: str
    extension: str = ""
    notes: str = ""
