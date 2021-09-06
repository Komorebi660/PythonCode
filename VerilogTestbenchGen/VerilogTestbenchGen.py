# ----------------------------------------------------------
# coding=utf-8
# Copyright © 2021 Komorebi660 All rights reserved.
# ----------------------------------------------------------

WRITE_FILE_NAME = 'VerilogTestbenchGen/testbench_module.txt'
READ_FILE_NAME = 'VerilogTestbenchGen/module_port.txt'
TESTBENCH_MODULE_NAME = 'test_'
INST_MODULE_NAME = 'inst_'

LINE_LENTH_1 = 20
LINE_LENTH_2 = 15
LINE_LENTH_3 = 30

f_out = open(WRITE_FILE_NAME, 'w+')
f_out.write('`timescale 1ns / 1ps \n')
f_out.write('/*------------------------------------------------\n')
f_out.write('Testbench file made by VerilogTestbenchGen.py\n')
f_out.write('------------------------------------------------*/\n\n\n')

# generate ports
start = 0
line_number = 0
with open(READ_FILE_NAME, 'r') as f:
    while True:
        line_input = f.readline()
        line_number += 1
        line_temp = line_input.split()
        lenth = len(line_temp)
        # read a empty line doesn't mean the module defination is over.
        if lenth == 0:
            continue
        # module is over.
        elif line_temp[0] == ');':
            break

        elif line_temp[0] == 'module(':
            print(f'Can not find module name in line {line_number}.')
            exit(0)
        elif line_temp[0] == 'module':
            # the start of a module
            start = 1
            # delete '(' in the module name
            module_name = line_temp[1].replace('(', '')
            # input module error
            if len(module_name) == 0:
                print(f'Can not find module name in line {line_number}.')
                exit(0)
            line_output = 'module '
            line_output += TESTBENCH_MODULE_NAME+module_name
            line_output += '();\n'
            f_out.write(line_output)

        elif line_temp[0] == 'input':
            if start == 0:
                continue
            line_output = 'reg '
            if lenth < 2:
                print(f"Can not find input port name in line {line_number}.")
                exit(0)
            elif lenth == 2 and line_temp[1] == ',':
                print(f"Can not find output port name in line {line_number}.")
                exit(0)
            for i in range(1, lenth):
                # ignore 'wire' or 'reg'
                if line_temp[i] == 'wire':
                    continue
                elif line_temp[i] == 'reg':
                    continue
                # if the last word is ','
                elif i == lenth-2 and line_temp[lenth-1] == ',':
                    line_output += ' '*(LINE_LENTH_1-len(line_output))
                    line_output += line_temp[i]+';'
                    break
                # if it is the last word
                elif i == lenth-1:
                    line_output += ' '*(LINE_LENTH_1-len(line_output))
                    # there may not have a ',' in the last word
                    line_output += line_temp[i].replace(',', '')+';'
                else:
                    line_output += ' '+line_temp[i]
            f_out.write('\n'+line_output)

        elif line_temp[0] == 'output':
            if start == 0:
                continue
            line_output = 'wire'
            if lenth < 2:
                print(f"Can not find output port name in line {line_number}.")
                exit(0)
            elif lenth == 2 and line_temp[1] == ',':
                print(f"Can not find output port name in line {line_number}.")
                exit(0)
            for i in range(1, lenth):
                # ignore 'wire' or 'reg'
                if line_temp[i] == 'wire':
                    continue
                elif line_temp[i] == 'reg':
                    continue
                # if the last word is ','
                elif i == lenth-2 and line_temp[lenth-1] == ',':
                    line_output += ' '*(LINE_LENTH_1-len(line_output))
                    line_output += line_temp[i]+';'
                    break
                # if it is the last word
                elif i == lenth-1:
                    line_output += ' '*(LINE_LENTH_1-len(line_output))
                    # there may not have a ',' in the last word
                    line_output += line_temp[i].replace(',', '')+';'
                else:
                    line_output += ' '+line_temp[i]
            f_out.write('\n'+line_output)

        else:
            continue
f.close()

# generate signals
f_out.write('\n\n\ninitial\n')
f_out.write('begin')
start = 0
with open(READ_FILE_NAME, 'r') as f:
    while True:
        line_input = f.readline()
        line_temp = line_input.split()
        lenth = len(line_temp)
        # read a empty line doesn't mean the module defination is over.
        if lenth == 0:
            continue
        # module is over.
        if line_temp[0] == ');':
            break
        # the start of a module
        elif line_temp[0] == 'module':
            start = 1
        # generate input signal
        elif line_temp[0] == 'input':
            if start == 0:
                continue
            # get the last word
            line_output = line_temp[lenth-1]
            # if the last word is ','
            if line_output == ',':
                line_output = '\t'+line_temp[lenth-2]
                line_output += ' '*(LINE_LENTH_2-len(line_output))
                line_output = line_output+'=\'d0;'
            else:
                line_output = '\t'+line_output.replace(',', '')
                line_output += ' '*(LINE_LENTH_2-len(line_output))
                line_output = line_output+'=\'d0;'
            f_out.write('\n'+line_output)
        else:
            continue
f.close()
f_out.write('\nend\n')

# instant module
start = 0
with open(READ_FILE_NAME, 'r') as f:
    while True:
        line_input = f.readline()
        line_temp = line_input.split()
        lenth = len(line_temp)
        # read a empty line doesn't mean the module defination is over.
        if (lenth == 0):
            continue
        # module is over.
        elif line_temp[0] == ');':
            f_out.write('\n);')
            break
        # the start of a module
        elif line_temp[0] == 'module':
            start = 1
            # delete '(' in the module name
            module_name = line_temp[1].replace('(', '')
            line_output = module_name+" "
            line_output += INST_MODULE_NAME+module_name
            line_output += '\n('
            f_out.write('\n\n'+line_output)

        elif line_temp[0] == 'input' or line_temp[0] == 'output':
            if start == 0:
                continue
            # get the last word
            line_output = line_temp[lenth-1]
            # if the last word is ','
            if line_output == ',':
                line_output = line_temp[lenth-2]
                line_output = '\t.'+line_output+'('+line_output+'),'
            # if the last letter of the last word is ','
            elif line_output[len(line_output)-1] == ',':
                line_output = line_output.replace(',', '')
                line_output = '\t.'+line_output+'('+line_output+'),'
            else:
                line_output = '\t.'+line_output+'('+line_output+')'
            # add scripts of the ports
            line_output += ' '*(LINE_LENTH_3-len(line_output))
            line_output += '//'
            for i in range(0, lenth-1):
                # ignore 'wire' or 'reg'
                if line_temp[i] == 'wire':
                    continue
                elif line_temp[i] == 'reg':
                    continue
                else:
                    # if the last word is ','
                    if i == lenth-2 and line_temp[lenth-1] == ',':
                        continue
                    else:
                        line_output += ' '+line_temp[i]
            f_out.write('\n'+line_output)

        else:
            continue
f.close()

f_out.write('\n\nendmodule')

f_out.close()
