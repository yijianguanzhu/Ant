# !/usr/bin/python
# coding=utf-8

from pathlib import Path
from excel import read_excel
import msvcrt
import os
from tkinter import filedialog
import tkinter


# deprecated
def check_file(path: str) -> bool:
    file = Path(path)
    if not file.exists():
        print("指定路径不存在，重新输入：", end='')
        return False

    if not file.is_file():
        print("指定路径不是文件，重新输入：", end='')
        return False
    return True


def choose_excel_file() -> str:
    root = tkinter.Tk()
    # 隐藏tk()窗体
    root.withdraw()
    # 设置文件对话框显示的文件类型
    file_type = [('excel file', '.xlsx')]
    # 请求选择文件
    path = filedialog.askopenfilename(initialdir=os.getcwd(), title="选择一个excel文件", filetypes=file_type)
    # 选择完成后，销毁文件选择框
    root.destroy()
    return path


if __name__ == '__main__':
    print("选择一个excel文件，按任意键继续...")
    ord(msvcrt.getch())
    path = choose_excel_file()
    try:
        read_excel.ReadExcelXlsx(path).read_excel()
    except Exception as e:
        print("读取文件失败。Cause by：", e)
    print("操作完成，按任意键退出...")
    ord(msvcrt.getch())
