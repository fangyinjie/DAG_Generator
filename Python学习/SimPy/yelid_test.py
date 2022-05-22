#!/usr/bin/env python3
# #-*-coding:utf-8 -*
def yield_test(n):
    init_number = 0

    while init_number <=n:
        print("-" * 20)
        print("现在位置是生成器函数循环体内")
        print("yield 语句传递的元素值是%d" % n)
        yield n
        print("表示回到生成器函数,完成函数内的")
        print("-" * 20 + "\n")

        n -= 1


for i in yield_test(3):
    print ("=" * 20)
    print("现在位置是在生成器函数外,i的值为 %d" % i)
    print("yield 语句传递的元素值进行平方处理 %d" % i ** 2)
    print("="* 20 + "\n")