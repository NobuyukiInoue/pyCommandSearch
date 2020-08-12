# -*- coding: utf-8 -*-

import glob
import sys
from commonLib import commonLib

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
        """
        # ファイルの内容を読み込む
        # f = open(filename, "rt", encoding="ascii")
        # f = open(filename, "rt", encoding="sjis")
        # f = open(filename, "rt", encoding="utf8")
        """
        encodings = ["ascii", "sjis", "utf8"]
        for enc in encodings:
            # ファイルの内容を読み込む
            try:
                f = open(filename, "rt", encoding=enc)
                contents = f.readlines()
                f.close
                break
            except:
                continue

        # target_commandの実行結果を取得する
        contents_target_command, prompt_list = commonLib.get_contents_target_command(contents, target_command, prompt_char, enable_perfect_match)

        # target_commandの実行結果を表示する
        commonLib.print_contents_target_command(filename, contents_target_command)

    print("##----------------------------------------------------------------------##")

def exit_msg(argv0):
    """使用例を表示する"""
    print("Usage: python {0} <logfiles target_path> <target_command> <match_flag>\n"
          "example)\n"
          "python {0} \"../log/*.log\" \"show ip route\" false".format(argv0))
    exit(0)

if __name__ == "__main__":
    main()
