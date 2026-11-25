#!/usr/bin/env python3
"""生成「视频分 P」汇总页（学习路线对照表 + 完整视频目录）。

用法：python3 scripts/gen-videos.py

分 P 数据从 B 站 pagelist 接口实时拉取，本地不用维护 200 多行表格。
章节区间写在 SUBJECTS 里，视频更新后调整区间重跑即可。
"""

import json
import re
import urllib.request

API = 'https://api.bilibili.com/x/player/pagelist?bvid={bvid}'
HEADERS = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.bilibili.com/'}

SUBJECTS = [
    {
        'bvid': 'BV1Bh4y1q7Nt',
        'out': 'c/videos.md',
        'title': 'C 语言视频目录',
        'intro': '课件整理自尚硅谷宋红康《C 语言精讲版》，下面把每一章对应到 B 站的分 P。',
        'link_prefix': '/c/',
        'chapters': [
            ('第01章 · C 语言入门', 1, 10, 'chapter-01-introduction'),
            ('第02章 · 变量与进制', 11, 21, 'chapter-02-variables-and-number-systems'),
            ('第03章 · 运算符与流程控制', 22, 44, 'chapter-03-operators-and-control-flow'),
            ('第04章 · 数组', 45, 56, 'chapter-04-arrays'),
            ('第05章 · 指针', 57, 74, 'chapter-05-pointers'),
            ('第06章 · 函数', 75, 99, 'chapter-06-functions'),
            ('第07章 · 结构体与共用体', 100, 114, 'chapter-07-structures-and-unions'),
            ('第08章 · C 语言常用函数', 115, 122, 'chapter-08-library-functions'),
            ('第09章 · 文件操作', 123, 125, 'chapter-09-file-operations'),
        ],
    },
    {
        'bvid': 'BV1vt421L7oc',
        'out': 'computer-organization/videos.md',
        'title': '计算机组成原理视频目录',
        'intro': '下面把每一章对应到 B 站的分 P，最后一节是章节练习与总结。',
        'link_prefix': '/computer-organization/',
        'chapters': [
            ('课程简介', 1, 1, None),
            ('第一章 · 计算机系统概述', 2, 11, 'chapter-01-overview'),
            ('第二章 · 数据的表示和运算', 12, 45, 'chapter-02-data-representation-and-arithmetic'),
            ('第三章 · 存储器', 46, 80, 'chapter-03-memory'),
            ('第四章 · 指令系统', 81, 102, 'chapter-04-instruction-set'),
            ('第五章 · 中央处理器', 103, 136, 'chapter-05-cpu'),
            ('第六章 · 总线和输入输出系统', 137, 162, 'chapter-06-bus-and-io'),
        ],
    },
]


def fetch(bvid):
    req = urllib.request.Request(API.format(bvid=bvid), headers=HEADERS)
    data = json.load(urllib.request.urlopen(req))['data']
    return {p['page']: {'title': p['part'], 'duration': p['duration']} for p in data}


def fmt_time(seconds):
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    return f'{h}:{m:02d}:{s:02d}' if h else f'{m:02d}:{s:02d}'


def fmt_span(seconds):
    h, rest = divmod(seconds, 3600)
    m, _ = divmod(rest, 60)
    return f'{h} 小时 {m} 分' if h else f'{m} 分'


def clean(title):
    """去掉 "001." / "001_" 这类序号前缀，序号单独占一列。"""
    return re.sub(r'^\d+[._]\s*', '', title)


def build(subject):
    pages = fetch(subject['bvid'])
    total = sum(pages[i]['duration'] for i in pages)

    out = [f"# {subject['title']}", '', subject['intro'], '',
           f"共 **{len(pages)}** 个分 P，总时长约 **{fmt_span(total)}**。", '',
           '链接格式：`https://www.bilibili.com/video/' + subject['bvid'] + '?p=N`，'
           '打开后直接定位到第 N 集。', '',
           '## 学习路线 & 资料对照', '',
           '| 章节 | 课件 | 视频分 P | 时长 |', '| --- | --- | --- | --- |']

    for name, start, end, link in subject['chapters']:
        span = sum(pages[i]['duration'] for i in range(start, end + 1))
        course = f'[{name}]({subject["link_prefix"]}{link})' if link else name
        part = f'P{start}' if start == end else f'P{start} – P{end}'
        out.append(f'| {course} | {end - start + 1} 个 | {part} | {fmt_span(span)} |')

    out += ['', '## 完整视频目录', '']

    for name, start, end, link in subject['chapters']:
        span = sum(pages[i]['duration'] for i in range(start, end + 1))
        part = f'P{start}' if start == end else f'P{start} – P{end}'
        out += [f'### {name}（{part}，合计 {fmt_span(span)}）', '',
                '| P | 标题 | 时长 | 在线观看 |', '| --- | --- | --- | --- |']
        for i in range(start, end + 1):
            p = pages[i]
            url = f'https://www.bilibili.com/video/{subject["bvid"]}?p={i}'
            out.append(f'| {i} | {clean(p["title"])} | {fmt_time(p["duration"])} | [► 观看]({url}) |')
        out.append('')

    with open(subject['out'], 'w', encoding='utf-8') as f:
        f.write('\n'.join(out).rstrip() + '\n')
    print(f'{subject["out"]}  {len(pages)} 个分 P，共 {fmt_span(total)}')


if __name__ == '__main__':
    for s in SUBJECTS:
        build(s)
