# by Abdalrahim Sawalha 211081



def pass2(intermediate_file_path,optab_file_path, symbol_table_path,object_file_path, listing_file_path):

    # load OPTAB from file
    opcode_table = {}


    with open(optab_file_path, "r",encoding="utf-8-sig") as optab_file:
        for line in optab_file:
            tokens = line.strip().split()
            if tokens:
                opcode_table[tokens[0]] = tokens[1]
                
    # now load Symbol Table and program info
    symbol_table = {}



    with open(symbol_table_path, "r") as symtab_file:
        lines = symtab_file.readlines()
        program_name = lines[0].split()[1]
        start_address = int(lines[1].split()[1],16)
        program_length = int(lines[2].split()[1], 16)
        
        for line in lines[3:]:
            parts = line.strip().split()
            if len(parts) >= 2:
                symbol_table[parts[0]] = int(parts[1],16)



    with open(intermediate_file_path, "r") as inter_file, \
         open(object_file_path, "w") as obj_file, \
         open(listing_file_path, "w") as lst_file:
        

        # write Header Record first
        obj_file.write(f"H^{program_name}^{start_address:06X}^{program_length:06X}\n")
        

        text_records = []
        current_record = ""
        current_record_start = None
        current_record_length = 0
        


        lines = inter_file.readlines()
        for line in lines:
            if line.strip() == '' or line.strip().startswith('.'):
                continue



            loc = int(line[0:4], 16)
            label = line[6:16].strip()
            opcode = line[17:26].strip()
            operand = line[27:].strip()
            operand = operand.split('.')[0].strip()
            obj_code = ""


            if opcode in opcode_table:

                code = opcode_table[opcode]
                if operand != "":
                    if ",X" in operand:
                        operand = operand.replace(",X", "")
                        address_part = symbol_table[operand] + 0x8000
                    else:
                        address_part = symbol_table[operand]
                    obj_code = f"{code}{address_part:04X}"
                else:
                    obj_code = f"{code}0000"
                    

            elif opcode == "WORD":
                obj_code = f"{int(operand):06X}"



            elif opcode == "BYTE":
                if operand.startswith("C'") and operand.endswith("'"):
                    chars = operand[2:-1]
                    obj_code = ''.join([f"{ord(c):02X}" for c in chars])
                elif operand.startswith("X'") and operand.endswith("'"):
                    obj_code = operand[2:-1]
                    
            

            lst_file.write(f"{loc:04X}\t{label:<10}{opcode:<10}{operand:<15}{obj_code}\n")


            if obj_code:

                if current_record_start is None:
                    current_record_start = loc
                if (current_record_length + len(obj_code) // 2) > 30:
                    
                    obj_file.write(f"T^{current_record_start:06X}^{current_record_length:02X}^{current_record}\n")
                    current_record = ""
                    current_record_start = loc
                    current_record_length = 0
                if current_record != "":
                    current_record += "^"
                current_record += obj_code
                current_record_length += len(obj_code) // 2


            if opcode == "END":
                break



        # last text record must write
        if current_record:
            obj_file.write(f"T^{current_record_start:06X}^{current_record_length:02X}^{current_record}\n")


        # write END Record finaly
        obj_file.write(f"E^{start_address:06X}\n")



pass2(
    "intermed_file.mdt",
    "OPTAB.txt",
    "symbol_table.symtab",
    "output.obj",
    "listing.lst"
)

