# -*- coding: utf-8 -*-

import sys

def get_contents_target_command(contents, target_command, prompt_char, enable_perfect_match):
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
            if command_start == False:
                if target_command in line:
                    if line.find(target_command) <= 0:
                        continue
                    if enable_perfect_match:
                        line_temp = line.rstrip()
                        if line_temp.index(target_command) != len(line_temp) - len(target_command):
                            continue
                    command_start = True
                    contents_target_command.append(line)
                    continue
            else:
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

def print_contents_target_command(filenamePath, contents_target_command):
    """
    Print execution result of target_command.
    """
    print("##----------------------------------------------------------------------##")
    print("## {0}".format(filenamePath))
    print("##----------------------------------------------------------------------##")
    for line in contents_target_command:
        print(line, end="")
