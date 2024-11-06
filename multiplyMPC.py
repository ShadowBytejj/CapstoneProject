import random
import galois

# 创建 GF(2^8) 的有限域
GF256 = galois.GF(2**8)  # 定义基于不可约多项式 x^8 + x^4 + x^3 + x + 1 的有限域

def generate_additive_shares(secret):
    """在 GF(2^8) 中生成加法共享"""
    # 生成一个随机共享值
    share1 = GF256(random.randint(0, 255))
    # 第二个共享值确保 share1 + share2 = secret
    share2 = GF256(secret) - share1
    return share1, share2

def generate_beaver_triple():
    """生成 Beaver Triple (a, b, c)，满足 c = a * b"""
    a = GF256(random.randint(0, 255))
    b = GF256(random.randint(0, 255))
    c = a * b
    return a, b, c

def mpc_multiply(x, y):
    """使用 MPC 的 Beaver Triple 计算 x * y"""
    # 参与方 A 和 B 分别持有 x 和 y 的加法共享
    x1, x2 = generate_additive_shares(x)
    y1, y2 = generate_additive_shares(y)

    # 生成一个 Beaver Triple (a, b, c)，并给 A 和 B 各分配共享
    a, b, c = generate_beaver_triple()
    a1, a2 = generate_additive_shares(a)
    b1, b2 = generate_additive_shares(b)
    c1, c2 = generate_additive_shares(c)

    print(f"Beaver Triple: a={a}, b={b}, c={c} (expected c = a * b = {a * b})")
    print(f"Shares: x1={x1}, x2={x2}, y1={y1}, y2={y2}")
    print(f"Shared values: a1={a1}, a2={a2}, b1={b1}, b2={b2}, c1={c1}, c2={c2}")

    # 计算 d 和 e 的共享
    d1 = x1 - a1
    d2 = x2 - a2
    e1 = y1 - b1
    e2 = y2 - b2

    # 参与方分别公开 d 和 e 的共享部分
    d = d1 + d2
    e = e1 + e2

    print(f"Calculated shares: d={d}, e={e}")

    # 计算 z 的共享
    z1 = c1 + d * b1 + e * a1 + d * e
    z2 = c2 + d * b2 + e * a2

    # 返回乘积结果的共享部分
    return z1 + z2

# 输入两个数字
x = 11
y = 3

# 计算 MPC 乘法结果
result = mpc_multiply(x, y)
print(f"Multiplication result of {x} and {y} using MPC: {result}")
print(200*34&256)