# -*- coding: utf-8 -*-

import glob
import sys

def main():
    argv = sys.argv
    argc = len(argv)

    # 引数チェック
    if argc < 3:
        exit_msg(argv[0])

    enable_perfect_match = False
    if argc >= 4:
        if argv[3].upper() == "TRUE":
            enable_perfect_match = True

    # target_command = "show chassis power"
    target_command = ""
    if argc >= 3:
        target_command = argv[2].replace("\"", "")

    target_path = "../log/*.log"
    if argc >= 2:
        target_path = argv[1].replace("\"", "")

    # ファイル一覧の取得
    files_list = glob.glob(target_path)

    """
    for filename in files_list:
        print(filename)
    """

    prompt_char = ["#", "> ", ">"]

    for filename in files_list:
        # ファイルの内容を読み込む
        f = open(filename, "rt", encoding="ascii")
        contents = f.readlines()
        f.close

        # target_commandの実行結果を取得する
        contents_target_command, prompt_list = get_contents_target_command_command(contents, target_command, prompt_char, enable_perfect_match)

        # target_commandの実行結果を表示する
        print("##----------------------------------------------------------------------##")
        print("## {0}".format(filename))
        print("##----------------------------------------------------------------------##")
        for line in contents_target_command:
            print(line, end="")
    print("##----------------------------------------------------------------------##")

def exit_msg(argv0):
    """使用例を表示する"""
    print("Usage: python {0} <logfiles target_path> <target_command> <match_flag>\n"
          "example)\n"
          "python {0} \"../log/*.log\" \"show ip route\" false".format(argv0))
    exit(0)


def get_contents_target_command_command(contents, target_command, prompt_char, enable_perfect_match):
    """ target_commandの実行結果を取得する"""
    prompt_list = []
    command_start = False
    contents_target_command = []
    for line in contents:
        # プロンプト文字列の検出
        if len(prompt_list) == 0:
            # "sysname> #comment command"といったパターンの誤検知防止のため
            # プロンプト文字列が複数検出された場合は、検出位置は小さい方の値とする。
            pos_min = sys.maxsize
            pos = 0
            for prompt in prompt_char:
                if prompt in line:
                    pos = line.index(prompt)
                    if pos < pos_min:
                        pos_min = pos
            if pos_min > 0 and pos_min != sys.maxsize:
                # プロンプト文字列の候補をセットする
                for prompt in prompt_char:
                    prompt_list.append(line[:pos_min] + prompt)
        else:
            # target_command開始行の検出
            if target_command in line:
                if enable_perfect_match:
                    line_temp = line.rstrip()
                    # 誤判断防止のため、正規表現を使った検索は廃止した（エスケープが面倒）
                    # example)
                    # "show ip route vrf *"
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
                contents_target_command.append(line)

                # 次のプロンプトの検出
                if isPrompt(line, prompt_list):
                    command_start = False
                    break

    return contents_target_command, prompt_list

def isPrompt(line, prompt_list):
    for prompt in prompt_list:
        if prompt in line:
            return True
    return False

if __name__ == "__main__":
    main()
