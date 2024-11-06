import random
from pyfinite import ffield


F = ffield.FField(8,gen=0x11b,useLUT=0)  # 定义 F_2^8 的有限域
# 可以指定

IRREDUCIBLE_POLY = 0b100011011
# print(c2_inv)

# 定义共享值
x1 = 0x2B  # 共享值1（十六进制表示）
x2 = 0x3D  # 共享值2（十六进制表示）

# 计算 x = x1 + x2
x = x1 ^ x2

# 随机生成8位随机值r，并提取高4位和低4位
r = 0xFe  # 选择与测试值相同的r
r_u = r >> 4                # 高4位
r_l = r & 0x0F              # 低4位

# 计算 ∏(1 - x1[i] - x2[i])，按位运算
product_term = 1
for i in range(8):
    bit_x1 = (x1 >> i) & 1
    bit_x2 = (x2 >> i) & 1
    # 如果某个位上的 1 - x1[i] - x2[i] < 0，则修正为 0

    product_term *= (1 - bit_x1 - bit_x2)
    """
    利用不可约多项式进行处理
    """
    if product_term & 0x100:  # 如果a超过8位
        product_term ^= IRREDUCIBLE_POLY


def get_mod(value):
    """
    利用不可约多项式进行处理
    """
    """
    对超过8位的值进行约简，使用不可约多项式 0x11B（对应于 0b100011011）

    :param value: 要约简的整数值
    :param irreducible: 不可约多项式，默认为 AES 中使用的 0x11B
    :return: 约简后的8位值
    """
    while value >= 0x100:  # 当高于8位时
        # 找到最高位的位数
        highest_bit = value.bit_length() - 1
        # 计算偏移量
        shift = highest_bit - 8
        # 将不可约多项式左移相应的位数，并与当前值异或
        value ^= IRREDUCIBLE_POLY << shift
    return value
# 计算分子 c1 和 分母 c2, 确保每一步都进行处理
# r = r_u/r_l
r_l = random.randint(1,256)
r_u = F.Multiply(r_l,r)


# encoding
c1 = (F.Multiply(x, r_u) ^ r_l) ^ F.Multiply((r_u ^ r_l), product_term)
c2 = (F.Multiply(x, r_l)) ^ F.Multiply(r_l, product_term)

# 计算 x^(-1) + r = c1 / c2  (仅在 c2 不为 0 时)
if c2 != 0:
    # 求模256的逆元: c1 * (c2 的逆元)
    c2_inv = F.Inverse(c2)  # 求 c_2 的逆元

    x_inverse_plus_r = F.Multiply(c1,c2_inv)
    print(f"c2的逆元：{c2_inv}, x_inverse_plus_r: {x_inverse_plus_r}")
else:
    x_inverse_plus_r = None      # 避免除零错误

# 减去随机值 r，得到 x 的逆元
if x_inverse_plus_r is not None:
    x_inverse = (x_inverse_plus_r ^ r)
else:
    x_inverse = None

# 验证逆元是否正确：检查 x * x_inverse 是否等于 1
if x_inverse is not None:
    verification = F.Multiply(x,x_inverse)
else:
    verification = None


# 输出结果
print(f"共享值 x1: {x1:#04x}, x2: {x2:#04x}")
print(f"计算的 x = x1 + x2 = {x:#04x}")
print(f"随机值 r: {r:#04x} (高4位: {r_u:#02x}, 低4位: {r_l:#02x})")
print(f"乘积项 ∏(1 - x1[i] - x2[i]) = {product_term}")
print(f"分子 c1 = {c1}, 分母 c2 = {c2}")
print(f"计算出的 x^(-1) + r = {x_inverse_plus_r}")
print(f"求得的 x 的逆元 x^(-1) = {x_inverse}")
print(f"验证结果: x * x^(-1) = {verification}")

# 检查是否逆元正确
if verification == 1:
    print("验证成功：计算出的逆元是正确的！")
else:
    print("验证失败：计算出的逆元不正确。")

def extended_gcd(a, b):
    """
    使用扩展欧几里得算法计算 a 和 b 的最大公因子 gcd 以及贝祖系数 x, y。
    返回 gcd, x, y，使得 ax + by = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

