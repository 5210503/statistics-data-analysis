# -*- coding: utf-8 -*-
"""
练习 01：描述性统计入门
========================
使用 data/students_scores.csv 中的学生成绩数据，
计算各科的均值、中位数、最大/最小值和标准差。

只用了 Python 标准库（csv + statistics），无需安装任何第三方包。
后续学到 pandas 后，可以回来用 3 行代码重写本练习！
"""

import csv
import statistics as stats

# 数据文件路径（相对于本脚本所在的 exercises/ 目录）
DATA_PATH = "../data/students_scores.csv"


def load_scores(path):
    """读取 CSV，返回 {科目: [分数列表]} 的字典"""
    subjects = {"math": [], "chinese": [], "english": []}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for subject in subjects:
                subjects[subject].append(int(row[subject]))
    return subjects


def describe(name, values):
    """计算并打印一组数据的描述性统计量"""
    print(f"—— {name} ——")
    print(f"  人数  : {len(values)}")
    print(f"  均值  : {stats.mean(values):.2f}")
    print(f"  中位数: {stats.median(values):.2f}")
    print(f"  标准差: {stats.stdev(values):.2f}")
    print(f"  最高分: {max(values)}")
    print(f"  最低分: {min(values)}")
    print()


def main():
    subjects = load_scores(DATA_PATH)

    name_map = {"math": "数学", "chinese": "语文", "english": "英语"}
    for subject, values in subjects.items():
        describe(name_map[subject], values)

    # 思考题验证：给数学成绩统一加 10 分，标准差会变吗？
    math_boosted = [x + 10 for x in subjects["math"]]
    print(f"数学原始标准差     : {stats.stdev(subjects['math']):.2f}")
    print(f"数学加10分后标准差 : {stats.stdev(math_boosted):.2f}")
    print("（结论：整体平移不改变离散程度，标准差不变）")


if __name__ == "__main__":
    main()
