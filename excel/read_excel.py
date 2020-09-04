# !/usr/bin/python
# coding=utf-8

import pandas as pd
import entry
import create_new_table
from log import log
from excel import write_excel


# 定义一个读取excel .xlsx 的类
class ReadExcelXlsx:

    def __init__(self, path: str = None):
        # excel文件位置路径
        self.path = path
        self.θ = None

    def read_excel(self):
        if self.path is None:
            log.error("请指定Excel文件。")
            return

        data = pd.read_excel(self.path, sheet_name=None, header=None)
        # 解析sheet
        for sheet_name in data:
            self.__resolve_sheet(data, sheet_name)

    # 解析sheet表单
    def __resolve_sheet(self, data: dict, sheet_name: str):
        log.info("正在解析[" + sheet_name + "]表单...")
        # 校验当前sheet是否参与矩阵运算，不参与则跳过
        try:
            str_y_or_no = data[sheet_name].iloc[0, 1]
        except IndexError:
            log.warning("[" + sheet_name + "]表单不符合定义，跳过。")
            return

        if str_y_or_no == "N":
            log.info("[" + sheet_name + "]表单不参与矩阵运算，跳过。")
        elif str_y_or_no == "Y":
            # to do
            try:
                self.__resolve_sheet_header(data, sheet_name)
            except Exception as e:
                log.warning("[" + sheet_name + "]表单解析失败，跳过。")
                return
        else:
            log.warning("[" + sheet_name + "]表单不符合定义，跳过。")

    # 解析表头
    def __resolve_sheet_header(self, data: dict, sheet_name: str):
        # 获取矩阵行起止
        str_row = data[sheet_name].iloc[0, 4]
        # 获取矩阵列起止
        str_col = data[sheet_name].iloc[1, 4]
        # θ值
        int_θ = int(data[sheet_name].iloc[1, 1])
        log.info("解析到θ值:%d", int_θ)
        self.θ = int_θ
        """ 
            使用","分割，返回list
        """
        # 所有矩阵的行起止
        list_row = str_row.split(",")
        # 所有矩阵的列起止
        list_col = str_col.split(",")
        if len(list_row) != len(list_col):
            log.error("矩阵行起止和矩阵列起止长度不相等。")
            raise ValueError()
        # 矩阵的个数
        int_length = len(list_row)
        writer = write_excel.WriteExcelXlsx(self.path, sheet_name)
        for i in range(int_length):
            str_row = list_row[i][1:-1]
            str_col = list_col[i][1:-1]
            # 某一矩阵的行起止
            list_row_r = str_row.split(":")
            # 某一矩阵的列起止
            list_col_c = str_col.split(":")

            int_row_start = int(list_row_r[0])
            int_row_end = int(list_row_r[1])
            int_col_start = int(list_col_c[0])
            int_col_end = int(list_col_c[1])
            dict_abns = self.__resolve_matrix(data, sheet_name, int_row_start, int_row_end, int_col_start, int_col_end)

            for key in dict_abns:
                int_row_start += 1
                writer.write_excel(int_row_start, int_col_end + 1, key + ":" + str(dict_abns[key]))
        # 把数据写入excel
        writer.wk.save(self.path)
        # 关闭文件
        writer.wk.close()

    # 解析sheet表单中的矩阵
    def __resolve_matrix(self, data: dict, sheet_name: str, int_row_start, int_row_end, int_col_start,
                         int_col_end) -> dict:
        str_matrix_name = data[sheet_name].iloc[int_row_start - 1, int_col_start - 1]
        log.info("解析到矩阵[%s]", str_matrix_name)
        # 读取指定范围内的矩阵
        obj_matrix = data[sheet_name].iloc[int_row_start:int_row_end, int_col_start:int_col_end]
        # object转成list 二维矩阵
        list_matrix = obj_matrix.values
        create_new_table.format_table(list_matrix, len(list_matrix), len(list_matrix[0]))
        return entry.entry(list_matrix, self.θ)

# read_excel = ReadExcelXlsx("D:\\py_test.xlsx")
# read_excel.read_excel()
