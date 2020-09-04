# !/usr/bin/python
# coding=utf-8
from __future__ import division

import math
import numpy as np
from log import log


# 构建新的table  table2
def build_new_table(is_all_digital, avgs, table, new_table, index, row):
    # 当前列是否是全数字标识。
    is_number = True
    # 获取table第一行第 ${index} + 1 列的值
    code = table[0][index]

    # 不是数字时
    if not isinstance(code, float) and not isinstance(code, int):
        is_number = False
        new_table[0][index] = code
        is_all_digital[index] = False
    # 初始化最大值和最小值，浮点型
    max = min = 0.0

    if is_number:
        max = min = code
    # 临时变量，浮点型
    tmp = 0.0

    # 找出最大值和最小值
    for i in range(row):
        if not is_number:
            new_table[i][index] = table[i][index]
            continue
        code = table[i][index]
        # 如果不是数字，跳过本次循环
        if not isinstance(code, float) and not isinstance(code, int):
            is_number = False
            new_table[i][index] = code
            is_all_digital[index] = False
            continue

        # 逻辑可以执行到这里，表明当前值 ${table[i][index]} 是一个数字
        tmp = code
        if tmp > max:
            max = tmp
        if tmp < min:
            min = tmp

    # 此条件成立，则表示整列都是数字。
    if is_number:
        log.debug('第%d列最大值：%s, 最小值：%s', index + 1, max, min)
        is_all_digital[index] = True
        __new_table_value(avgs, new_table, table, index, row, max, min)
    else:
        log.debug('第%d列非数字列', index + 1)


# 设置新table值
def __new_table_value(avgs, new_table, table, index, row, max, min):
    total = 0.0
    tmp = 0.0
    for i in range(row):
        tmp = (table[i][index] - min) / (max - min)
        total += tmp
        # 四舍五入，保留六位小数，并将结果存入新table中
        new_table[i][index] = round(tmp, 6)
    # 求得平均值
    avgs[index] = round(total / row, 6)


# 求离散值table
def discrete_value_table(table, tree_new_table, number_new_table, ngb_new_table, r, is_all_digital, row, col):
    # 外层，里层遍历行数
    total = 0
    for i in range(row):
        x = table[i][col]
        name_i = "x" + str(i + 1)
        for j in range(i + 1, row):
            y = table[j][col]
            name_j = "x" + str(j + 1)
            # 整列都是数字时
            if is_all_digital[col]:
                # 在范围内
                if abs(x - y) <= r:
                    tree_new_table[i][col].append(name_j)
                    tree_new_table[j][col].append(name_i)
            # 整列都是字母或包含字母时
            else:
                if x == y:
                    tree_new_table[i][col].append(name_j)
                    tree_new_table[j][col].append(name_i)
        # 记录个数
        number_new_table[i][col] = len(tree_new_table[i][col])
        total += number_new_table[i][col]

    ngb_new_table[col] = total


def hch_table_value(hch_new_table, number_new_table, ngb_new_table, row, col):
    total = 0.0
    for i in range(col):
        hch = tmp = 0.0
        for j in range(row):
            tmp = number_new_table[j][i] / ngb_new_table[i]
            try:
                tmp = tmp * math.log(tmp)
            except ValueError:
                tmp = 0
            hch += tmp
        hch = round(-(hch * (math.log(1 / col))), 6)
        hch_new_table[i] = hch
        total += hch
    return total


# 权重表
def weight_table(weight_new_table, hcn_new_table, deno, col):
    for i in range(col):
        weight_new_table[i] = round((1 - hcn_new_table[i]) / deno, 6)


# 生成相似矩阵
def build_similar_new_table(table, weight_table, similar_table, is_all_digital, row, col):
    for i in range(col):
        # 构建对应一张 row * row 的二维表
        new_table = [[None for m in range(row)] for n in range(row)]
        # 为生成s表做准备，有几列，生成多少张表
        __build_col_number_new_table(table, new_table, weight_table[i], row, i, is_all_digital[i])
        # 把中间表结果相加
        similar_table += np.array(new_table)
    # 四舍五入矩阵的每一个值，保留六位小数
    return np.round(similar_table, decimals=6)


def __build_col_number_new_table(table, new_table, weight_value, row, col, is_number):
    for i in range(row):
        for j in range(i, row):
            # 对角线，直接赋值为0
            if i == j:
                new_table[i][j] = 0
            else:
                # 该列是全数字
                if is_number:
                    tmp = table[i][col] - table[j][col]
                    new_table[i][j] = new_table[j][i] = (1 - abs(tmp)) * weight_value
                # 该列存在字母
                else:
                    # 三目运算符， 类似 c语言 (x > y)? x: y
                    tmp = 1 if (table[i][col] == table[j][col]) else 0
                    new_table[i][j] = new_table[j][i] = tmp * weight_value


# 生成N矩阵，二进制表
def build_binary_new_table(tree_new_table, binary_table, row, col):
    for i in range(row):
        for j in range(row):
            if i == j:
                continue
            row_x = "x" + str(j + 1)
            for z in range(col):
                if row_x in tree_new_table[i][z]:
                    binary_table[i][j] = 1
                    break


# 矩阵点乘
def build_a_new_table(similar_table, binary_table):
    # 四舍五入矩阵的每一个值，保留六位小数
    return np.round(np.multiply(similar_table, binary_table), decimals=6)


# D矩阵
def build_d_new_table(d_table, a_table, row):
    for i in range(row):
        for j in range(row):
            if i == j:
                d_table[i][j] = round(a_table[i].sum(), 6)
                break


# 矩阵求逆
def build_d_inverse_new_table(d_table):
    # 四舍五入矩阵的每一个值，保留六位小数
    return np.round(np.linalg.inv(np.array(d_table)), decimals=6)
    # return np.matrix(d_table).I


# 转移概率p矩阵 矩阵乘法
def build_p_new_table(d_inverse_table, a_table):
    # 四舍五入矩阵的每一个值，保留六位小数
    return np.round(np.dot(d_inverse_table, a_table), decimals=6)


def build_π_new_table(π, p_table, row):
    # 四舍五入矩阵的每一个值，保留六位小数
    π1 = np.round(np.dot(π, p_table), decimals=6)
    if (π == π1).all():
        return π1
    else:
        return build_π_new_table(π1, p_table, row)


def get_imps(π_table, imps1, row):
    max1 = max(π_table)
    min1 = min(π_table)
    for i in range(row):
        imps = "IMPS(" + str(i + 1) + ")= %s"
        tmp = round(((100 - 1) * (π_table[i] - min1) / (max1 - min1)), 6) + 1
        imps1[i] = tmp
        log.debug(imps, tmp)


def get_abns(binary_table, imps, row) -> dict:
    binary_table = np.array(binary_table)
    # 创建一个空字典
    dict_abns = {}
    for i in range(row):
        sum_n = binary_table[i].sum()
        abns = "ABNS(" + str(i + 1) + ")"
        float_value = round(imps[i] / sum_n, 6)
        dict_abns[abns] = float_value
        log.info(abns + "= %s", float_value)
    return dict_abns


# 格式化输出table
def format_table(table, row, col):
    for i in range(row):
        str_row_value = ""
        for j in range(col):
            str_row_value = str_row_value + str(table[i][j]) + "    "
        log.debug("X%d: %s", i + 1, str_row_value)
