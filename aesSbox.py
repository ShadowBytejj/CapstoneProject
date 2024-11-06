from pyfinite import ffield
import random

# 初始化有限域 F_2^8，使用AES的标准多项式 x^8 + x^4 + x^3 + x + 1
F = ffield.FField(8, gen=0x11b, useLUT=0)
print(F.Inverse(3))

# 生成加法共享（Additive Sharing）
def generate_additive_shares(secret):
    share1 = random.randint(0, 255)  # 因为是8比特数字
    share2 = secret ^ share1  # 异或用于分割秘密
    return share1, share2


# 生成Beaver Triple (a, b, c)，满足 c = a * b mod F_2^8
def generate_beaver_triple():
    a = random.randint(1, 255)  # 1到255的随机数
    b = random.randint(1, 255)
    c = F.Multiply(a, b)
    return (a, b, c)


# 计算S-box的仿射变换
def affine_transformation(input_byte):
    # 仿射变换矩阵和常量
    A = [
        [1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1]
    ]
    c = 0x63  # 仿射变换中的常量

    # 计算仿射变换
    output = 0
    for i in range(8):
        bit = 0
        for j in range(8):
            bit ^= ((input_byte >> j) & 1) * A[i][j]
        output |= ((bit ^ ((c >> i) & 1)) << i)

    return output


# 使用MPC计算AES S-box
def mpc_aes_sbox(input_byte):
    if input_byte == 0:
        return 0  # 0 的逆元为 0

    # 计算有限域上的逆元
    inv_byte = F.Inverse(input_byte) # 8 bits inverse, 4 bits (3 multiplication + 1 inverse)
    print(bin(input_byte))
    print(bin(inv_byte))
    # 使用MPC安全计算仿射变换
    output_byte = affine_transformation(inv_byte) # x0 + x1 = x, x0[0] \oplus ^ x1[0] = x[0]

    return output_byte


# 测试MPC S-box计算
input_byte = 0x53  # 例如输入 0x53
result = mpc_aes_sbox(input_byte)
print(f"S-box result for input {hex(input_byte)} using MPC: {hex(result)}")


# 1. Additive secret sharing -> finite fields F_{2^8}, x = b8||b7||...||b1, x0 + x1 = x, x0=b80||b70||...||b10, x1 = b81||b71||...||b11, x0 ^ x1 = x
# 2. Beavers'triple (a,b,c) same, beaver triple的abc是一样的吗？
# 3. Inverse: tower fields: 8 bits inverse -> 3 个 4 bits multiplition + 1 个 4 bits inverse -> 9 个 2 bits 乘法 + 3 个 2bits的乘法 + 2 bit的inverse.
#                       1. 2 bits的乘法.



# 4. bits上的arithmetic garbling -> Sbox. ()
# 5. look-up table. 256 元素，8bits。


#task 1：complete additive secret sharing using finite files F_{2^8}
#task 2: apply F_{2^8} secret sharing in beaver triple


#task 3: complete inverse on finite field with tower fields

#task 4: complete arithmetic garbling for bit

#task 5: complete look-table

#task 6:https://crypto.stackexchange.com/questions/41651/what-are-the-ways-to-generate-beaver-triples-for-multiplication-gate