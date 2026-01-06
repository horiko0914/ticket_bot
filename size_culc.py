
from fractions import Fraction

def size_culc(x, y):
    type_a = Fraction(5*x, 8*y)
    type_b = Fraction(7*x, 10*y)
    type_c = Fraction(3*x, 4*y)
    return type_a, type_b, type_c

def print_size(x, y):
    type_a, type_b, type_c = size_culc(x, y)
    print(f"横枚数{x}、縦枚数{y}で計{x*y}枚の時")
    print("横: 縦")
    print(type_a.numerator,":" , type_a.denominator)
    print(type_b.numerator,":" , type_b.denominator)
    print(type_c.numerator,":" , type_c.denominator)

# 横枚数、縦枚数
print_size(1, 1)
print_size(2, 1)
print_size(3, 1)
print_size(4, 1)
print_size(5, 1)
print()
print_size(2, 2)
print_size(3, 2)
print_size(4, 2)
print_size(5, 2)
print()
print_size(3, 3)
print_size(4, 3)
print_size(5, 3)





# https://qiita.com/simonritchie/items/2931963a6f102b8c7853

# 無理数の近似の値を取得
# print(Fraction(22, 7).limit_denominator(max_denominator=5))

"""
横枚数1、縦枚数1で計1枚の時
横: 縦
5 : 8
7 : 10
3 : 4
横枚数2、縦枚数1で計2枚の時
横: 縦
5 : 4
7 : 5
3 : 2
横枚数3、縦枚数1で計3枚の時
横: 縦
15 : 8
21 : 10
9 : 4
横枚数4、縦枚数1で計4枚の時
横: 縦
5 : 2
14 : 5
3 : 1
横枚数5、縦枚数1で計5枚の時
横: 縦
25 : 8
7 : 2
15 : 4

横枚数2、縦枚数2で計4枚の時
横: 縦
5 : 8
7 : 10
3 : 4
横枚数3、縦枚数2で計6枚の時
横: 縦
15 : 16
21 : 20
9 : 8
横枚数4、縦枚数2で計8枚の時
横: 縦
5 : 4
7 : 5
3 : 2
横枚数5、縦枚数2で計10枚の時
横: 縦
25 : 16
7 : 4
15 : 8

横枚数3、縦枚数3で計9枚の時
横: 縦
5 : 8
7 : 10
3 : 4
横枚数4、縦枚数3で計12枚の時
横: 縦
5 : 6
14 : 15
1 : 1
横枚数5、縦枚数3で計15枚の時
横: 縦
25 : 24
7 : 6
"""
