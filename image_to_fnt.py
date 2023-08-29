#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
功能：简单生成fnt格式字体文件
1.美术人员提供所有艺术文字的碎图（最好所有碎图是等高的，这样可以避免高度不一致时，展示效果不美观的问题）
2.所有碎图文件命名为对应的字。例如艺术字“6”的命名为6.png，“中”的命名为“中.png”
3.执行此脚本后，可生成xx.fnt和xx.png
注意：实现较简单，一般文字不多的情况，已足够用
     多page未实现，
     kerning和offset未实现（一般需要在GUI工具手动调整，以达到美观），
     碎图拼接到大图时未实现自动紧凑算法（稍稍浪费一点空间）
    需要安装插件：
    pip install pillow
    pip install imagesize
    需要使用python3的版本调用，否则会出现中文无法识别导致生成fnt失败！！！
"""
import math
import os

from PIL import Image
import imagesize

HEAD = u"""info face="{typeface}" size={fontsize} bold=0 italic=0 charset="" unicode={unicode} stretchH=100 smooth=1 aa=1 padding=0,0,0,0 spacing=1,1
common lineHeight={lineheight} base={basesize} scaleW={width} scaleH={height} pages=1 packed=0
page id=0 file="{filename}"
chars count={count}"""

LINE = u"""char id={id} x={x} y={y} width={w} height={h} xoffset={xo} yoffset={yo} xadvance={xa} page=0 chnl=0"""

PNG_DIR = r'D:\UserProfiles\fuyao\Desktop\images\image'  # 碎图文件目录
OUT_DIR = r'D:\UserProfiles\fuyao\Desktop\images\image_font' # 输入fnt文件的目录
OUT_FILENAME = 'num_clock'  # 输出的fnt文件名
WIDTH, HEIGHT = 0, 0  # 输出图片的尺寸
spacing = {'x': 1, 'y': 1}


def check_images_size():
    """
    计算仅一行情况下，合图的宽和高。多行的情况请手动修改宽高
    """
    max_height = 0
    total_width = 0
    for file in os.listdir(PNG_DIR):
        if not file.endswith('.png'):
            continue
        w, h = imagesize.get(os.path.join(PNG_DIR, file))
        total_width += w + spacing['x']
        if h > max_height:
            max_height = h
    total_width -= spacing['x']
    print("WIDTH, HEIGHT:", total_width, max_height)
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = total_width, max_height


def test():
    out = ''
    img = Image.new('RGBA', (WIDTH, HEIGHT))
    x = 0  # 下一个字符或字的x起始点
    y = 0  # 下一个字符或字的y起始点
    h = 0  # 每一行的高度，等于每一行中最高的字的高度
    n = 0  # 共多少个字符或字
    max_h = 0
    min_h = 1000
    for file in os.listdir(PNG_DIR):
        if file.endswith('.png'):
            char = Image.open(os.path.join(PNG_DIR, file))
            max_h = max(max_h, char.size[1])
            min_h = min(min_h, char.size[1])
    for file in os.listdir(PNG_DIR):
        if file.endswith('.png'):
            char = Image.open(os.path.join(PNG_DIR, file))
            if x + char.size[0] > WIDTH:
                x = 0
                y += h + spacing['y']
                h = 0
            img.paste(char, box=(x, y))
            print(file[:-4])
            out += LINE.format(id=ord(file[:-4]),
                               x=x,
                               y=y,
                               w=char.size[0],
                               h=char.size[1],
                               xo=0,
                               yo=math.ceil((max_h-char.size[1])*0.5),
                               xa=char.size[0]) + '\n'
            x += char.size[0] + spacing['x']
            h = max(h, char.size[1])
            n += 1
    img.save(os.path.join(OUT_DIR, OUT_FILENAME + '.png'))
    out = HEAD.format(typeface="arial",
                      unicode=1,
                      lineheight=max_h,
                      fontsize=20,
                      basesize=min_h,
                      count=n,
                      filename=OUT_FILENAME + ".png",
                      width=WIDTH,
                      height=HEIGHT) + '\n' + out
    print(out)
    with open(os.path.join(OUT_DIR, OUT_FILENAME + '.fnt'), 'w') as fw:
        fw.write(out)


if __name__ == '__main__':
    check_images_size()
    test()
