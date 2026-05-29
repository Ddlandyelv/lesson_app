# 教案数据结构定义
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class ClassLevel(str, Enum):
    启蒙班 = "启蒙班"
    初级班 = "初级班"
    中级班 = "中级班"
    高级班 = "高级班"
    最高级班 = "最高级班"


class LessonDuration(str, Enum):
    _30分钟 = "30分钟"
    _45分钟 = "45分钟"
    _60分钟 = "60分钟"
    _90分钟 = "90分钟"
    _120分钟 = "120分钟"


@dataclass
class LessonData:
    """一份教案的全部内容"""

    title: str  # 教案标题
    level: str  # 适用班级
    duration: str  # 课时
    materials: str  # 绘画材料
    objectives: str  # 教学目标（三个维度）
    key_points: str  # 教学重点
    difficult_points: str  # 教学难点
    process: str  # 教学过程（分步骤）
    extension: str = ""  # 课后延伸
    notes: str = ""  # 注意事项

    def to_sections(self) -> dict:
        """转成有序分段，供模板渲染"""
        return {
            "title": self.title,
            "level": self.level,
            "duration": self.duration,
            "materials": self.materials,
            "objectives": self.objectives,
            "key_points": self.key_points,
            "difficult_points": self.difficult_points,
            "process": self.process,
            "extension": self.extension,
            "notes": self.notes,
        }
