# -*- coding: utf-8 -*-
"""
第 04 讲：表达式
================
解决什么问题：运算符和表达式常常被混为一谈。本讲把重点放在
“表达式与语句的区别、求值顺序、以及 Python 特有的几种表达式写法”上。

怎么运行：在 VSCode 终端里执行  python scripts/python-basics/05_表达式.py
（建议用 Python 3.8+，海象运算符 := 与 f-string 调试写法需要 3.8）

跑完能掌握：
1. 区分“表达式（一定有值）”和“语句（不一定）”
2. 看懂优先级 / 结合性，以及“拿不准就加括号”
3. 用短路、三元、海象、解包、f-string 表达式写出更地道的统计代码
"""

# 第 03 讲已经讲过运算符本身，本讲在其之上讲“表达式”这个概念。


def demo_expr_vs_stmt():
    """表达式一定有值，语句不一定。"""
    print(">> 表达式 vs 语句")
    # 1 + 2 是表达式：求值后产生一个值 3
    print("type(1 + 2)        =", type(1 + 2))      # <class 'int'>
    # print(...) 也是表达式！它有副作用(打印)，并返回 None —— 这是反直觉点
    print("type(print('x'))   =", type(print("x")))  # 先打印 x，再返回 NoneType
    # x = 1 整体是“赋值语句”，不是表达式（Python 里不能写 y = (x = 1)）
    x = 1
    # 但 = 右边的 1 + 2 是表达式，先求值成 3，再赋给 x
    x = 1 + 2
    print("x 现在是            =", x)
    print("结论：表达式‘有值’，语句‘做事’；赋值号右边永远是表达式")
    print()


def demo_eval_order():
    """子表达式按优先级 + 结合性求值。"""
    print(">> 求值顺序：优先级 + 结合性")
    print("2 + 3 * 4           =", 2 + 3 * 4)        # 14，先乘后加
    print("2 ** 3 ** 2         =", 2 ** 3 ** 2)      # 512，幂运算右结合
    a, b = 5, 5
    print("not a == b          =", not a == b)       # False，== 优先于 not
    # 拿不准就加括号，括号是给读代码的人看的，不改变机器结果
    print("(2 + 3) * 4         =", (2 + 3) * 4)      # 20，显式表达意图
    print()


def demo_short_circuit():
    """短路求值本身就是表达式，能拿来给默认值。"""
    print(">> 短路求值（也是表达式）")
    user_input = ""                       # 模拟用户没输入
    value = user_input or "默认值"
    print("value = user_input or '默认值' =", value)   # 默认值
    x = 0
    # result = x and x.name ：x 为假时直接返回 x，不会去碰 .name
    result = x and "名字"
    print("result = x and '名字' (x=0)    =", result)  # 0
    # 证明右侧未被求值：用一个会打印副作用的函数
    def noisy():
        print("  （noisy 被调用了）")
        return "响了"
    print("True or noisy()  =", True or noisy())       # 短路，noisy 不执行
    print("False and noisy()=", False and noisy())     # 短路，noisy 不执行
    print()


def demo_ternary():
    """条件表达式 a if cond else b。"""
    print(">> 条件表达式（三元）")
    score = 58
    label = "及格" if score >= 60 else "不及格"
    print("label = '及格' if score>=60 else '不及格' =", label)  # 不及格
    # 嵌套三元可读性差，优先写成普通 if 或查表
    grade = ("A" if score >= 90 else
             "B" if score >= 75 else
             "C" if score >= 60 else "D")
    print("嵌套三元 grade =", grade)                     # D
    # 替代写法（更清晰）：用字典查表
    table = {90: "A", 75: "B", 60: "C"}
    grade2 = next((g for t, g in table.items() if score >= t), "D")
    print("查表写法 grade =", grade2)                    # D
    print()


def demo_walrus():
    """赋值表达式 := 解决‘算了还要再用一次’。"""
    print(">> 赋值表达式（海象运算符 :=，Python 3.8+）")
    data = [12, 19, 7, 23]
    # 不用 :=：要把 len 算出来再比较，等于算两次
    # 用 := ：在条件里算一次并绑定给 n
    if (n := len(data)) > 3:
        print("列表长度 n =", n, "，超过 3")   # n = 4
    # while 里逐次取值直到 None：这里用固定序列演示
    total = 0
    vals = iter([1, 2, 3])
    while (v := next(vals, None)) is not None:
        total += v
    print("求和 total =", total)   # 6
    print()


def demo_unpack():
    """序列解包表达式。"""
    print(">> 序列解包")
    a, b = 1, 2
    a, b = b, a            # 经典交换：右侧先打包成元组，再整体解包
    print("交换后 a, b =", a, b)   # 2 1
    first, *rest = [1, 2, 3, 4]
    print("first, *rest =", first, rest)   # 1 [2, 3, 4]
    # * 收集剩余项，rest 永远是列表
    head, *middle, tail = [10, 20, 30, 40]
    print("head, *middle, tail =", head, middle, tail)  # 10 [20, 30] 40
    print("引子：函数传参时 *seq 也能把序列‘展开’成多个位置参数（下讲细说）")
    print()


def demo_fstring():
    """f-string 里可以放任意表达式，对统计报告很实用。"""
    print(">> f-string 里的表达式")
    a, b = 3, 4
    x = 1.234567
    ratio = 0.375
    print(f"a + b = {a + b}")                 # a + b = 7
    print(f"x 保留两位小数   : {x:.2f}")      # 1.23
    print(f"ratio 百分比     : {ratio:.1%}")  # 37.5%
    print(f"{a + b = }")                      # a + b = 7（3.8+ 调试写法）
    print()


def demo_chained_compare():
    """比较链只求值一次。"""
    print(">> 比较链")
    score = 85
    print("0 < score <= 100   =", 0 < score <= 100)        # True
    # 语义等价于下面，但 score 只被求值一次
    print("0 < score and score <= 100 =", 0 < score and score <= 100)  # True
    print("证明：比较链里 score 只算了一次")
    def log_score():
        print("  （score 被读取）")
        return 85
    print("(0 < log_score() <= 100) =", 0 < log_score() <= 100)  # 只打印一次
    print()


def demo_pitfalls():
    """两个常见坑：共享别名 vs 不可变安全。"""
    print(">> 常见坑")
    a = b = []            # 两个名字指向【同一个】列表
    a.append(1)
    print("a = b = [] 后 a, b =", a, b)   # [1] [1] —— 坑！同时变了
    x = y = 0            # int 不可变，所以安全
    x = x + 1
    print("x = y = 0 后 x, y =", x, y)    # 1 0 —— 没影响
    print("预告：列表推导式 [x for x in ...] 是循环的简写形式，第 05 讲先把循环本身讲清")
    print()


def demo_statistics_scene():
    """落到统计场景：一个表达式算 z-score 并格式化及格率。"""
    print(">> 落到统计场景")
    scores = [72, 85, 90, 60, 78, 92, 88, 76]
    mean = sum(scores) / len(scores)
    std = (sum((s - mean) ** 2 for s in scores) / len(scores)) ** 0.5
    z = lambda s: (s - mean) / std
    print(f"均值               : {mean:.2f}")   # 80.12
    print(f"标准差             : {std:.2f}")    # 10.10
    print(f"分数 90 的 z-score : {z(90):.2f}")
    passed = sum(1 for s in scores if s >= 60)
    rate = passed / len(scores)
    print(f"及格率             : {rate:.1%}")   # 100.0%
    print()


def main():
    print("=" * 50)
    print("第 04 讲 · 表达式  —— 一次跑完的演示脚本")
    print("=" * 50)
    print()
    demo_expr_vs_stmt()
    demo_eval_order()
    demo_short_circuit()
    demo_ternary()
    demo_walrus()
    demo_unpack()
    demo_fstring()
    demo_chained_compare()
    demo_pitfalls()
    demo_statistics_scene()

    print(">> 本讲 3 条要点小结")
    print("1. 表达式‘有值’、语句‘做事’；函数调用也返回 None，别被副作用骗了")
    print("2. 拿不准求值顺序就加括号——括号是写给读代码的人看的")
    print("3. 短路 / 三元 / 海象 / 解包 / f-string 表达式让统计代码更短更清楚")
    print()
    print("配套讲义：notes/第04讲-表达式.md")


if __name__ == "__main__":
    main()

# 动手改一改 1：把 demo_short_circuit 里的 user_input 改成 "我的数据"，再看 value 变成什么？
# 动手改一改 2：在 demo_walrus 的 while 循环里，把序列换成 [5, 6, 7]，total 会变成多少？
# 动手改一改 3：把 demo_statistics_scene 的及格线从 60 改成 80，及格率会怎么变？
