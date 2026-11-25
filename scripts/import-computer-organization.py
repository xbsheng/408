#!/usr/bin/env python3
"""把尚硅谷《计算机组成原理》单文件课件拆成按章的文件。

用法：python3 scripts/import-computer-organization.py <源 md> <输出目录>

处理内容（原文件是 Typora 导出的，直接放进 VitePress 会构建失败）：
  1. 按 "## 第X章" 切成 6 个文件，章标题提到 H1，其余标题降一级（代码块内不动）；
  2. pictures\\x.png 之类的反斜杠/绝对路径统一成 images/x.png；
  3. <img src="..."> 改成 Markdown 图片语法，否则 Vite 不打包；
  4. 表格缺 </table> 的补上（Vue 编译器会报 miss end tag）；
  5. 正文里的 pandoc 下标/上标 T~1~、2^10^ 转成 <sub>/<sup>，代码块和公式内不动；
  6. 正文里的 {{ 转成 HTML 实体，避免被 Vue 当成插值；
  7. 正文里的制表符换成 &emsp;（Typora 用 tab 缩进和对齐，HTML 会压成一个空格）；
  8. 图片改名为 img-001.png 之类并拷到 <输出目录>/images，中文文件名进了 URL 会变百分号编码。
"""

import os
import re
import shutil
import sys

CHAPTERS = [
    'chapter-01-overview',
    'chapter-02-data-representation-and-arithmetic',
    'chapter-03-memory',
    'chapter-04-instruction-set',
    'chapter-05-cpu',
    'chapter-06-bus-and-io',
]

# 行内公式与块公式（块公式允许跨行）
MATH = re.compile(r'\$\$.*?\$\$|\$[^$\n]+\$', re.S)
SUB = re.compile(r'~([^\s~<>][^\s~<>]{0,19})~')
SUP = re.compile(r'(?<![\w^])([A-Za-z0-9)\]]) \^([^\s^<>]{1,19})\^')


def protect_math(line):
    """把一行拆成 [是否公式, 文本] 片段。"""
    parts, pos = [], 0
    for m in MATH.finditer(line):
        if m.start() > pos:
            parts.append((False, line[pos:m.start()]))
        parts.append((True, m.group(0)))
        pos = m.end()
    if pos < len(line):
        parts.append((False, line[pos:]))
    return parts


def convert_sub_sup(line):
    out = []
    for is_math, text in protect_math(line):
        if is_math:
            out.append(text)
            continue
        text = SUB.sub(r'<sub>\1</sub>', text)
        text = SUP.sub(r'\1<sup>\2</sup>', text)
        out.append(text)
    return ''.join(out)


def normalize_picture(path):
    """各种写法（pictures\\x.png、C:\\...\\pictures/x.png）统一成 images/x.png。

    源文件里的图片都平铺在一个目录里，直接取文件名即可。
    """
    name = path.replace('\\', '/').split('#')[0].rsplit('/', 1)[-1]
    return 'images/' + name


IMG_FILE = re.compile(r'\.(png|jpe?g|gif|webp|bmp|svg)$', re.I)


def fix_images(line):
    """Markdown 图片和 <img> 标签都归一成 ![](images/xxx.png)。"""

    def md_link(m):
        target = m.group(1)
        if not IMG_FILE.search(target.split('#')[0]):
            return m.group(0)
        return '](' + normalize_picture(target) + ')'

    def html_img(m):
        src = m.group(1)
        if not IMG_FILE.search(src.split('#')[0]):
            return m.group(0)
        return f'![]({normalize_picture(src)})'

    line = re.sub(r'\]\(([^)]+)\)', md_link, line)
    line = re.sub(r'<img[^>]*?src="([^"]+)"[^>]*?/?>', html_img, line)
    return line


TAB_RUN = re.compile(r'\t+')


def expand_tabs(line):
    """Typora 里制表符用于缩进和对齐，HTML 会把 tab 压成一个空格，这里换成全角空格。"""
    return TAB_RUN.sub(lambda m: '&emsp;' * (2 * len(m.group(0))), line)


def split_heading(line):
    m = re.match(r'^(#{2,5}) (.*)$', line)
    if not m:
        return line
    return '#' * (len(m.group(1)) - 1) + ' ' + m.group(2)


# 源文件名里有空格（如 "2_58_IEEE 浮点数形式.png"），所以一直取到右括号
IMAGE_REF = re.compile(r'images/([^)\n]+)')


def main(src, outdir):
    raw = open(src, encoding='utf-8-sig').read().replace('\r\n', '\n')
    lines = raw.split('\n')
    src_images = os.path.join(os.path.dirname(os.path.abspath(src)), 'pictures')

    starts = [i for i, l in enumerate(lines) if re.match(r'^## 第[一二三四五六]章 ', l)]
    if len(starts) != len(CHAPTERS):
        sys.exit(f'找到 {len(starts)} 个章标题，期望 {len(CHAPTERS)} 个')

    chapters = []
    for n, start in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(lines)
        block = lines[start:end]

        fence = False
        in_table = False
        out = []
        for line in block:
            if re.match(r'^\s*(```|~~~)', line):
                fence = not fence
                out.append(line)
                continue
            if fence:
                out.append(line)
                continue

            line = fix_images(line)
            line = convert_sub_sup(line)
            line = expand_tabs(line)

            # 表格没写 </table>：遇到下一个标题前补上
            if '<table' in line:
                in_table = True
            if '</table>' in line:
                in_table = False
            if in_table and re.match(r'^#{1,6} ', line):
                while out and not out[-1].strip():
                    out.pop()
                out.append('  </table>')
                out.append('')
                in_table = False

            out.append(line)

        # 标题层级调整 + {{ 转义
        result, fence = [], False
        for line in out:
            if re.match(r'^\s*(```|~~~)', line):
                fence = not fence
                result.append(line)
                continue
            if fence:
                result.append(line)
                continue
            result.append(split_heading(line).replace('{{', '&#123;&#123;'))

        chapters.append((n, len(block), '\n'.join(result).strip('\n') + '\n'))

    # 图片统一改名 img-001.png 之类：中文文件名进了 URL 会变成百分号编码，容易出问题
    mapping = {}
    for _, _, text in chapters:
        for m in IMAGE_REF.finditer(text):
            name = m.group(1)
            if name not in mapping:
                ext = os.path.splitext(name)[1].lower()
                mapping[name] = f'img-{len(mapping) + 1:03d}{ext}'

    os.makedirs(os.path.join(outdir, 'images'), exist_ok=True)
    for old, new in mapping.items():
        shutil.copy2(os.path.join(src_images, old), os.path.join(outdir, 'images', new))

    for n, count, text in chapters:
        text = IMAGE_REF.sub(lambda m: 'images/' + mapping[m.group(1)], text)
        open(os.path.join(outdir, CHAPTERS[n] + '.md'), 'w', encoding='utf-8').write(text)
        print(f'{CHAPTERS[n]}.md  {count} 行')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
