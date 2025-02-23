def ConvertBin(decimal, maxSize):
    aux = ''
    if decimal < 0:
        aux = bin(decimal + 1)[3:]
        size = len(aux)
        aux = '0' * (maxSize - size) + aux if size < maxSize else aux
        aux = ''.join('1' if bit == '0' else '0' for bit in aux)
    else:
        aux = bin(decimal)[2:]
        size = len(aux)
        aux = '0' * (maxSize - size) + aux if size < maxSize else aux
    return aux

def ConvertToMachineCode(opr, file, writeToFile, assembly, index):
    instr_map = {
        "add": ("0000000", "000", "0110011"),
        "addi": (None, "000", "0010011"),
        "lw": (None, "010", "0000011"),
        "sw": (None, "010", "0100011"),
        "bne": (None, "001", "1100111"),
        "xor": ("0000000", "100", "0110011"),
        "sll": ("0000000", "001", "0110011")
    }
    funct7, funct3, opcode = instr_map.get(opr, (None, None, None))
    
    if opr in {"add", "xor", "sll"}:
        rs2 = ConvertBin(int(assembly[index][3][1:]), 5)
        rs1 = ConvertBin(int(assembly[index][2][1:]), 5)
        rd = ConvertBin(int(assembly[index][1][1:]), 5)
        machine_code = f"{funct7}{rs2}{rs1}{funct3}{rd}{opcode}"
    elif opr in {"addi", "lw"}:
        imm = ConvertBin(int(assembly[index][3]), 12)
        rs1 = ConvertBin(int(assembly[index][2][1:]), 5)
        rd = ConvertBin(int(assembly[index][1][1:]), 5)
        machine_code = f"{imm}{rs1}{funct3}{rd}{opcode}"
    elif opr == "sw":
        imm_bin = ConvertBin(int(assembly[index][2]), 12)
        imm1, imm2 = imm_bin[:7], imm_bin[7:]
        rs2 = ConvertBin(int(assembly[index][3][1:]), 5)
        rs1 = ConvertBin(int(assembly[index][1][1:]), 5)
        machine_code = f"{imm1}{rs1}{rs2}{funct3}{imm2}{opcode}"
    elif opr == "bne":
        imm_bin = ConvertBin(int(assembly[index][3]), 12)
        imm1, imm2, imm3, imm4 = imm_bin[0], imm_bin[2:8], imm_bin[8:12], imm_bin[1]
        rs1 = ConvertBin(int(assembly[index][1][1:]), 5)
        rs2 = ConvertBin(int(assembly[index][2][1:]), 5)
        machine_code = f"{imm1}{imm2}{rs2}{rs1}{funct3}{imm3}{imm4}{opcode}"
    
    if writeToFile:
        file.write(machine_code + '\n')
    else:
        print(machine_code)

def process_assembly(input_file, output_file=None):
    with open(input_file, 'r') as file:
        assembly = [line.replace(',', '').replace('\n', '').replace('(', ' ').replace(')', '').split() for line in file]
        
        file = open(output_file, 'w') if output_file else None
        for index, instruction in enumerate(assembly):
            ConvertToMachineCode(instruction[0], file, bool(output_file), assembly, index)
        
        if output_file:
            file.close()
