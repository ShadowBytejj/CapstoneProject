import numpy as np

# 定义有限域GF(2^8)的不可约多项式
IRREDUCIBLE_POLY = 0b100011011  # x^8 + x^4 + x^3 + x + 1

def gf_add(a, b):
    """在GF(2^8)上执行加法（异或运算）"""
    return a ^ b

def gf_mult(a, b):
    """在GF(2^8)上执行乘法"""
    result = 0
    while b > 0:
        if b & 1:  # 如果b的最低位为1
            result ^= a  # 加法是异或
        a <<= 1  # 左移一位
        if a & 0x100 or a>=256:  # 如果a超过8位
            a ^= IRREDUCIBLE_POLY  # 对不可约多项式取模
        b >>= 1  # 右移一位
    return result

def additive_sharing(value, num_shares):
    """在GF(2^8)上执行加法共享"""
    # 确保值在GF(2^8)范围内
    if value < 0 or value >= 256:
        raise ValueError("Value must be in the range [0, 255]")

    # 创建随机共享
    shares = np.random.randint(0, 256, num_shares - 1, dtype=np.uint8)

    # 计算最后一个共享
    last_share = value
    for share in shares:
        last_share = gf_add(last_share, share)

    shares = np.append(shares, last_share)
    return shares


def recover_value(shares):
    """从共享中恢复原始值，并检查共享的和"""
    value = 0
    for share in shares:
        value = gf_add(value, share)

    print("共享的和:", value)  # 输出共享的和
    return value

def display_binary_shares(shares):
    """以二进制形式展示共享值"""
    binary_shares = [format(share, '08b') for share in shares]  # 以8位二进制表示
    return binary_shares

# 示例
value = 22  # 要共享的值
num_shares = 4

shares = additive_sharing(value, num_shares)
print("生成的共享:", shares)

# 展示共享值的二进制形式
binary_shares = display_binary_shares(shares)
print("共享值的二进制形式:", binary_shares)

recovered_value = recover_value(shares)
print("恢复的值:", recovered_value)
