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
        ('r', 'red'),
        ('g', 'lime'),
        ('b', 'blue'),
        ('y', 'yellow'),
        ('m', 'magenta'),
        ('c', 'cyan'),
        ('p', 'purple'),
    ]
    
    color = 'black'
    colorized = False

    for color_set in color_sets:
        if color_set[0] == character_color:
            color = color_set[1]
            colorized = True
            break
    
    return color, colorized


def analyse_version(version, level, words):
    num_list = '0123456789'
    alphanum_list = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:'
    mode_index_list = {'numeric':0, 'alphanumeric':1, 'byte':2, 'kanji':3}

    version_set = {
        'L': [(41, 25, 17, 10), (77, 47, 32, 20), (127, 77, 53, 32), (187, 114, 78, 48), (255, 154, 106, 65), (322, 195, 134, 82), (370, 224, 154, 95), (461, 279, 192, 118), (552, 335, 230, 141), (652, 395, 271, 167), (772, 468, 321, 198), (883, 535, 367, 226), (1022, 619, 425, 262), (1101, 667, 458, 282), (1250, 758, 520, 320), (1408, 854, 586, 361), (1548, 938, 644, 397), (1725, 1046, 718, 442), (1903, 1153, 792, 488), (2061, 1249, 858, 528), (2232, 1352, 929, 572), (2409, 1460, 1003, 618), (2620, 1588, 1091, 672), (2812, 1704, 1171, 721), (3057, 1853, 1273, 784), (3283, 1990, 1367, 842), (3517, 2132, 1465, 902), (3669, 2223, 1528, 940), (3909, 2369, 1628, 1002), (4158, 2520, 1732, 1066), (4417, 2677, 1840, 1132), (4686, 2840, 1952, 1201), (4965, 3009, 2068, 1273), (5253, 3183, 2188, 1347), (5529, 3351, 2303, 1417), (5836, 3537, 2431, 1496), (6153, 3729, 2563, 1577), (6479, 3927, 2699, 1661), (6743, 4087, 2809, 1729), (7089, 4296, 2953, 1817)],
        'M': [(34, 20, 14, 8), (63, 38, 26, 16), (101, 61, 42, 26), (149, 90, 62, 38), (202, 122, 84, 52), (255, 154, 106, 65), (293, 178, 122, 75), (365, 221, 152, 93), (432, 262, 180, 111), (513, 311, 213, 131), (604, 366, 251, 155), (691, 419, 287, 177), (796, 483, 331, 204), (871, 528, 362, 223), (991, 600, 412, 254), (1082, 656, 450, 277), (1212, 734, 504, 310), (1346, 816, 560, 345), (1500, 909, 624, 384), (1600, 970, 666, 410), (1708, 1035, 711, 438), (1872, 1134, 779, 480), (2059, 1248, 857, 528), (2188, 1326, 911, 561), (2395, 1451, 997, 614), (2544, 1542, 1059, 652), (2701, 1637, 1125, 692), (2857, 1732, 1190, 732), (3035, 1839, 1264, 778), (3289, 1994, 1370, 843), (3486, 2113, 1452, 894), (3693, 2238, 1538, 947), (3909, 2369, 1628, 1002), (4134, 2506, 1722, 1060), (4343, 2632, 1809, 1113), (4588, 2780, 1911, 1176), (4775, 2894, 1989, 1224), (5039, 3054, 2099, 1292), (5313, 3220, 2213, 1362), (5596, 3391, 2331, 1435)],
        'Q': [(27, 16, 11, 7), (48, 29, 20, 12), (77, 47, 32, 20), (111, 67, 46, 28), (144, 87, 60, 37), (178, 108, 74, 45), (207, 125, 86, 53), (259, 157, 108, 66), (312, 189, 130, 80), (364, 221, 151, 93), (427, 259, 177, 109), (489, 296, 203, 125), (580, 352, 241, 149), (621, 376, 258, 159), (703, 426, 292, 180), (775, 470, 322, 198), (876, 531, 364, 224), (948, 574, 394, 243), (1063, 644, 442, 272), (1159, 702, 482, 297), (1224, 742, 509, 314), (1358, 823, 565, 348), (1468, 890, 611, 376), (1588, 963, 661, 407), (1718, 1041, 715, 440), (1804, 1094, 751, 462), (1933, 1172, 805, 496), (2085, 1263, 868, 534), (2181, 1322, 908, 559), (2358, 1429, 982, 604), (2473, 1499, 1030, 634), (2670, 1618, 1112, 684), (2805, 1700, 1168, 719), (2949, 1787, 1228, 756), (3081, 1867, 1283, 790), (3244, 1966, 1351, 832), (3417, 2071, 1423, 876), (3599, 2181, 1499, 923), (3791, 2298, 1579, 972), (3993, 2420, 1663, 1024)],
        'H': [(17, 10, 7, 4), (34, 20, 14, 8), (58, 35, 24, 15), (82, 50, 34, 21), (106, 64, 44, 27), (139, 84, 58, 36), (154, 93, 64, 39), (202, 122, 84, 52), (235, 143, 98, 60), (288, 174, 119, 74), (331, 200, 137, 85), (374, 227, 155, 96), (427, 259, 177, 109), (468, 283, 194, 120), (530, 321, 220, 136), (602, 365, 250, 154), (674, 408, 280, 173), (746, 452, 310, 191), (813, 493, 338, 208), (919, 557, 382, 235), (969, 587, 403, 248), (1056, 640, 439, 270), (1108, 672, 461, 284), (1228, 744, 511, 315), (1286, 779, 535, 330), (1425, 864, 593, 365), (1501, 910, 625, 385), (1581, 958, 658, 405), (1677, 1016, 698, 430), (1782, 1080, 742, 457), (1897, 1150, 790, 486), (2022, 1226, 842, 518), (2157, 1307, 898, 553), (2301, 1394, 958, 590), (2361, 1431, 983, 605), (2524, 1530, 1051, 647), (2625, 1591, 1093, 673), (2735, 1658, 1139, 701), (2927, 1774, 1219, 750), (3057, 1852, 1273, 784)]
    }
    
    if all(i in num_list for i in words):
        mode = 'numeric'
    elif all(i in alphanum_list for i in words):
        mode = 'alphanumeric'
    else:
        mode = 'byte'

    mode_index = mode_index_list[mode]
    words_length = len(words)

    for temp_version in range(40):
        if version_set[level][temp_version][mode_index] > words_length:
            version = temp_version + 1 if temp_version + 1 > version else version
            break

    return version


def get_image_size_info(version):
    image_size_info_list = [
        (261, 175, (175, 175)),
        (297, 220, (200, 190)),
        (333, 275, (200, 200)),
        (369, 300, (220, 220)),
        (405, 330, (230, 230)),
        (441, 353, (265, 265)),
        (477, 382, (286, 286)),
        (513, 410, (308, 308)),
        (549, 439, (329, 329)),
        (585, 468, (351, 351)),
        (621, 497, (373, 373)),
        (657, 526, (394, 394)),
        (693, 554, (416, 416)),
        (729, 583, (437, 437)),
        (765, 612, (459, 459)),
        (801, 641, (481, 481)),
        (837, 670, (502, 502)),
        (873, 698, (524, 524)),
        (909, 727, (545, 545)),
        (945, 756, (567, 567)),
        (981, 785, (589, 589)),
        (1017, 814, (610, 610)),
        (1053, 842, (632, 632)),
        (1089, 871, (653, 653)),
        (1125, 900, (675, 675)),
        (1161, 929, (697, 697)),
        (1197, 958, (718, 718)),
        (1233, 986, (740, 740)),
        (1269, 1015, (761, 761)),
        (1305, 1044, (783, 783)),
        (1341, 1073, (805, 805)),
        (1377, 1102, (826, 826)),
        (1413, 1130, (848, 848)),
        (1449, 1159, (869, 869)),
        (1485, 1188, (891, 891)),
        (1521, 1217, (913, 913)),
        (1557, 1246, (934, 934)),
        (1593, 1274, (956, 956)),
        (1629, 1303, (977, 977)),
        (1665, 1332, (999, 999)),
    ]

    image_size_info = image_size_info_list[version - 1]

    return image_size_info


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
    # QRコードバージョン確認 ####################################################
    version = analyse_version(version, level, words)

    # 文字画像 #################################################################
    image_size_info = get_image_size_info(version)
    image_length = image_size_info[0]
    font_size = image_size_info[1]
    font_point = image_size_info[2]

    temp_file_name = '_temp_generate_character_image.png'
    temp_image = Image.new('RGB', (image_length, image_length), 'white')

    # 文字色
    color, colorized = get_font_color(character_color)

    draw = ImageDraw.Draw(temp_image)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(
        font_point,
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
    characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '"', '#', '$', '%', '&', "'", '(', ')', '-', '=', '^', '~', '|', ';', ':', '+', '*', '@', '`', '[', ']', '{', '}', '?', '/', ' ']
    character_colors = [None]  # character_colors = [' ', 'r', 'g', 'b', 'y', 'm', 'c', 'p']
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
    main()
    # test()