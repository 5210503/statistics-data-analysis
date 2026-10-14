# -*- coding: utf-8 -*-
"""
第 02 讲：变量
================
本讲要解决什么问题：
    你已经用 Python 算过均值、中位数、标准差，但可能没仔细想过——
    每次写 `mean = stats.mean(scores)` 时，等号到底在"做"什么？
    变量到底是个什么东西？为什么 1 和 1.0 在 Python 里是两种不同类型？

怎么运行：
    python scripts/python-basics/03_变量.py
    （Python 3.12 / 3.13，仅使用标准库，无需联网或安装任何第三方包）

跑完本讲你能掌握：
    1. 变量是"贴在某个对象上的标签"，不是装数据的盒子
    2. 变量的命名规则、区分大小写、动态类型与五种基本数据类型
    3. 可变与不可变对象的本质区别（用 id() 看穿它）
"""

import keyword


def demo_what_is_variable():
    """变量是什么：名字到对象的绑定关系，= 是绑定操作"""
    print("==== 1. 变量是什么：名字 -> 对象的绑定 ====")
    # = 不是"把值放进变量"，而是给右边的对象贴一个名字标签
    score = 88
    print("score = 88        # 给整数对象 88 贴上叫 score 的标签")
    print("score 现在指向:", score)
    # 再给同一个对象贴第二个标签
    another = score
    print("another = score   # another 和 score 指向同一个对象:", another)
    print("结论: 变量是'标签'不是'盒子'，数据是对象本身，变量只是名字")
    print()


def demo_naming():
    """命名规则：合法标识符、区分大小写、保留字、snake_case"""
    print("---- 2. 命名规则 ----")
    print("Python 保留字(关键字)示例:", keyword.kwlist[:8], "...")
    # 判断一个名字是否合法：是合法标识符且不是保留字
    def is_valid_name(name):
        return name.isidentifier() and not keyword.iskeyword(name)
    print("'mean_score' 合法吗 ?", is_valid_name("mean_score"))
    print("'class' 合法吗 ?", is_valid_name("class"), "  # class 是保留字")
    print("'2score' 合法吗 ?", is_valid_name("2score"), "  # 不能以数字开头")
    print("区分大小写: MEAN 和 mean 是两个不同的变量")
    mean, MEAN = 10, 20
    print("  mean =", mean, "  MEAN =", MEAN)
    print("PEP 8 惯例: 变量名用小写+下划线 snake_case, 如 student_count")
    print()


def demo_dynamic_type():
    """动态类型：变量本身没有类型，对象才有"""
    print("---- 3. 动态类型：变量无类型，对象有类型 ----")
    x = 5
    print("x = 5        -> type(x) =", type(x),
          " isinstance(x, int) =", isinstance(x, int))
    x = "hello"
    print("x = 'hello'  -> type(x) =", type(x),
          " isinstance(x, str) =", isinstance(x, str))
    print("同一个名字 x 先后指向 int 和 str，说明'变量无类型，对象有类型'")
    print()


def demo_basic_types():
    """基本类型概览：int / float / bool / str / NoneType"""
    print("---- 4. 基本类型概览 ----")
    a = 10;    print("int    :", a, "->", type(a))
    b = 3.14;  print("float  :", b, "->", type(b))
    c = True;  print("bool   :", c, "->", type(c))
    d = "数据"; print("str    :", d, "->", type(d))
    e = None;  print("None   :", e, "->", type(e), "  # 表示'没有值'")
    print()


def demo_mutable_immutable():
    """可变与不可变：用 id() 观察对象身份"""
    print("---- 5. 可变与不可变：id() 看对象身份 ----")
    n = 100
    print("int  n =", n, " id =", id(n))
    n = 200
    print("n = 200   id =", id(n), " # id 变了 -> 整数不可变，是重新绑定")
    s = "abc"
    print("str  s =", s, " id =", id(s))
    s = s + "d"
    print("s = s+'d' id =", id(s), " # id 变了 -> 字符串不可变")
    lst = [1, 2, 3]
    print("list lst =", lst, " id =", id(lst))
    lst.append(4)
    print("lst.append(4) ->", lst, " id =", id(lst), " # id 不变 -> 列表可变")
    print()


def demo_type_convert():
    """类型转换：int / float / str / bool 及易错点"""
    print("---- 6. 类型转换 ----")
    print("int('42')    =", int("42"))
    print("float('3.5') =", float("3.5"))
    print("str(3.14)    =", str(3.14))
    # 易错 1：int() 不能解析带小数点的字符串，会抛 ValueError
    try:
        int("3.5")
    except ValueError as err:
        print("int('3.5') 报错:", type(err).__name__, "- 字符串里的小数点无法解析")
    # 易错 2：int() 是截断而非四舍五入
    print("int(3.99)    =", int(3.99), " # 截断成 3，不是 4")
    # 易错 3：bool() 的真假规则
    print("bool('')     =", bool(""), "  bool('0') =", bool("0"),
          " # 非空字符串都是 True")
    print("bool(0)      =", bool(0), "  bool([])  =", bool([]),
          " # 0 和空容器是 False")
    print()


def demo_unpacking():
    """多重赋值与解包"""
    print("---- 7. 多重赋值与解包 ----")
    a = b = 1
    print("a = b = 1    -> a =", a, " b =", b)
    x, y = 1, 2
    print("x, y = 1, 2  -> x =", x, " y =", y)
    x, y = y, x
    print("x, y = y, x  -> 交换后 x =", x, " y =", y)
    print()


def demo_in_statistics():
    """落到统计场景：给中间结果起名字提升可读性"""
    print("==== 8. 落到统计场景：给中间结果起名字 ====")
    scores = [72, 85, 90, 60, 78, 92, 88, 76]
    n = len(scores)
    total = sum(scores)
    mean = total / n
    # 方差(总体)：每个数据与均值之差的平方的平均
    squared_diff = [(s - mean) ** 2 for s in scores]
    variance = sum(squared_diff) / n
    std_dev = variance ** 0.5
    print("scores          =", scores)
    print("n (样本数)       =", n)
    print("mean (均值)      =", round(mean, 3))
    print("std_dev (标准差)  =", round(std_dev, 3))
    print("起名价值: mean / variance / std_dev 让公式读起来像数学书")
    print("# 注: input() 永远返回 str，本脚本不调用它以免阻塞；")
    print("#      需要时记得自行用 int(input()) 之类转换类型")
    print()


def print_summary():
    print(">> 本讲 3 条要点小结")
    print("1. 变量是贴到对象上的标签，= 是绑定；重绑定只是换标签，不搬数据")
    print("2. 变量无类型、对象有类型；int/str 不可变，list 可变（看 id 便知）")
    print("3. 类型转换要当心：int() 截断不四舍五入，int('3.5') 会报错")
    print()


def main():
    demo_what_is_variable()
    demo_naming()
    demo_dynamic_type()
    demo_basic_types()
    demo_mutable_immutable()
    demo_type_convert()
    demo_unpacking()
    demo_in_statistics()
    print_summary()


if __name__ == "__main__":
    main()

# 动手改一改 1：把 demo_in_statistics 里的 scores 换成你自己的成绩，
#               看看均值和标准差会怎么变。
# 动手改一改 2：用 id() 验证 bool 值 True / False 在 Python 里只有两个单例对象。
# 动手改一改 3：试试用 a, b, *rest = [1, 2, 3, 4] 解包，rest 会得到什么？
