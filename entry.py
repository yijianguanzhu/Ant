# !/usr/bin/python
# coding=utf-8


from __future__ import division
import create_new_table
from log import log


## 入口
def entry(table: list, ch: int) -> dict:
    # 行数
    row = len(table)
    # 列数
    col = len(table[0])
    # 新table表，二维数组，初始化大小， 【row行 * col列】的表
    new_table = [[None for j in range(col)] for i in range(row)]
    # 记录哪些列是全数字， boolean类型，初始化大小
    is_all_digital = [None] * col
    # 记录平均值，初始化大小
    avgs = [None] * col
    # 记录每列r值的数组
    r_value = [None] * col

    for i in range(col):
        create_new_table.build_new_table(is_all_digital, avgs, table, new_table, i, row)

    for i in range(col):
        if is_all_digital[i]:
            avg = avgs[i]
            std = find_std(avg, new_table, i, row)
            r = round(std / (avg * ch), 6)
            r_value[i] = r
            log.debug("第%d列r值：%s", i + 1, r)

    # 三维数组
    tree_new_table = [[[] for j in range(col)] for i in range(row)]
    # 个数表
    number_new_table = [[None for j in range(col)] for i in range(row)]
    # 权重表，Hch表，邻居表
    weight_new_table = hch_new_table = ngb_new_table = [None] * col

    for i in range(col):
        create_new_table.discrete_value_table(new_table, tree_new_table, number_new_table, ngb_new_table, r_value[i],
                                              is_all_digital,
                                              row, i)

    log.debug('table4 邻域集表')
    create_new_table.format_table(tree_new_table, row, col)
    log.debug('table5 邻居表')
    create_new_table.format_table(number_new_table, row, col)
    log.debug('table6 邻居总和表')
    log.debug(ngb_new_table)
    log.debug('table7 HchTable')
    hcn_total = create_new_table.hch_table_value(hch_new_table, number_new_table, ngb_new_table, row, col)
    log.debug(hch_new_table)

    create_new_table.weight_table(weight_new_table, hch_new_table, col - hcn_total, col)
    log.debug('table8 权重表')
    log.debug(weight_new_table)

    # 生成相似矩阵 row * row
    similar_table = [[0 for j in range(row)] for i in range(row)]
    similar_table = create_new_table.build_similar_new_table(new_table, weight_new_table, similar_table, is_all_digital,
                                                             row,
                                                             col)
    log.debug("相似矩阵S")
    create_new_table.format_table(similar_table, row, row)

    # 生成n表 row行 * row列 ，表格初始值为0
    binary_table = [[0 for j in range(row)] for i in range(row)]
    create_new_table.build_binary_new_table(tree_new_table, binary_table, row, col)
    log.debug("N矩阵，二进制矩阵")
    create_new_table.format_table(binary_table, row, row)

    log.debug("A矩阵")
    a_table = create_new_table.build_a_new_table(similar_table, binary_table)
    create_new_table.format_table(a_table, row, row)

    log.debug("D矩阵")
    # 生成d表 row行 * row列 ，表格初始值为0
    d_table = [[0 for j in range(row)] for i in range(row)]
    create_new_table.build_d_new_table(d_table, a_table, row)
    create_new_table.format_table(d_table, row, row)

    # d表矩阵求逆
    d_inverse_table = create_new_table.build_d_inverse_new_table(d_table)
    log.debug("D逆矩阵")
    create_new_table.format_table(d_inverse_table, row, row)

    # p表
    p_table = create_new_table.build_p_new_table(d_inverse_table, a_table)
    log.debug("转移概率矩阵P")
    create_new_table.format_table(p_table, row, row)

    # π0 迭代计算
    log.debug("平稳状态π")
    π = [1 / row] * row
    πx = create_new_table.build_π_new_table(π, p_table, row)
    log.debug(πx)

    # imps
    log.debug("重要度得分IMPS")
    imps = [None] * row
    create_new_table.get_imps(πx, imps, row)

    # abns
    log.debug("异常值分数ABNS")
    return create_new_table.get_abns(binary_table, imps, row)


# 计算标准差
def find_std(avgs, table, index, row):
    total = std = 0.0

    for i in range(row):
        total += (table[i][index] - avgs) ** 2
        log.debug("第%d行第%d列的值: %s", i + 1, index + 1, table[i][index])

    # 计算标准差
    std = round((total / row) ** 0.5, 6)
    log.debug("第%d列标准差：%s, 平均值：%s", index + 1, std, avgs)
    return std


table = [
    [12, 0.4, "A", "q"],
    [5, 0.2, "B", "m"],
    [8, 0.3, "D", "h"],
    [10, 0.1, "B", "m"],
    [2, 0.1, "A", "q"],
    [13, 0.5, "C", "q"],
    [7, 0.7, "D", "h"],
    [20, 0.9, "B", "m"],
    [14, 0.2, "B", "q"],
    [6, 0.8, "C", "h"]
]

if __name__ == '__main__':
    entry(table, 2)
