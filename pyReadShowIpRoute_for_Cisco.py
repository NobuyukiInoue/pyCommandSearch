# -*- coding: utf-8 -*-

import sys

def main():
    argv = sys.argv
    argc = len(argv)

    # Argument check.
    if argc < 2:
        exit_msg(argv[0])

    enable_sort = False
    if argc > 2:
        if argv[2].upper() == "TRUE":
            enable_sort = True

    filename = argv[1].replace("\"", "")
    target_command = "show ip route vrf *"
    enable_perfect_match = True

    prompt_char = ["#", "> ", ">"]

    encodings = ["ascii", "sjis", "utf8"]
    for enc in encodings:
        # Read the contents of a file.
        try:
            f = open(filename, "rt", encoding=enc)
            contents = f.readlines()
            f.close
            break
        except:
            continue

    # Get execution result of target_command.
    contents_target_command, prompt_list = get_contents_target_command_command(contents, target_command, prompt_char, enable_perfect_match)

    """
    Print execution result of target_command.
    """
    """
    print("##----------------------------------------------------------------------##")
    print("## {0}".format(filename))
    print("##----------------------------------------------------------------------##")
    for line in contents_target_command:
        print(line, end="")
    """

    """
    Store the execution result of "show ip route vrf *" in the list.
    """
    started_vrf, started_routes = False, False
    i = 0
    table = {}
    """
    table[vrf_id] fields:
    table[vrf_id][0]    decimal of destinaton ipaddr.
    table[vrf_id][1]    destination ipaddr.
    table[vrf_id][2]    [distance/metric]
    table[vrf_id][3]    next hop.
    table[vrf_id][4]    elapsed time.
    table[vrf_id][5]    Output interface.
    table[vrf_id][6]    Codes.
    """
    while i < len(contents_target_command):
        line = contents_target_command[i].rstrip()
        if line == "":
            i += 1
            continue
        if "Routing Table:" in line:
            vrf_id = line.replace("Routing Table: ", "")
            started_routes = False
            started_vrf = True
            table[vrf_id] = []
            """
            # print line for debug.
            print("##----------------------------------------------------------------------##")
            print("## {0}".format(line))
            print("##----------------------------------------------------------------------##")
            """
            i += 1
            continue
        if started_vrf and "Gateway of last resort" in contents_target_command[i]:
            started_routes = True
            i += 1
            continue
        if started_routes == False:
            i += 1
            continue
        if "is variably subnetted" in line:
            i += 1
            continue
        if "is subnetted" in line:
            i += 1
            continue

        """
        Example)
        Before) "C       192.168.4.248/30 is directly connected, GigabitEthernet0/10"
        After)  "C       192.168.4.248/30 [0/0] via connected, None GigabitEthernet0/10"
        """
        line = line.replace("is directly connected,", "[0/0] via connected, None")
        line = line.replace(",", "")

    #   codes = line[:8].rstrip()
        codes = line[:5].rstrip()
        if line[8] != " " and line[5] == " ":
            """
            Example)
            "O       192.168.255.1/32 [110/36] via 192.168.5.66, 00:14:26, Vlan2171"
            "O E2    192.168.158.0/24 [110/0] via 10.158.254.6, 00:14:26, Vlan612"
            """
            cols = line[8:].split(" ")
            if len(cols) == 6:
                latest_dst_ip = cols[0]
                latest_codes = codes
                cols.append(codes)
                cols = [ipAddrToDecimal(cols[0])] + cols
                table[vrf_id].append(cols)
            else:
                """
                Example)
                "O       192.168.155.0/24 "
                "           [110/110] via 192.168.4.10, 00:14:26, GigabitEthernet0/2"
                "           [110/110] via 192.168.4.2, 00:14:26, GigabitEthernet0/1"
                """
                line = line + " " + contents_target_command[i + 1].replace(",", "").strip()
                cols = line[8:].split(" ")
                if len(cols) == 6:
                    latest_dst_ip = cols[0]
                    latest_codes = codes
                    cols.append(codes)
                    cols = [ipAddrToDecimal(cols[0])] + cols
                    table[vrf_id].append(cols)
                else:
                    print("Format Split Error!!")
                    print("{0:d}:{1}".format(i, line))
                    exit(0)
                i += 1
        elif line[5] != " ":
            """
            Example)
            "O*E2 0.0.0.0/0 [110/1] via 192.168.5.74, 00:14:26, Vlan2173"
            """
            cols = line[5:].split(" ")
            if len(cols) == 6:
                latest_dst_ip = cols[0]
                latest_codes = codes
                cols.append(codes)
                cols = [ipAddrToDecimal(cols[0])] + cols
                table[vrf_id].append(cols)
            else:
                line = line + " " + contents_target_command[i + 1].replace(",", "").rstrip()
                cols = line[5:].split(" ")
                if len(cols) == 7:
                    latest_dst_ip = cols[0]
                    latest_codes = codes
                    cols.append(codes)
                    cols = [ipAddrToDecimal(cols[0])] + cols
                    table[vrf_id].append(cols)
                else:
                    """
                    for example)
                    "S*   0.0.0.0/0 [115/0] via 192.168.5.81"
                    """
                    latest_dst_ip = cols[0]
                    latest_codes = codes
                    if cols[4] == "":
                        cols[4] = "None"
                    cols.append("None")
                    cols.append(codes)
                    cols = [ipAddrToDecimal(cols[0])] + cols
                    table[vrf_id].append(cols)
                i += 1
        elif line[8] == " ":
            """
            for example)
            "           [110/110] via 192.168.4.10, 00:14:26, GigabitEthernet0/2"
            "           [110/110] via 192.168.4.2, 00:14:26, GigabitEthernet0/1"
            """
            cols2 = line.strip().split(" ")
            cols = [latest_dst_ip] + cols2 + [latest_codes]
            cols = [ipAddrToDecimal(cols[0])] + cols
            table[vrf_id].append(cols)
        else:
            print("Format Split Error!!")
            print("{0:d}:{1}".format(i, line))
            exit(0)

    #   print("{0}\n{1}\n".format(line, table[vrf_id][-1]))
        i += 1

    # print result
    for k, v in table.items():
        if enable_sort:
            v.sort()
        print("##----------------------------------------------------------------------##\n"
              "## vrf = {0}\n"
              "##----------------------------------------------------------------------##"
              .format(k))

        for row in v:
            if not "/" in row[1] and not "/" in row[2] and row[3] != "via":
                print("Format Error!!!")
        #   print(row)
        #   print("{1:20}{2:14}{3:4}{4:20}{5:10}{6:20}{7}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        #   print("{0: <12}{1:20}{2:14}{4:20}{5:10}{6:20}{7}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            print("{0:20}{1:14}{3:20}{4:10}{5:20}{6}".format(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

def exit_msg(argv0):
    """
    Print usage example and exit.
    """
    print("Usage: python {0} <logfile> [enable sort]\n"
          "example)\n"
          "python {0} \"./log/sample.log true".format(argv0))
    exit(0)


def get_contents_target_command_command(contents, target_command, prompt_char, enable_perfect_match):
    """
    Get execution result of target_command.
    """
    prompt_list = []
    command_start = False
    contents_target_command = []
    for line in contents:
        # Prompt string detection.
        if len(prompt_list) == 0:
            """
            When multiple prompt character strings are detected to prevent erroneous
            detection of patterns such as "sysname> #comment command", the detection
            position shall be the smaller value.
            """
            pos_min = sys.maxsize
            pos = 0
            for prompt in prompt_char:
                if prompt in line:
                    pos = line.index(prompt)
                    if pos < pos_min:
                        pos_min = pos
            if pos_min > 0 and pos_min != sys.maxsize:
                # Set the prompt string candidates.
                for prompt in prompt_char:
                    prompt_list.append(line[:pos_min] + prompt)
        else:
            # target_command Start line detected.
            if target_command in line:
                if enable_perfect_match:
                    line_temp = line.rstrip()
                    if line_temp.index(target_command) != len(line_temp) - len(target_command):
                        continue
                command_start = True
                contents_target_command.append(line)
                continue
            else:
                if target_command in line:
                    command_start = True
                    contents_target_command.append(line)
                    continue
            if command_start:
                # Detect next prompt.
                if isPrompt(line, prompt_list):
                    command_start = False
                    break
                contents_target_command.append(line)

    return contents_target_command, prompt_list

def isPrompt(line, prompt_list):
    """
    Determine if the target string contains a prompt.
    """
    for prompt in prompt_list:
        if prompt in line:
            return True
    return False

def ipAddrToDecimal(ipAddrStr):
    """
    Convert IP address string to number.
    """
    pos = ipAddrStr.find("/")
    if pos > 0:
        ipaddr = ipAddrStr[:pos]
    else:
        ipaddr = ipAddrStr
    flds = ipaddr.split(".")
    res = 0
    for fld in flds:
        res <<= 8
        res += int(fld)
    return res

if __name__ == "__main__":
    main()
