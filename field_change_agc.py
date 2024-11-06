import logging
import random as rm
from pyfinite import ffield
import numpy as np

class MixedCircuits:
    def __init__(self):
        self.num_of_levels = 0
        self.number_of_wires = 0
        self.number_of_gates = 0
        self.wires = []
        self.gates = []
        self.wire_labels = []
        self.outputs_bits = []


def convert_sbox(file_loc: str, file_output: str):
    file = open(file_loc)
    file_r = file.readlines()
    info_ = file_r[1]
    info_ = info_.split(' ')
    number_of_gate = int(info_[0])
    wire_label = [8, 8, 8, 8]
    wires = ["X", "Y", "R0", "R1"]
    wires.extend(["x" + str(i) for i in range(8)])
    wire_label.extend([2 for i in range(8)])
    wires.extend(["y" + str(i) for i in range(8)])
    wire_label.extend([2 for i in range(8)])

    wires.extend(["T" + str(i + 1) for i in range(6)])
    wire_label.extend([8 for i in range(6)])
    wires.extend(["t" + str(i) for i in range(15)])
    wire_label.extend([2 for i in range(15)])
    file_w = open(file_output, "w")
    file_w.write(str(wire_label)[1:-1] + "\n")
    for i in range(4, 4 + number_of_gate):
        gate_i = file_r[i].split(' ')

        if gate_i[0] == "INV" or gate_i[0] == "INV_8":
            output_i = wires.index(gate_i[1])
            input_i1 = wires.index(gate_i[2][0:-1])
            write_str = "1 1 " + str(input_i1) + " " + str(output_i) + " " + gate_i[0] + "\n"
        else:
            output_i = wires.index(gate_i[1])
            input_i1 = wires.index(gate_i[2])
            input_i2 = wires.index(gate_i[3][0:-1])
            write_str = "2 1 " + str(input_i1) + " " + str(input_i2) + " " + str(output_i) + " " + gate_i[0] + "\n"

        file_w.write(write_str)
        print(file_r[i])

    file_w.close()


def construct_mixed_circuits(circuit, tl, ts, exp):
    if not isinstance(circuit, MixedCircuits):
        raise TypeError("The circuit should be <MixedCircuits>.")
    table_random = []
    A_table = [[] for i in range(circuit.number_of_wires)]
    B_table = [[] for i in range(circuit.number_of_wires)]

    A_table[25] = [[1]]
    B_table[25] = [[0]]

    for i in range(circuit.number_of_gates-1, -1, -1):
        gate_ = circuit.gates[i]

        A_output = A_table[gate_[4]]
        B_output = B_table[gate_[4]]
        #print(i)
        field = ffield.FField(exp)
        if gate_[5] == 'MUL_8':
            T = tl
            for jth_output in range(len(A_output)):
                A_output_jth = A_output[jth_output]
                B_output_jth = B_output[jth_output]
                A_input1_new = []
                A_input2_new = []
                B_input1_new = []
                B_input2_new = []
                print(len(A_output_jth))
                for i_jth_output in range(len(A_output_jth)):
                    r_1 = rm.randint(0, T - 1)
                    r_2 = rm.randint(0, T - 1)
                    r_3 = rm.randint(0, T - 1)
                    table_random.append([r_1, r_2, r_3])

                    A_output_j = A_output_jth[i_jth_output]
                    B_output_j = B_output_jth[i_jth_output]

                    A_input1_new_2j = A_output_j
                    A_input1_new_2jp1 = field.Multiply(r_1, A_output_j)
                    B_input1_new_2j = field.Multiply(r_2, A_output_j)
                    t_1 = field.Multiply(r_1, B_input1_new_2j)
                    t_2 = field.Add(r_3, t_1)
                    field.Add(t_2, B_output_j)
                    B_input1_new_2jp1 = field.Add(t_2, B_output_j)
                    A_input1_new.extend([A_input1_new_2j, A_input1_new_2jp1])
                    B_input1_new.extend([B_input1_new_2j, B_input1_new_2jp1])

                    A_input2_new_2j = 1
                    A_input2_new_2jp1 = field.Multiply(r_2, A_output_j)
                    B_input2_new_2j = r_1
                    B_input2_new_2jp1 = r_3
                    A_input2_new.extend([A_input2_new_2j, A_input2_new_2jp1])
                    B_input2_new.extend([B_input2_new_2j, B_input2_new_2jp1])
                A_table[gate_[2]].append(A_input1_new)
                A_table[gate_[3]].append(A_input2_new)
                B_table[gate_[2]].append(B_input1_new)
                B_table[gate_[3]].append(B_input2_new)

        elif gate_[5] == 'ADD_8':
            T = tl
            for jth_output in range(len(A_output)):

                A_output_jth = A_output[jth_output]
                B_output_jth = B_output[jth_output]
                A_input1_new = []
                A_input2_new = []
                B_input1_new = []
                B_input2_new = []
                for i_jth_output in range(len(A_output_jth)):
                    rv = rm.randint(0, T - 1)
                    table_random.append([rv])
                    A_output_j = A_output_jth[i_jth_output]
                    B_output_j = B_output_jth[i_jth_output]

                    A_input1_new_j = A_output_j
                    B_input1_new_j = field.Add(rv, B_output_j)
                    A_input1_new.extend([A_input1_new_j])
                    B_input1_new.extend([B_input1_new_j])

                    A_input2_new_j = A_output_j
                    B_input2_new_j = rv
                    A_input2_new.extend([A_input2_new_j])
                    B_input2_new.extend([B_input2_new_j])
                A_table[gate_[2]].append(A_input1_new)
                A_table[gate_[3]].append(A_input2_new)
                B_table[gate_[2]].append(B_input1_new)
                B_table[gate_[3]].append(B_input2_new)

        elif gate_[5] == 'MIX_MUL':
            for jth_output in range(len(A_output)):
                A_output_jth = A_output[jth_output]
                B_output_jth = B_output[jth_output]
                A_input1_new = []
                A_input2_new = []
                B_input1_new = []
                B_input2_new = []
                print(len(A_output_jth))
                out_all = len(A_output_jth)
                if isinstance(A_output_jth[-1], list):
                    out_all = out_all - 1
                for i_jth_output in range(out_all):
                    r_1s = rm.randint(0, ts - 1)
                    r_2 = rm.randint(0, tl - 1)
                    r_3 = rm.randint(0, tl - 1)
                    table_random.append([r_1s, r_2, r_3])

                    A_output_j = A_output_jth[i_jth_output]
                    B_output_j = B_output_jth[i_jth_output]

                    A_input1_new_2j = A_output_j
                    A_input1_new_2jp1 = field.Multiply(r_1s, A_output_j)
                    B_input1_new_2j = field.Multiply(r_2, A_output_j)
                    t_1 = field.Multiply(r_1s, B_input1_new_2j)
                    t_2 = field.Add(r_3, t_1)
                    field.Add(t_2, B_output_j)
                    B_input1_new_2jp1 = field.Add(t_2, B_output_j)
                    A_input1_new.extend([A_input1_new_2j, A_input1_new_2jp1])
                    B_input1_new.extend([B_input1_new_2j, B_input1_new_2jp1])

                    A_input2_new_2j = 1
                    A_input2_new_2jp1 = field.Multiply(r_2, A_output_j)
                    B_input2_new_2j = r_1s
                    B_input2_new_2jp1 = r_3
                    A_input2_new.extend([A_input2_new_2j, A_input2_new_2jp1])
                    B_input2_new.extend([B_input2_new_2j, B_input2_new_2jp1])

                A_input2_new.append([0, 1])
                B_input2_new.append([0, 1])
                if circuit.wire_labels[gate_[2]] == 8:
                    A_table[gate_[2]].append(A_input1_new)
                    A_table[gate_[3]].append(A_input2_new)
                    B_table[gate_[2]].append(B_input1_new)
                    B_table[gate_[3]].append(B_input2_new)
                else:
                    A_table[gate_[3]].append(A_input1_new)
                    A_table[gate_[2]].append(A_input2_new)
                    B_table[gate_[3]].append(B_input1_new)
                    B_table[gate_[2]].append(B_input2_new)

        elif gate_[5] == "AND" or gate_[5] == "XOR":
            for jth_output in range(len(A_output)):
                A_output_jth = A_output[jth_output]
                B_output_jth = B_output[jth_output]
                A_input1_new = []
                A_input2_new = []
                B_input1_new = []
                B_input2_new = []
                print(len(A_output_jth))
                out_all = len(A_output_jth)
                control1_new = []
                control2_new = []
                if isinstance(A_output_jth[-1], list):
                    out_all = out_all - 1
                    control_list = A_output_jth[-1]
                else:
                    control_list = [0 for i in range(out_all)]

                if gate_[5] == "AND":
                    for i_jth_output in range(out_all):
                        if control_list[i_jth_output] == 0:
                            control1_new.extend([0, 0])
                            control2_new.extend([0, 0])
                            r_1 = rm.randint(0, ts - 1)
                            r_2 = rm.randint(0, ts - 1)
                            r_3 = rm.randint(0, ts - 1)
                            table_random.append([r_1, r_2, r_3])

                            A_output_j = A_output_jth[i_jth_output]
                            B_output_j = B_output_jth[i_jth_output]

                            A_input1_new_2j = A_output_j % ts
                            A_input1_new_2jp1 = (r_1 * A_output_j) % ts
                            B_input1_new_2j = (-r_2 * A_output_j) % ts
                            B_input1_new_2jp1 = (r_3 - r_1 * r_2 * A_output_j + B_output_j) % ts
                            A_input1_new.extend([A_input1_new_2j, A_input1_new_2jp1])
                            B_input1_new.extend([B_input1_new_2j, B_input1_new_2jp1])

                            A_input2_new_2j = 1
                            A_input2_new_2jp1 = (r_2 * A_output_j) % ts
                            B_input2_new_2j = (-r_1) % ts
                            B_input2_new_2jp1 = (-r_3) % ts
                            A_input2_new.extend([A_input2_new_2j, A_input2_new_2jp1])
                            B_input2_new.extend([B_input2_new_2j, B_input2_new_2jp1])
                        else:
                            control1_new.extend([1, 1])
                            control2_new.extend([0, 1])
                            r_1s = rm.randint(0, ts - 1)
                            r_2s = rm.randint(0, ts - 1)
                            r_3 = rm.randint(0, tl - 1)
                            table_random.append([r_1s, r_2s, r_3])

                            A_output_j = A_output_jth[i_jth_output]
                            B_output_j = B_output_jth[i_jth_output]

                            A_input1_new_2j = A_output_j
                            A_input1_new_2jp1 = field.Multiply(r_1s, A_output_j)
                            B_input1_new_2j = field.Multiply(r_2s, A_output_j)
                            t_1 = field.Multiply(r_1s, B_input1_new_2j)
                            t_2 = field.Add(r_3, t_1)
                            field.Add(t_2, B_output_j)
                            B_input1_new_2jp1 = field.Add(t_2, B_output_j)
                            A_input1_new.extend([A_input1_new_2j, A_input1_new_2jp1])
                            B_input1_new.extend([B_input1_new_2j, B_input1_new_2jp1])

                            A_input2_new_2j = 1
                            A_input2_new_2jp1 = field.Multiply(r_2s, A_output_j)
                            B_input2_new_2j = r_1s
                            B_input2_new_2jp1 = r_3
                            A_input2_new.extend([A_input2_new_2j, A_input2_new_2jp1])
                            B_input2_new.extend([B_input2_new_2j, B_input2_new_2jp1])


                else:
                    for i_jth_output in range(out_all):
                        if control_list[i_jth_output] == 0:
                            control1_new.extend([0])
                            control2_new.extend([0])
                            rv = rm.randint(0, ts - 1)
                            table_random.append([rv])

                            A_output_j = A_output_jth[i_jth_output]
                            B_output_j = B_output_jth[i_jth_output]

                            A_input1_new_j = A_output_j % ts
                            B_input1_new_j = (-rv + B_output_j) % ts
                            if gate_[5] == "NXOR":
                                B_input1_new_j = (B_input1_new_j + A_input1_new_j) % ts
                            A_input1_new.extend([A_input1_new_j])
                            B_input1_new.extend([B_input1_new_j])

                            A_input2_new_j = A_output_j % ts
                            B_input2_new_j = rv % ts
                            A_input2_new.extend([A_input2_new_j])
                            B_input2_new.extend([B_input2_new_j])
                        else:
                            control1_new.extend([1])
                            control2_new.extend([1])
                            rv = rm.randint(0, tl - 1)
                            table_random.append([rv])

                            A_output_j = A_output_jth[i_jth_output]
                            B_output_j = B_output_jth[i_jth_output]

                            A_input1_new_j = A_output_j
                            B_input1_new_j = field.Add(rv, B_output_j)
                            if gate_[5] == "NXOR":
                                B_input1_new_j = field.Add(B_input1_new_j, A_input1_new_j)
                            A_input1_new.extend([A_input1_new_j])
                            B_input1_new.extend([B_input1_new_j])

                            A_input2_new_j = A_output_j
                            B_input2_new_j = rv
                            A_input2_new.extend([A_input2_new_j])
                            B_input2_new.extend([B_input2_new_j])

                A_input1_new.append(control1_new)
                B_input1_new.append(control1_new)
                A_input2_new.append(control2_new)
                B_input2_new.append(control2_new)

                A_table[gate_[2]].append(A_input1_new)
                A_table[gate_[3]].append(A_input2_new)
                B_table[gate_[2]].append(B_input1_new)
                B_table[gate_[3]].append(B_input2_new)

    return A_table, B_table, table_random



def execute_garbling_circuits(circuit, tables, inputs_values, input_wire, exp):
    if not isinstance(circuit, MixedCircuits):
        raise TypeError("The circuit should be <ArithmeticCircuits>.")
    wire_values = [[] for i in range(circuit.number_of_wires)]
    A_table = tables[0]
    B_table = tables[1]
    r_table = tables[2]
    field = ffield.FField(exp)
    wire_values_copy = [[] for i in range(circuit.number_of_wires)]
    print("input_wire",inputs_values)
    for i in range(len(input_wire)):
        wire_value_i = inputs_values[i]
        wire_index = input_wire[i]
        wire_values_i = []
        A_input1 = A_table[wire_index]
        B_input1 = B_table[wire_index]
        for j in range(len(A_input1)):
            A_input1j = A_input1[j]
            B_input1j = B_input1[j]
            output_j = []

            if len(A_input1j) == 1:
                if circuit.wire_labels[wire_index] == 2:
                    output_j.append((A_input1j[0] & wire_value_i) ^ B_input1j[0])
                if circuit.wire_labels[wire_index] == 8:
                    output_j.append(field.Add(field.Multiply(A_input1j[0], wire_value_i), B_input1j[0]))
            else:
                if isinstance(A_input1j[-1], list):
                    control_list = A_input1j[-1]
                else:
                    control_list = [0 for i in range(len(A_input1j))]
                for k in range((len(A_input1j) // 2)):
                    t_1 = field.Add(field.Multiply(A_input1j[k * 2], wire_value_i), B_input1j[k * 2])
                    t_2 = field.Add(field.Multiply(A_input1j[k * 2 + 1], wire_value_i), B_input1j[k * 2 + 1])
                    output_j.extend([t_1, t_2])
            wire_values_i.append(output_j)
        wire_values[wire_index] = wire_values_i

    for i in range(40):
        wire_values_copy[i] = wire_values[i]
    print(wire_values)


    for i in range(circuit.number_of_gates):
        print(f"circuite.gates[i] : {circuit.gates[i]}")
        gate_i = circuit.gates[i]
        input_index1 = gate_i[2]
        input_index2 = gate_i[3]
        output_index = gate_i[4]
        input_wire1 = wire_values[input_index1]
        input_wire2 = wire_values[input_index2]

        output_i = []
        print("input_wire1",input_wire1)
        if gate_i[5] == "ADD_8" or gate_i[5] == "XOR":
            input_wire1_j = input_wire1[-1]
            input_wire2_j = input_wire2[-1]
            output_i_j = []
            for kth in range(len(input_wire1_j)):
                output_i_j.append(field.Add(input_wire1_j[kth], input_wire2_j[kth]))
            output_i.append(output_i_j)

        elif gate_i[5] == "MUL_8" or gate_i[5] == "AND" or gate_i[5] == "MIX_MUL":
            input_wire1_j = input_wire1[-1]
            input_wire2_j = input_wire2[-1]
            output_i_j = []
            if len(input_wire1_j) % 2 == 0:
                for kth in range(len(input_wire1_j) // 2):
                    t_1 = input_wire1_j[kth * 2]
                    t_2 = input_wire1_j[kth * 2 + 1]
                    t_3 = input_wire2_j[kth * 2]
                    t_4 = input_wire2_j[kth * 2 + 1]
                    output_i_j.append(field.Add(field.Add(field.Multiply(t_1, t_3), t_2), t_4))

            output_i.append(output_i_j)
        wire_values[output_index] = output_i
        wire_values[input_index1] = wire_values[input_index1][0:-1]
        wire_values[input_index2] = wire_values[input_index2][0:-1]
    return wire_values


def expansion(x):
    if not isinstance(x, list):
        raise TypeError("x should be a list with 0s, 1s")
    res1 = []
    res2 = []
    for i in range(len(x)):
        if x[i] == 0:
            res1.extend([0, 0])
            res2.extend([0, 0])
        else:
            res1.extend([1, 1])
            res2.extend([1, 0])

    return res1, res2


def expan_for_n(n):
    x_b = [0, 1]
    mid_res = [x_b]
    mid_res_ = []
    for ith_a in range(n):
        for jth_a in range(len(mid_res)):
            x_now = mid_res[jth_a]
            ac, bc = expansion(x_now)
            mid_res_.append(ac)
            mid_res_.append(bc)

        mid_res = mid_res_.copy()
        mid_res_ = []
    return np.array(mid_res)




if __name__ == "__main__":
    convert_sbox("sbox_mixed.txt", "sbox_mixed_T.txt")
    circuits_file = open("sbox_mixed_T.txt")
    circuits_file_r = circuits_file.readlines()
    wire_labels = circuits_file_r[0].split(', ')
    wire_labels[-1] = wire_labels[-1][0:-1]
    for ith in range(len(wire_labels)):
        wire_labels[ith] = int(wire_labels[ith])
    gates = []
    for ith in range(1, len(circuits_file_r)):
        gate_1 = circuits_file_r[ith].split(' ')
        gate_1[-1] = gate_1[-1][0:-1]
        for j in range(len(gate_1)-1):
            gate_1[j] = int(gate_1[j])
        gates.append(gate_1)
    sbox = MixedCircuits()
    sbox.wires = [i for i in range(len(wire_labels))]
    sbox.wire_labels = wire_labels
    sbox.gates = gates
    sbox.number_of_gates = len(sbox.gates)
    sbox.number_of_wires = len(sbox.wires)
    sbox.outputs_bits = [1]
    a, b, c = construct_mixed_circuits(sbox, 2**8, 2, 8)
    wire_inputs = [1, 19, 17, 21, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    wire_inputs_label = [i for i in range(20)]
    w = execute_garbling_circuits(sbox, [a, b, c], wire_inputs, wire_inputs_label, 8)

    total_bits = []
    n_bit = 0
    for i in range(20):
        bit_i = 0
        if sbox.wire_labels[i] == 2:
            for j in range(len(a[i])):
                if isinstance(a[i][j][-1], list):
                    control_list = b[i][j][-1]
                    ln = len(a[i][j]) - 1
                else:
                    control_list = [0 for i in range(len(b[i][j]))]
                    ln = len(b[i][j])
                for k in range(ln):
                    if control_list[k]:
                        bit_i += 8
                    else:
                        bit_i += 1
        else:
            for j in range(len(a[i])):
                for k in range(len(a[i][j])):
                    bit_i += 8
        total_bits.append(bit_i)
        n_bit += bit_i
    print(w[25])
    print(total_bits)
    print(n_bit)

