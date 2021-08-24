# ----------------------------------------------------------
# Copyright © 2021 Komorebi660 All rights reserved.
# ----------------------------------------------------------

WRITE_FILE_NAME = 'VerilogTestbenchGen/testbench_module.txt'
READ_FILE_NAME = 'VerilogTestbenchGen/module_port.txt'
TESTBENCH_MODULE_NAME = 'test_'
INST_MODULE_NAME = 'inst_'

f_out = open(WRITE_FILE_NAME, 'w+')
f_out.write('`timescale 1ns / 1ps \n')
f_out.write('/*------------------------------------------------\n')
f_out.write('Testbench file made by VerilogTestbenchGen.py\n')
f_out.write('------------------------------------------------*/\n\n\n')

# generate ports
with open(READ_FILE_NAME, 'r') as f:
    while True:
        line_input = f.readline()
        line_temp = line_input.split()
        # read a empty line doesn't mean the module defination is over.
        if (len(line_temp) == 0):
            continue
        # module is over.
        elif line_temp[0] == ');':
            break

        elif line_temp[0] == 'module':
            if len(line_temp) < 2:
                print("Can not find module name!")
                exit(0)
            # delete '(' in the module name
            module_name = line_temp[1].replace('(', '')
            line_output = 'module '
            line_output += TESTBENCH_MODULE_NAME+module_name
            line_output += '();\n'
            f_out.write(line_output)

        elif line_temp[0] == 'input':
            line_output = 'reg '
            if len(line_temp) < 2:
                print("Can not find input port name!")
                exit(0)
            for i in range(1, len(line_temp)):
                # ignore 'wire' or 'reg'
                if line_temp[i] == 'wire':
                    continue
                elif line_temp[i] == 'reg':
                    continue
                else:
                    # replace ',' to ';' but in case that the last port in the module doesn't have a ','
                    if i == len(line_temp)-1:
                        line_output += ' '+line_temp[i].replace(',', '')
                        line_output += ';'
                    else:
                        line_output += ' '+line_temp[i]
            f_out.write('\n'+line_output)

        elif line_temp[0] == 'output':
            line_output = 'wire'
            if len(line_temp) < 2:
                print("Can not find output port name!")
                exit(0)
            for i in range(1, len(line_temp)):
                # ignore 'wire' or 'reg'
                if line_temp[i] == 'wire':
                    continue
                elif line_temp[i] == 'reg':
                    continue
                else:
                    # replace ',' to ';' but in case that the last port in the module doesn't have a ','
                    if i == len(line_temp)-1:
                        line_output += ' '+line_temp[i].replace(',', '')
                        line_output += ';'
                    else:
                        line_output += ' '+line_temp[i]
            f_out.write('\n'+line_output)

        else:
            continue
f.close()

# generate signals
f_out.write('\n\ninitial\n')
f_out.write('begin\n')
f_out.write('\t\n')
f_out.write('end\n')

# instant module
with open(READ_FILE_NAME, 'r') as f:
    while True:
        line_input = f.readline()
        line_temp = line_input.split()
        # read a empty line doesn't mean the module defination is over.
        if (len(line_temp) == 0):
            continue
        # module is over.
        elif line_temp[0] == ');':
            f_out.write('\n);')
            break

        elif line_temp[0] == 'module':
            if len(line_temp) < 2:
                print("Can not find module name!")
                exit(0)
            # delete '(' in the module name
            module_name = line_temp[1].replace('(', '')
            line_output = module_name+" "
            line_output += INST_MODULE_NAME+module_name
            line_output += '\n('
            f_out.write('\n\n'+line_output)

        elif line_temp[0] == 'input' or line_temp[0] == 'output':
            if len(line_temp) < 2:
                print("Can not find port name!")
                exit(0)
            # get the last word
            line_output = line_temp[len(line_temp)-1]
            # if the last word is ','
            if line_output == ',':
                line_output = line_temp[len(line_temp)-2]
            # if the last letter of the last word is ','
            elif line_output[len(line_output)-1] == ',':
                line_output = line_output.replace(',', '')
                line_output = '\t.'+line_output+'('+line_output+'),'
            else:
                line_output = '\t.'+line_output+'('+line_output+')'
            f_out.write('\n'+line_output)

        else:
            continue
f.close()

f_out.write('\n\nendmodule')

f_out.close()
