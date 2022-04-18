import sys

def charhex2int ( str ):
    if str == 'a' or str == 'A':
        return 10
    elif str == 'b' or str == 'B':
        return 11
    elif str == 'c' or str == 'C':
        return 12
    elif str == 'd' or str == 'D':
        return 13
    elif str == 'e' or str == 'E':
        return 14
    elif str == 'f' or str == 'F':
        return 15
    else:
        return int(str)

def strhex2int ( str ):
    hexdat = 0
    for power in range(0, len(str)):
        hexdat = hexdat + charhex2int(str[-(power + 1)]) * pow(16, power)
    return hexdat

def outputline ( loc, hexbuffer, file ):
    file.write((':10%04x00' % loc).upper())
    check_sum = 0
    for i in range(0, 0x10):
        file.write(('%02x' % buffer[i]).upper())
        check_sum = check_sum + buffer[i]
    check_sum = check_sum + strhex2int(('%04x' % loc)[0:2]) + strhex2int(('%04x' % loc)[2:4]) + 0x10 + 0x00
    check_sum = check_sum % 256
    if check_sum != 0:
        check_sum = 0x100 - check_sum
    file.write(('%02x' % check_sum).upper())
    file.write('\n')

if __name__ == '__main__':
    filename = sys.argv[1]
    buffer = [0 for i in range(0x10)]
    with open(filename + ".tmp.hex", "w") as o:
        with open(filename, "r") as f:
            diclines = {}
            sortlines = f.readline()
            while(sortlines != ''):
                if sortlines[7:9] == '00':
                    diclines[strhex2int(sortlines[3:7])] = sortlines
                sortlines = f.readline()
            diclineslist = sorted(diclines.items(), key=lambda x: x[0])
        for value in diclineslist:
            o.write(value[1])
            if value[0] == diclineslist[-1][0]:
                outputline( strhex2int(value[1][3:7]) + strhex2int(value[1][1:3]) + 0x10, buffer, o)
                # o.write(':01' + ('%04x' % (strhex2int(value[1][3:7]) + strhex2int(hex_line[1:3]))) + '')

    with open(filename + ".out.hex", "w") as o:
        with open(filename + ".tmp.hex", "r") as f:
            hex_line = f.readline()
            convert_loc = (strhex2int(hex_line[3:7]) // 0x10) * 0X10
            convert_bias = 0
            source_loc = 0
            source_bias = 0
            line_bytes_cnt = 0
            buffer = [0 for i in range(0x10)]
            # print(strhex2int('FFFF'))
            while(hex_line != ''):
                print(hex_line[1:3] + ' ' + hex_line[3:7] + '->' + hex(strhex2int(hex_line[3:7])) + ' ' + hex_line[7:9] + ' ' + hex_line[9:-3])
                hex_line_next = f.readline()
                # if hex_line_next == '':
                #     break
                source_loc = strhex2int(hex_line[3:7])
                source_bias = 0
                for i in range(0, strhex2int(hex_line[3:7]) + strhex2int(hex_line[1:3]) - convert_loc - convert_bias):
                    if(convert_loc + convert_bias == source_loc + source_bias and source_bias < strhex2int(hex_line[1:3])):
                        buffer[convert_bias] = strhex2int(hex_line[9 + source_bias * 2: 11 + source_bias * 2])
                        source_bias = source_bias + 1
                    else:
                        buffer[convert_bias] = 0
                    convert_bias = convert_bias + 1
                    if(convert_bias == 0x10):
                        print('convert:' + hex(convert_loc) + ' ', end="")
                        for i in range(0, 0x10):
                            print(hex(buffer[i]) + ' ', end="")
                        print("")
                        outputline(convert_loc, buffer, o)
                        convert_loc = convert_loc + 0x10
                        convert_bias = 0
                hex_line = hex_line_next
        o.write(':00000001FF')
    with open(filename + ".out.hex", "rb") as fp:
        data = fp.read()
    data = data.replace(b"\n", b"\r\n")
    with open(filename + ".out.win.hex", "wb") as fp:
        fp.write(data)