# -*- coding: utf-8 -*-
"""
第03讲：运算符
====================
本讲解决什么问题：
    你已经会用 Python 算均值 / 中位数 / 标准差，但代码里出现的
    + - * / // % ** 、== and or 、in 等符号到底怎么工作？
    为什么 -7 // 2 == -4？为什么 0.1 + 0.2 != 0.3？本讲一次性讲清。

怎么运行（Windows + VSCode + Python 3.12/3.13，仅标准库）：
    python scripts/python-basics/04_运算符.py

跑完你能掌握：
    - 各类运算符的语义与易错点（/ 永远 float、// 向下取整、% 符号跟除数走）
    - 短路求值、运算符优先级、浮点精度陷阱
    - 把运算符用到「判断奇偶、分页、标准化」等真实场景
"""

import math


def demo_arithmetic():
    # 算术运算符 + - * / // % **
    print(">> 算术运算符")
    print("5 / 2  =", 5 / 2)           # / 永远返回 float
    print("5 // 2 =", 5 // 2)          # // 向下取整
    print("-7 // 2 =", -7 // 2)        # 负数也向下: floor(-3.5) = -4
    print("-7 % 2  =", -7 % 2)         # 余数符号跟除数走: -7 = 2*(-4) + 1
    print("2 ** 10 =", 2 ** 10)        # 整数幂: 1024
    print("math.pow(2, 10) =", math.pow(2, 10))  # 永远返回 float
    print("（差别：** 对整数返回 int；math.pow 永远 float，且只接受两个参数）")
    print()


def demo_compare():
    # 比较运算符返回 bool；== 比「值」，is 比「同一对象」
    print(">> 比较运算符与 is")
    print("3 == 3 ->", 3 == 3, "  3 != 4 ->", 3 != 4)

    a = 1000
    b = int("1000")                    # 运行时构造，是另一个对象
    print("int : a == b ->", a == b, "  a is b ->", a is b)   # True / False

    s1 = "data"
    s2 = "".join(["d", "a", "t", "a"])
    print("str : s1 == s2 ->", s1 == s2, "  s1 is s2 ->", s1 is s2)  # True / False
    lst1, lst2 = [1, 2, 3], [1, 2, 3]
    print("list: lst1 == lst2 ->", lst1 == lst2, "  lst1 is lst2 ->", lst1 is lst2)

    x = None
    print("判断空值用 is None: x is None ->", x is None)   # 推荐写法
    print()


def demo_logic():
    # 逻辑运算符 and / or / not；短路求值
    print(">> 逻辑运算符与短路求值")

    def side_effect():
        print("   （side_effect 真的被执行了）")
        return True

    print("False and side_effect() ->", False and side_effect())
    print("（左侧为 False，右侧 side_effect 没被调用）")
    print("True or side_effect()  ->", True or side_effect())
    print("（左侧为 True，右侧同样没被调用）")
    # and / or 返回操作数本身，不一定是 True/False
    print("0 and 5 ->", 0 and 5, "  3 and 5 ->", 3 and 5, "  0 or 5 ->", 0 or 5, "  not 0 ->", not 0)
    print()


def demo_assign():
    # 赋值运算符 += -= *= /= //= %= **=
    print(">> 赋值运算符")
    n = 10
    n += 3
    print("n=10; n += 3 ->", n)        # 13
    n -= 2
    print("n -= 2      ->", n)         # 11
    n *= 2
    print("n *= 2      ->", n)         # 22
    n //= 3
    print("n //= 3     ->", n)         # 7
    # += 对 list 是原地修改，对 int/str 是重新绑定
    lst = [1, 2, 3]
    ref = lst
    lst += [4]
    print("lst += [4]  ->", lst, "  ref 也变 ->", ref)
    print()


def demo_membership():
    # 成员运算符 in / not in
    print(">> 成员运算符 in / not in")
    print("'a' in 'cat' ->", "a" in "cat", "  4 in [1,2,3] ->", 4 in [1, 2, 3])
    d = {"math": 90, "chinese": 85}
    print("'math' in d ->", "math" in d, "  'english' not in d ->", "english" not in d)


def demo_bit():
    # 位运算符（点到为止）
    print(">> 位运算符（点到为止）")
    print("6 & 3 =", 6 & 3, "  6 | 3 =", 6 | 3, "  6 ^ 3 =", 6 ^ 3, "  ~6 =", ~6)
    print("1 << 3 =", 1 << 3, "（左移3位 = 乘 2^3）  16 >> 2 =", 16 >> 2, "（右移2位 = 整除 2^2）")
    print("（用途：底层/性能场景，日常数据分析很少手写，认识即可）")


def demo_precedence():
    # 运算符优先级记忆主线：算术 > 比较 > 逻辑 > 赋值
    print(">> 运算符优先级（记忆主线: 算术 > 比较 > 逻辑 > 赋值）")
    print("2 + 3 * 4 =", 2 + 3 * 4)    # 14，不是 20
    print("True or False and False ->", True or False and False)  # True
    print("（等价于 True or (False and False)，and 比 or 先算）")
    print("不确定时加括号，(2 + 3) * 4 =", (2 + 3) * 4)


def demo_float():
    # 浮点精度陷阱
    print(">> 浮点精度陷阱")
    print("0.1 + 0.2 == 0.3 ?", 0.1 + 0.2 == 0.3)   # False
    print("round(0.1 + 0.2, 1) =", round(0.1 + 0.2, 1))  # 0.3
    print("math.isclose(0.1+0.2, 0.3) =", math.isclose(0.1 + 0.2, 0.3))  # True
    print()


def demo_scenarios():
    # 把运算符用到真实小场景
    print(">> 实用场景")
    for n in (4, 7):
        print(f"  {n} 是偶数? {n % 2 == 0}")
    n, size = 23, 5
    print(f"  {n} 条数据每页 {size} 条 -> 共 {(n + size - 1) // size} 页")  # 分页 ceil
    print("  保留两位小数 round(3.14159, 2) =", round(3.14159, 2))
    c = 37.0
    print(f"  {c} 摄氏度 = {c * 9 / 5 + 32} 华氏度")   # 摄氏转华氏
    print()


def demo_statistics():
    # 运算符落到统计场景
    print(">> 落到统计场景")
    scores = [72, 85, 90, 60, 78, 92, 88, 76]
    rng = max(scores) - min(scores)     # 极差用 -
    print("  极差 = max - min =", rng)
    # 标准化 z = (x - mean) / std，用到 -  **  /
    mean = sum(scores) / len(scores)
    var = sum((x - mean) ** 2 for x in scores) / len(scores)
    std = var ** 0.5
    z = [(x - mean) / std for x in scores[:3]]
    print("  均值 =", round(mean, 2), " 标准差 =", round(std, 2))
    print("  前3个成绩标准化:", [round(v, 3) for v in z])
    print()


def main():
    demo_arithmetic()
    demo_compare()
    demo_logic()
    demo_assign()
    demo_membership()
    demo_bit()
    demo_precedence()
    demo_float()
    demo_scenarios()
    demo_statistics()

    print("==== 本讲小结 ====")
    print("1. / 永远 float；// 向下取整（负数同理）；% 符号跟除数走；** 是整数幂、math.pow 永远 float")
    print("2. == 比『值』，is 比『同一对象』；判断 None 用 is None；and/or 返回操作数本身且会短路")
    print("3. 浮点别用 == 比较，用 round() 或 math.isclose()；不确定优先级就加括号")
    print()
    print("动手练完本脚本后，可继续看 notes/第04讲-表达式.md")


if __name__ == "__main__":
    main()

# 动手改一改 1：把 demo_scenarios 的 n=23, size=5 改成 22 和 6，预测并验证总页数。
# 动手改一改 2：写一个用成员运算符判断成绩是否落在 [60, 100] 区间里的表达式。
# 动手改一改 3：把摄氏转华氏反过来，写一段华氏转摄氏代码 (c = (f - 32) * 5 / 9)。
