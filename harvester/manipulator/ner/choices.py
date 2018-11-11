from collections import OrderedDict


# !! update 2018-01-25 !!
# 所有 Index 相关操作，慎用动态生成
# 现已迁移到 estimation/indexes.py 中


def generate_legal_index_pair(choice):
    PAIR = lambda x, y: str(x) + '_' + str(y)
    start, inter, end, ret, other = [], [], [], [], []
    l = len(choice) - 1
    for i in range(l):
        start, inter, end = [], [], []
        start.extend([PAIR(i * 3, i * 3 + 1), PAIR(i * 3, i * 3 + 2)])
        inter.extend([PAIR(i * 3 + 1, i * 3 + 1), PAIR(i * 3 + 1, i * 3 + 2)])
        start.extend(list([PAIR(i * 3, j * 3) for j in range(l)]))
        end.extend(list([PAIR(i * 3 + 2, j * 3) for j in range(l)]))
        start.append(PAIR(i * 3, l * 3))
        end.append(PAIR(i * 3 + 2, l * 3))
        other.append(PAIR(l * 3, i * 3))
        ret.extend(start + inter + end)
    other.append(PAIR(l * 3, l * 3))
    ret.extend(other)

    return ret


# Deprecated
WORD_POS_LTP_CHOICES = (
    ('n', '名词'),
    ('ns', '地名'),
    ('ni', '组织名'),
    ('b', '区别词'),
    ('nl', '方位词'),
    ('c', '连词'),
    ('d', '副词'),
    ('a', '形容词'),
    ('nt', '时间词'),
    ('e', '惊叹词'),
    ('nz', '专有名词'),
    ('g', '词素'),
    ('o', '拟声词'),
    ('h', '前缀词'),
    ('p', '介词'),
    ('i', '成语'),
    ('q', '量词'),
    ('j', '缩写词'),
    ('r', '代词'),
    ('k', '后缀词'),
    ('u', '附属词'),
    ('m', '数词'),
    ('v', '动词'),
    ('wp', '标点'),
    ('nd', '方向词'),
    ('ws', '外国词'),
    ('nh', '人名'),
    ('x', '其他'),
)

# 2018-01-25, 目前在用, 所有分词相关
# jieba POS
JIEBA_POS_CHOICES = (
    ('n', '名词'),
    ('nr', '人名'),
    ('ns', '地名'),
    ('nt', '机构'),
    ('nz', '专用名'),
    ('v', '动词'),
    ('a', '形容词'),
    ('ad', '副形词'),
    ('ag', '形容词性语素'),
    ('an', '名形词'),
    ('b', '区别词'),
    ('c', '连词'),
    ('d', '副词'),
    ('df', '方位副词'),
    ('dg', '副语素'),
    ('e', '叹词'),
    ('f', '方位词'),
    ('g', '语素'),
    ('h', '前接'),
    ('i', '成语'),
    ('j', '略语'),
    ('k', '后接'),
    ('l', '习用语'),
    ('m', '数词'),
    ('mq', '数词*'),
    ('mg', '数语素'),
    ('nrt', '名词*'),
    ('nrfg', '名词*'),
    ('ng', '名动词'),
    ('o', '拟声词'),
    ('p', '介词'),
    ('q', '量词'),
    ('r', '代词'),
    ('rr', '人称代词'),
    ('rz', '代词*'),
    ('rg', '代词语素'),
    ('s', '处所词'),
    ('t', '时间词'),
    ('tg', '时语素'),
    ('u', '助词'),
    ('ug', '助词素'),
    ('uv', '助动词'),
    ('ul', '助词*'),
    ('uz', '助词*'),
    ('uj', '助词*'),
    ('ud', '助词*'),
    ('vd', '副动词'),
    ('vg', '动语素'),
    ('vi', '动词*'),
    ('vn', '名动词'),
    ('vq', '动词*'),
    ('x', '符号'),
    ('y', '语气词'),
    ('z', '状态词'),
    ('zg', '状态词素'),
    ('w', '标点'),
    ('eng', '英文'),
    ('yg', '未知'),
    ('placeholder1', '占位1'),
)

JIEBA_POS_DICT = OrderedDict(JIEBA_POS_CHOICES)

# NER #
NER_CHOICES = (
    ('nr', '人名'),
    ('ns', '地名'),
    ('nt', '机构'),
    ('o', '其他'),
)

NER_PART_CHOICES = (
    ('nr_s', '人名首'),  # 0
    ('nr_i', '人名中'),  # 1
    ('nr_e', '人名尾'),  # 2

    ('ns_s', '地名首'),  # 3
    ('ns_i', '地名中'),  # 4
    ('ns_e', '地名尾'),  # 5

    ('nt_s', '机构首'),  # 6
    ('nt_i', '机构中'),  # 7
    ('nt_e', '机构尾'),  # 8

    ('o', '其他')  # 9
)

NER_DICT = OrderedDict(NER_CHOICES)
NER_PART_DICT = OrderedDict(NER_PART_CHOICES)

# ENTITY #
ENTITY_CHOICES = (
    ('n', '产品名称'),
    ('e', '收益'),
    ('d', '期限'),
    ('s', '规模'),
    ('p', '进度'),
    ('o', '其它')
)
ENTITY_MAX_LENGTH = 300
ENTITY_PARTS_CHOICES = (
    ('n_s', '产首'),  # 0
    ('n_i', '产中'),  # 1
    ('n_e', '产尾'),  # 2

    ('e_s', '收益首'),  # 3
    ('e_i', '收益中'),  # 4
    ('e_e', '收益尾'),  # 5

    ('d_s', '期限首'),  # 6
    ('d_i', '期限中'),  # 7
    ('d_e', '期限尾'),  # 8

    ('s_s', '规模首'),  # 9
    ('s_i', '规模中'),  # 10
    ('s_e', '规模尾'),  # 11

    ('p_s', '进度首'),  # 12
    ('p_i', '进度中'),  # 13
    ('p_e', '进度尾'),  # 14

    ('o', '其它')  # 15
)
ENTITY_DICT = OrderedDict(ENTITY_CHOICES)
ENTITY_PART_DICT = OrderedDict(ENTITY_PARTS_CHOICES)

NAME_ENTITY_MAX_LENGTH = 50
NAME_ENTITY_CHOICES = (
    ('s', '系列名'),
    ('o', '其它')
)
NAME_ENTITY_PARTS_CHOICES = (
    ('s_s', '系列首'),  # 0
    ('s_i', '系列中'),  # 1
    ('s_e', '系列尾'),  # 2

    ('o', '其他'),  # 3
)
NAME_ENTITY_DICT = OrderedDict(NAME_ENTITY_CHOICES)
NAME_ENTITY_PART_DICT = OrderedDict(NAME_ENTITY_PARTS_CHOICES)
