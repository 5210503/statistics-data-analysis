# -*- coding: utf-8 -*-
"""
第 06 讲：函数
==============
把"函数"系统过一遍，并把第 01 讲散着写的描述统计过程函数化，作为本套 5 讲的收口。
运行（Windows + VSCode + Python 3.12/3.13）：python scripts/python-basics/07_函数.py
掌握：为什么要函数、参数种类与作用域、文档字符串、纯函数、lambda、类型注解，
以及用 describe()+format_report() 拆解统计过程。
"""

import statistics as stats


def mean(values):
    """计算一组数的算术平均值（本讲贯穿始终的小工具）"""
    return sum(values) / len(values)

# 一、为什么用函数：同样的计算写三遍的对比
def demo_why_function():
    print(">> 一、为什么用函数：没有函数时同样计算要复制三遍")
    a, b, c = [72, 85, 90, 60], [88, 76, 92, 81], [65, 70, 80, 95]
    print("  复制粘贴: A=%.2f B=%.2f C=%.2f" % (sum(a)/len(a), sum(b)/len(b), sum(c)/len(c)))
    print("  函数写法: A=%.2f B=%.2f C=%.2f（逻辑只写一次）" % (mean(a), mean(b), mean(c)))

# 二、定义与调用：def/参数/return；无 return 返回 None；多值返回是元组
def demo_def_and_call():
    print(">> 二、定义与调用：def / 参数 / return")

    def greet(name):
        print("    你好，" + name)

    print("  无 return 时 greet 返回值类型:", type(greet("小明")))

    def min_max(values):
        return min(values), max(values)

    out = min_max([3, 1, 4, 1, 5])
    print("  返回多值的类型:", type(out), "内容:", out)
    lo, hi = min_max([3, 1, 4, 1, 5])  # 元组解包
    print("  解包接收: 最小值 =", lo, "最大值 =", hi)

# 三、参数种类：位置/关键字/默认/*args/**kwargs，重点坑=可变默认参数
def demo_args():
    print(">> 三、参数种类")

    def describe(values, digits=2):
        print("    " + str(round(stats.mean(values), digits)))

    vals = [72, 85, 90, 60]
    print("  位置调用 describe(vals):", end=""); describe(vals)
    print("  关键字调用 describe(values=vals, digits=1):", end=""); describe(values=vals, digits=1)

    def add_item_bad(item, box=[]):   # 危险：默认列表只创建一次
        box.append(item)
        return box

    r1 = add_item_bad("苹果"); print("  可变默认污染: 第一次", r1)
    r2 = add_item_bad("香蕉")
    print("  第二次", r2, "（第一次也变成", r1, "，同一默认列表被污染）")

    def add_item_ok(item, box=None):  # 正确：None 占位，每次新建
        if box is None:
            box = []
        box.append(item)
        return box

    print("  正确写法 box=None: 第一次", add_item_ok("苹果"), "第二次", add_item_ok("香蕉"), "（独立）")

    def my_sum(*args):
        return sum(args)

    print("  *args 求和 my_sum(1,2,3,4,5):", my_sum(1, 2, 3, 4, 5))

    def show_config(**kwargs):
        for k, v in kwargs.items():
            print("    " + str(k) + " = " + str(v))

    print("  **kwargs 打印配置项:")
    show_config(encoding="utf-8", version=3, pretty=True)
    print("  参数顺序: 位置 -> 默认 -> *args -> **kwargs")


# 四、作用域：局部/全局、LEGB、global 尽量别用
def demo_scope():
    print(">> 四、作用域：局部变量 vs 全局变量")
    print("  函数内可见全局变量 outside（不演示 NameError，以免运行报错）")
    print("  LEGB: Local -> Enclosing -> Global -> Built-in")
    print("  global 能改全局但尽量别用——会产生隐蔽副作用，难调试。")


# 五、文档字符串
def demo_docstring():
    print(">> 五、文档字符串（docstring，函数自带说明书）")
    print("  mean.__doc__ =", mean.__doc__)
    print("  说明：raw/statistics/statistics-exercise-01.py 的 load_scores/describe 就是这样写的。")


# 六、纯函数 vs 有副作用
def demo_pure_vs_side():
    print(">> 六、纯函数 vs 有副作用")
    data = [72, 85, 90, 60]

    def describe_pure(values):
        return {"n": len(values), "均值": mean(values)}

    def describe_side(values):
        print("    内部打印: 均值 = " + str(round(mean(values), 2)))

    print("  纯函数只返回:", describe_pure(data))
    print("  有副作用的函数自己打印:")
    describe_side(data)
    print("  做数据分析尽量写纯函数，输出交给调用方——第 01 讲练习即此做法。")


# 七、lambda 表达式
def demo_lambda():
    print(">> 七、lambda：只能写一个表达式的匿名函数")
    scores = [72, 85, 90, 60, 78, 92, 88, 76]
    print("  降序 sorted(scores, key=lambda x: -x):", sorted(scores, key=lambda x: -x))
    students = [("小明", 88), ("小红", 95), ("小刚", 72)]
    print("  按分数排序:", sorted(students, key=lambda t: t[1]))


# 八、类型注解（运行时不强制检查）
def demo_type_hints():
    print(">> 八、类型注解：给人/工具看，运行时【不】强制检查")

    def mean_hint(values: list[float]) -> float:
        return sum(values) / len(values)

    print("  正确类型 mean_hint([1.0,2.0,3.0]):", mean_hint([1.0, 2.0, 3.0]))
    print("  传错类型 mean_hint([1,2,3]) 也不报错:", mean_hint([1, 2, 3]))


# 九、收尾串联：把第 01 讲统计过程函数化
def demo_capstone():
    print(">> 九、收尾串联：describe() 返回 dict，format_report() 负责打印")
    scores = [72, 85, 90, 60, 78, 92, 88, 76]

    def describe(scores):
        return {"n": len(scores), "均值": stats.mean(scores),
                "中位数": stats.median(scores), "标准差": stats.stdev(scores)}

    def format_report(name, report):
        print("  ==== " + name + " 报告 ====")
        for k, v in report.items():
            print("    " + str(k) + ": " + (str(round(v, 2)) if isinstance(v, float) else str(v)))

    format_report("期末成绩", describe(scores))
    print("  函数拆解 = 把一段事拆成几个可命名的小事。")


def main():
    print("############################################")
    print("# 第 06 讲 · 函数 · 运行结果")
    print("############################################")
    demo_why_function()
    demo_def_and_call()
    demo_args()
    demo_scope()
    demo_docstring()
    demo_pure_vs_side()
    demo_lambda()
    demo_type_hints()
    demo_capstone()
    print("============================================")
    print("本讲 3 条要点小结：")
    print("  1. 函数 = 封装复用 + 命名即文档 + 便于单独测试")
    print("  2. 默认值别用可变对象；参数顺序 位置->默认->*args->**kwargs")
    print("  3. 尽量写纯函数（只 return），统计用 describe+format_report 拆解")
    print("============================================")


if __name__ == "__main__":
    main()

# 动手改一改 1：给 describe 增加「最大值」「最小值」两个字段并打印。
# 动手改一改 2：把 add_item_ok 改成支持传入初始 box（默认 None），再追加多个 item。
# 动手改一改 3：用 lambda 给 students 按姓名（元组第 1 项）排序，而非按分数。
