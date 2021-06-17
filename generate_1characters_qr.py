#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse

from amzqr import amzqr
from PIL import Image, ImageDraw, ImageFont


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--font', type=str, default='font/umefont_670/ume-ugo5.ttf')

    parser.add_argument('-c', '--character', type=str, default=' ')
    parser.add_argument('-cc', '--character_color', help='r,g,b,y,m,c,p', type=str, default=None)

    parser.add_argument('-w', '--words', type=str, default='')
    parser.add_argument('-v', '--version', help='1,2,3,...,40', type=int, default=3)
    parser.add_argument('-l', '--level', help='L,M,Q,H', type=str, default='H')
    parser.add_argument('-n', '--save_name', type=str, default='qr.png')
    parser.add_argument('-d', '--save_dir', type=str, default=None)

    args = parser.parse_args()

    return args
 
def get_font_color(character_color):
    color_sets = [
        ['r', 'red'],
        ['g', 'lime'],
        ['b', 'blue'],
        ['y', 'yellow'],
        ['m', 'magenta'],
        ['c', 'cyan'],
        ['p', 'purple'],
    ]
    
    color = 'black'
    colorized = False

    for color_set in color_sets:
        if color_set[0] == character_color:
            color = color_set[1]
            colorized = True
            break
    
    return color, colorized

def generate_1charactes_qr(
    font_path,
    character,
    character_color,
    words,
    version,
    level,
    save_name,
    save_dir,
):
    # 文字画像 #################################################################
    temp_file_name = '_temp_generate_character_image.png'
    temp_image = Image.new('RGB', (500, 500), 'white')

    # 文字色
    color, colorized = get_font_color(character_color)

    draw = ImageDraw.Draw(temp_image)
    font = ImageFont.truetype(font_path, 340)
    draw.text(
        (350, 330),
        character[0],
        font=font,
        fill=color,
        anchor='mm'
    )

    temp_image.save(temp_file_name)

    # QRコード生成 #############################################################
    if save_dir is None:
        save_dir = os.getcwd()

    generate_version, generate_level, _ = amzqr.run(
        words,
        version=version,
        level=level,
        picture=temp_file_name,
        colorized=colorized,
        contrast=1.0,
        brightness=1.0,
        save_name=save_name,
        save_dir=save_dir,
    )
    print('Version:' + str(generate_version), end=', ')
    print('Level:' + str(generate_level), end=', ')
    print('Words:' + words, end=', ')
    print('Character:' + str(character[0]))

    # 一時ファイル削除 ##########################################################
    os.remove(temp_file_name)

def main():
    # 引数解析 #################################################################
    args = get_args()

    font_path = args.font

    character = args.character
    character_color = args.character_color

    words = args.words
    version = args.version
    level = args.level
    save_name = args.save_name
    save_dir = args.save_dir

    # QRコード生成 #############################################################
    generate_1charactes_qr(
        font_path,
        character,
        character_color,
        words,
        version,
        level,
        save_name,
        save_dir,
    )

def test():
    # 引数解析 #################################################################
    args = get_args()

    font_path = args.font

    versions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    level = 'H'
    words = 'test'
    # characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '"', '#', '$', '%', '&', "'", '(', ')', '-', '=', '^', '~', '|', ';', ':', '+', '*', '@', '`', '[', ']', '{', '}', '?', '/', ' ']
    characters = ['A']
    # character_colors = [' ', 'r', 'g', 'b', 'y', 'm', 'c', 'p']
    character_colors = [None]
    save_name = 'test'
    save_dir = 'test'

    os.makedirs(save_dir, exist_ok=True)

    # QRコード生成 #############################################################
    count = 0
    for version in versions:
        for character in characters:
            for character_color in character_colors:
                generate_1charactes_qr(
                    font_path,
                    character,
                    character_color,
                    words,
                    version,
                    level,
                    save_name + str(count).zfill(4) + '.png',
                    save_dir,
                )

            count += 1

if __name__ == '__main__':
    # main()
    test()