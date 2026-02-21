# by Abdalrahim Sawalha   211081



def pass1(source_file_path,optab_file_path,intermediate_file_path):


    symbol_table = {}

    opcode_table = {}
    program_name = ""
    program_length = 0
    start_address = 0
    error_flag = False

    assembler_directives = ["START","END","BYTE","WORD","RESB","RESW"]



    # loading OPTAB file
    with open(optab_file_path, "r", encoding="utf-8-sig") as optab_file:

        for line in optab_file:
            tokens = line.strip().split()
            if tokens:
                opcode_table[tokens[0]] = 3  # every SIC instructions is 3 byte



    with open(source_file_path, "r", encoding="utf-8-sig") as source_file, open(intermediate_file_path, "w") as intermediate_file:


        lines = source_file.readlines()
        index = 0

        # skip coment in start
        while index < len(lines) and lines[index].strip().startswith("."):
            index += 1

        LOCCTR = 0


        # check if start exist
        if index < len(lines):

            first_line = lines[index].rstrip('\n')
            label = first_line[0:10].strip()
            opcode = first_line[11:20].strip()
            operand = first_line[21:39].strip()

            if opcode == "START":
                program_name = label
                start_address = int(operand,16)
                LOCCTR = start_address

                # add the program label inside the symbol_table
                if label:
                    if label in symbol_table:
                        error_flag = True
                        print(f"[Error] Duplicate label found: '{label}'")
                    else:
                        symbol_table[label] = LOCCTR

                intermediate_file.write(f"{LOCCTR:04X}  {first_line}\n")
                index += 1




        # now process other lines
        while index < len(lines):
            line = lines[index].rstrip('\n')
            index += 1

            if line.strip() == '' or line.strip().startswith('.'):
                continue  # skip empty or coment line

            label = line[0:10].strip()
            opcode = line[11:20].strip()
            operand = line[21:39].strip()


            # if have label, add to table
            if label:
                if label in symbol_table:
                    error_flag = True
                    print(f"[Error] Duplicate label found: '{label}'")
                else:
                    symbol_table[label] = LOCCTR



            # write it to intermed file
            intermediate_file.write(f"{LOCCTR:04X}  {line}\n")



            # check if opcode is valid
            clean_operand = operand.rstrip(",X") if ",X" in operand else operand  

            if opcode in opcode_table:
                LOCCTR += 3
            elif opcode in assembler_directives:
                if opcode == "WORD":
                    LOCCTR += 3
                elif opcode == "RESW":
                    LOCCTR += 3 * int(operand)
                elif opcode == "RESB":
                    LOCCTR += int(operand)
                elif opcode == "BYTE":
                    if operand.startswith("C'") and operand.endswith("'"):
                        LOCCTR += len(operand) - 3
                    elif operand.startswith("X'") and operand.endswith("'"):
                        LOCCTR += (len(operand) - 3) // 2
                    else:
                        error_flag = True
                        print(f"[Error] Invalid BYTE operand format: '{operand}'")
                elif opcode == "END":
                    break
            else:
                error_flag = True
                print(f"[Error] Unrecognized opcode: '{opcode}'")

        program_length = LOCCTR - start_address


    # print symbol table after finish
    print("\n========== Symbol Table ==========")
    for symbol, address in symbol_table.items():
        print(f"{symbol:<12} -> Address: {address:04X}")



    # print program informations
    print("\n========== Program Information ==========")
    print(f"Program Name   : {program_name}")
    print(f"Start Address  : {start_address:04X}")
    print(f"Program Length : {program_length:04X}")



    with open("symbol_table.symtab", "w") as symtab_file:
        symtab_file.write(f"ProgramName {program_name}\n")
        symtab_file.write(f"StartAddress {start_address:04X}\n")
        symtab_file.write(f"ProgramLength {program_length:04X}\n")
        for symbol, address in symbol_table.items():
            symtab_file.write(f"{symbol} {address:04X}\n")


pass1("source.asm","OPTAB.txt","intermed_file.mdt")
