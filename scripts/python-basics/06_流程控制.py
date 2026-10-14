# -*- coding: utf-8 -*-
"""
第 05 讲：流程控制
====================
解决：学完第 01 讲后，系统过一遍 if/for/while、缩进、真值判断、break/continue，
并全部落到统计场景（挑不及格、手算均值/标准差）。
运行：python scripts/python-basics/06_流程控制.py（Windows + Python 3.12/3.13，仅标准库）
掌握：1) 缩进即语法 2) 三大分支循环结构 3) 手算统计量呼应第 01 讲
"""

# 知识点 1：缩进即语法（4 空格，同一块必须一致，没有大括号）
def demo_indentation():
    print(">> 1. 缩进即语法")
    print("   Python 靠缩进划分代码块，不靠大括号 {}。同一块缩进必须一致（推荐 4 空格）。")
    score = 88
    if score >= 60:
        print("   分支命中：成绩及格（这行缩进 4 空格，属于 if 块）")
    print("   这行没缩进，已回到主流程，无论 if 是否命中都会执行")

# 知识点 2：if / elif / else（从上到下匹配，命中即跳出）
def demo_if_elif_else():
    print("\n>> 2. if / elif / else：从上往下匹配，命中第一个就跳出，后面 elif 不再判断")
    x = 5
    if x > 10:
        print("   不会走到这里（x=5 不满足）")
    elif x > 3:
        print("   命中这里：x > 3（命中后直接跳出，下面 elif 被跳过）")
    elif x > 0:
        print("   不会走到这里（上面的 elif 已命中）")
    else:
        print("   也不会走到这里")

# 知识点 3：真值判断（哪些值被当成“假”）
def demo_truthiness():
    print("\n>> 3. 真值判断：下列值在 if 里都等价于 False")
    for v in [0, 0.0, "", [], {}, (), None, False]:
        print(f"   bool({v!r}) = {bool(v)}")
    print("   其他值（如 1、'a'、[1]）都是 True。")
    print("   实用建议：判断列表非空写 if items: 而不是 if len(items) > 0:")
    items = []
    if items:
        print("   列表非空才进这里")
    else:
        print("   items 为空 -> bool([]) 是 False -> 走了 else 分支")

# 知识点 4：while 循环（计数器写法 + 必须有终止条件）
def demo_while():
    print("\n>> 4. while 循环：计数器写法，循环必须有终止条件（否则卡死，按 Ctrl+C 中断）")
    count = 0
    total = 0
    while count < 5:
        total += count
        count += 1          # 终止条件依赖它，少了这行会死循环
    print(f"   while 累加 0..4 的结果 = {total}（循环跑了 {count} 次后正常退出）")
    print("   补充：while 还支持 else 子句（循环正常结束才执行），日常较少用。")

# 知识点 5：for 循环 + range()（stop 取不到）
def demo_for_and_range():
    print("\n>> 5. for 循环与 range()：for 遍历序列；range 的 stop 是“取不到”的")
    for ch in "abc":
        print(f"   字符: {ch}")
    for n in [10, 20, 30]:
        print(f"   列表元素: {n}")
    for k, v in {"语文": 80, "数学": 90}.items():
        print(f"   科目 {k} 分数 {v}（dict.items() 同时取键值）")
    print(f"   range(5)        -> {list(range(5))}        （0..4，不含 5）")
    print(f"   range(2, 6)     -> {list(range(2, 6))}     （2..5，不含 6）")
    print(f"   range(0, 10, 2) -> {list(range(0, 10, 2))} （步长 2）")

# 知识点 6：break / continue（只影响最内层循环）
def demo_break_continue():
    print("\n>> 6. break / continue：break 结束循环，continue 跳到下一轮；都只影响最内层")
    for i in range(5):
        if i == 3:
            break
        print(f"   break 演示：i={i}（i==3 时直接结束循环）")
    for i in range(5):
        if i == 2:
            continue
        print(f"   continue 演示：i={i}（i==2 时跳过本次）")

# 知识点 7：enumerate()（同时拿下标和值）
def demo_enumerate():
    print("\n>> 7. enumerate()：遍历时同时拿到下标和值（对比手动计数器写法）")
    fruits = ["苹果", "香蕉", "橙子"]
    idx = 0
    for f in fruits:
        print(f"   手动计数: 第{idx}个是 {f}")
        idx += 1
    for i, f in enumerate(fruits):
        print(f"   enumerate: 第{i}个是 {f}")

# 知识点 8：zip()（并行遍历，以短为准）
def demo_zip():
    print("\n>> 8. zip()：并行遍历多个序列；长度不一致时以短的为准")
    names = ["小明", "小红", "小刚"]
    scores = [85, 92]
    for name, score in zip(names, scores):
        print(f"   {name} 的分数是 {score}（scores 只有 2 个，小刚被忽略）")

# 知识点 9：嵌套循环（内层跑完才轮到外层）
def demo_nested():
    print("\n>> 9. 嵌套循环：5x5 加法表（外层每走一步，内层从头跑到尾）")
    for i in range(1, 6):
        print("   " + "  ".join(f"{i}+{j}={i+j}" for j in range(1, 6)))

# 知识点 10：实用场景 —— 挑不及格、手算均值/最大值/计数
def demo_stats_loop():
    print("\n>> 10. 实用场景：用循环挑不及格、手算统计量")
    scores = [88, 45, 92, 60, 30, 77, 58, 95]
    failed = [s for s in scores if s < 60]
    total = 0
    max_score = scores[0]
    for s in scores:
        total += s
        if s > max_score:
            max_score = s
    mean = total / len(scores)
    print(f"   全部成绩: {scores}")
    print(f"   不及格(<60): {failed}")
    print(f"   手算：总和={total} 均值={mean:.2f} 最大值={max_score}")
    print("   提示：以后用 sum()/max()/len() 或 statistics 库更省事，但手算一遍才懂循环。")

# 知识点 11：while 做输入校验逻辑（只写逻辑，不真的 input）
def demo_input_validation():
    print("\n>> 11. while 做输入校验逻辑（用固定值模拟，不阻塞 input）")
    user_input = "abc"
    attempts = 0
    while attempts < 3:
        valid = user_input.isdigit() and 0 <= int(user_input) <= 100
        if valid:
            print(f"   输入合法：{user_input}")
            break
        print(f"   第{attempts + 1}次输入 '{user_input}' 不合法，重新输入...")
        user_input = "85"
        attempts += 1
    print("   （真实代码把 user_input 换成 input('请输入0-100的整数: ') 即可）")

# 知识点 12：统计呼应 —— 手算均值与标准差（呼应第 01 讲）
def demo_std_dev():
    print("\n>> 12. 呼应第 01 讲：用循环手算均值与标准差")
    data = [72, 85, 90, 60, 78, 92, 88, 76]
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)   # 总体方差（除以 n）
    std = variance ** 0.5
    print(f"   数据: {data}")
    print(f"   手算均值   = {mean:.3f}")
    print(f"   手算标准差 = {std:.3f}（总体标准差，除以 n）")
    print("   对比：第 01 讲 statistics.stdev 是样本标准差（除以 n-1），数值略不同是分母差异。")

def main():
    print("=" * 60)
    print("第 05 讲 · 流程控制  ——  配套脚本 06_流程控制.py")
    print("=" * 60)
    demo_indentation()
    demo_if_elif_else()
    demo_truthiness()
    demo_while()
    demo_for_and_range()
    demo_break_continue()
    demo_enumerate()
    demo_zip()
    demo_nested()
    demo_stats_loop()
    demo_input_validation()
    demo_std_dev()
    print("\n" + "=" * 60)
    print("本讲 3 条要点小结")
    print("=" * 60)
    print("  1. 缩进即语法：4 个空格，同一块必须一致，没有大括号。")
    print("  2. for 遍历序列、while 看条件；range 的 stop 取不到；")
    print("     break/continue 只影响最内层循环。")
    print("  3. enumerate 拿下标、zip 并行遍历；手算统计量帮你看懂循环。")

if __name__ == "__main__":
    main()

# 动手改一改 1：把 demo_std_dev 里的数据换成你自己的成绩列表，重算均值和标准差。
# 动手改一改 2：在 demo_nested 里把加法表改成乘法表（把 i+j 改成 i*j）。
# 动手改一改 3：在 demo_stats_loop 里增加“统计及格率”的计数逻辑。
