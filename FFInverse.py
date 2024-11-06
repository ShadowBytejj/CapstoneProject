import galois
from pyfinite import ffield

# 定义 GF(2^2) 和 GF(2^4) 的不可约多项式
LAMBDA = 0b111   # x^2 + x + 1 (在 GF(2^2) 上不可约)
LAMBDA_GF2 = LAMBDA
DELTA = 0b10011 # y^4 + y + 1 (在 GF(2^4) 上不可约)
DELTA_GF4 = DELTA
# GF(2^2) 中的加法（在 GF(2) 上按位异或）

# 导入 galois 库



def add_gf2(a, b):
    return a ^ b
# GF(2^2) 中的乘法，使用不可约多项式 x^2 + x + 1 (0b111).

def mul_gf2(a, b):
    """GF(2^2) 中的乘法，结果使用不可约多项式模 x^2 + x + 1."""
    res = 0
    while b > 0:
        if b & 1:
            res ^= a
        a <<= 1
        if a & 0b100:  # 检查 a 是否超出 2 位（即 x^2 的系数位）
            a ^= LAMBDA_GF2  # 当 a 超出 2 位时，需要模掉 x^2
        b >>= 1
    return res

# GF(2^2) 中的逆元（直接求逆）
def inv_gf2(a):
    """GF(2^2) 中的逆元求解，找到一个 b 使得 a * b = 1."""
    if a == 0:
        raise ZeroDivisionError("0 has no multiplicative inverse")
    for b in range(1, 4):  # GF(2^2) 中的元素从 1 到 3（0 没有逆元）
        if mul_gf2(a, b) == 1:
            return b
    return None

# GF(2^4) 中的加法（在 GF(2^2) 上按位异或）
def add_gf4(a, b):
    return a ^ b

# GF(2^4) 中的乘法，使用不可约多项式 δ(y) = y^4 + y + 1
def mul_gf4(a, b):
    res = 0
    while b:
        if b & 1:
            res ^= a
        a <<= 1
        if a & 0b10000:  # 保持 a 在 GF(2^4) 范围内
            a ^= DELTA
        b >>= 1
    return res

# GF(2^4) 中的逆元
def inv_gf4(a):
    if a == 0:
        raise ZeroDivisionError("0 has no multiplicative inverse")
    for b in range(1, 16):  # 在 GF(2^4) 中遍历所有可能的 b
        if mul_gf4(a, b) == 1:
            return b
    return None

# GF(2^8) 中的逆元
def gf2_8_inv_tower(a):
    """使用塔式域方法计算 GF(2^8) 中元素的逆元."""
    """使用塔式域方法计算 GF(2^8) 中元素的逆元."""
    if a == 0:
        raise ZeroDivisionError("0 has no multiplicative inverse")

    # 将 GF(2^8) 中的元素 a 拆解为 GF(2^4) 中的 (a1, a0) 形式
    a0 = a & 0xF  # 低 4 位
    a1 = (a >> 4) & 0xF  # 高 4 位
    print(a0,a1)

    # 1. 计算 GF(2^4) 中 a0 和 a1 的范数 norm = a1^2 + δ * a0^2
    a0_sq = mul_gf4(a0, a0)
    a1_sq = mul_gf4(a1, a1)
    norm = add_gf4(a1_sq, a0_sq)  # 范数 = a1^2 + a0^2

    # 2. 计算范数的逆元（在 GF(2^4) 中）
    norm_inv = inv_gf4(norm)

    # 3. 计算 GF(2^8) 中的逆元 a_inv = a1 * norm_inv + (a0 * norm_inv) * y
    a0_inv = mul_gf4(a1, norm_inv)
    a1_inv = mul_gf4(a0, norm_inv)

    print(hex(a0_inv << 4) ,hex(a1_inv))

    # 返回逆元 a1_inv + a0_inv * y
    return (a0_inv << 4) | a1_inv


# 验证 GF(2^8) 中元素的逆元是否正确
def verify_gf2_8_inverse(a):
    # 定义 GF(2^8) 的域（使用 AES 标准的不可约多项式 x^8 + x^4 + x^3 + x + 1）
    GF2_8 = galois.GF(2 ** 8, irreducible_poly="x^8 + x^4 + x^3 + x + 1")

    a_inv = gf2_8_inv_tower(a)
    product = GF2_8(a)*GF2_8(a_inv)
    return product == 1, a_inv, product


# GF(2^8) 中的标准乘法，直接在 GF(2^8) 上进行
IRREDUCIBLE_POLY = 0x11B  # x^8 + x^4 + x^3 + x + 1
# GF(2^8) 中的乘法运算（加入调试输出）

def gf2_8_mul(a, b):
    """GF(2^8) 中的乘法，使用标准不可约多项式 x^8 + x^4 + x^3 + x + 1 (0x11B)."""
    res = 0  # 初始化结果为 0
    print(f"Multiplying 0x{a:02X} by 0x{b:02X} in GF(2^8):")  # 调试输出
    while b > 0:  # 当 b 不为 0 时继续迭代
        if b & 1:  # 如果 b 的最低位为 1，则累加当前 a
            res ^= a
        print(f"Intermediate result: 0x{res:02X}, a = 0x{a:02X}, b = 0x{b:02X}")  # 打印中间结果
        a <<= 1  # a 左移一位，相当于乘以 x
        if a & 0x100:  # 检查 a 是否超出 8 位（第 9 位为 1）
            a ^= IRREDUCIBLE_POLY  # 使用不可约多项式模掉最高位
            print(f"After modulo: a = 0x{a:02X}")  # 打印模运算后的 a 值
        b >>= 1  # b 右移一位，相当于除以 x
    print(f"Final result of multiplication: 0x{res:02X}\n")  # 最终乘法结果
    return res

# 验证 GF(2^2) 中的所有乘法和逆元
def test_gf2():
    """测试 GF(2^2) 中所有非零元素的逆元和乘法是否正确."""
    print("Testing GF(2^2)...")
    for a in range(1, 4):  # GF(2^2) 中的非零元素为 1, 2, 3
        a_inv = inv_gf2(a)
        product = mul_gf2(a, a_inv)
        print(f"Element: {a}, Inverse: {a_inv}, a * a_inv = {product} (Expected: 1)")


# 验证 GF(2^4) 中的所有乘法和逆元
def test_gf4():
    """测试 GF(2^4) 中所有非零元素的逆元和乘法是否正确."""
    print("Testing GF(2^4)...")
    for a in range(1, 16):  # GF(2^4) 中的非零元素从 1 到 15
        a_inv = inv_gf4(a)
        product = mul_gf4(a, a_inv)
        print(f"Element: {a}, Inverse: {a_inv}, a * a_inv = {product} (Expected: 1)")

# 运行测试
# test_gf2()
# test_gf4()
# gf2和gf4的运算测试通过

# # 测试 GF(2^8) 中的逆元计算
a = 0x53  # 示例元素
is_correct, a_inv, product = verify_gf2_8_inverse(a)
F = ffield.FField(8, gen=0x11b, useLUT=0)
print(f"GF(2^8) 中 0x{a:02X} 的逆元是: 0x{a_inv:02X}")
print(f"验证结果：{'正确' if is_correct else '错误'}，a * a_inv = {hex(product)}")
print(hex(F.Inverse(a)))