import os
import re
import json

PATH = '/Users/jeandanielpearson/Downloads/drapeaux2'

COLORS_LIST = {'0': 'black',
               '1': 'blue',
               '4': 'red',
               '6': 'yellow',
               '7': 'white',
               '14': 'green'}

TILE_LIST = [['0', '0', '1', '0', '1', '1', '0', '1', '0', '0'],
             ['0', '1', '1', '1', '1', '3', '0', '3', '0', '1'],
             ['0', '3', '1', '3', '1', '4', '0', '4', '0', '3'],
             ['1', '0', '3', '0', '3', '1', '1', '1', '1', '0'],
             ['1', '1', '3', '1', '3', '3', '1', '3', '1', '1'],
             ['1', '3', '3', '3', '3', '4', '1', '4', '1', '3'],
             ['3', '0', '4', '0', '4', '1', '3', '1', '3', '0'],
             ['3', '1', '4', '1', '4', '3', '3', '3', '3', '1'],
             ['3', '3', '4', '3', '4', '4', '3', '4', '3', '3'],
             ['0', '0', '4', '0', '4', '4', '0', '4', '0', '0']]

tab = []
flags = {}
for filename in os.listdir(PATH):
    reg_fig_file = re.compile("([A-z]\w+.fig)")
    reg_line_polyline = re.compile("2 2 -?\d* -?\d* -?\d* (-?\d*) -?\d* -?\d* -?\d* \d*\.\d* -?\d* -?\d* -?\d* -?\d* -?\d* -?\d*")
    reg_square = re.compile(" (\d+)[\s](\d+) (\d+)[\s](\d+) (\d+)[\s](\d+) (\d+)[\s](\d+) (\d+)[\s](\d+)")
    found_file = reg_fig_file.findall(filename)
    if len(found_file) > 0:
        print filename
        f = open(PATH + '/' + filename, 'r')
        polyline_color = None
        flag = [None] * 10
        for line in f:
            found_polyline = reg_line_polyline.findall(line)
            found_square = reg_square.findall(line)
            if len(found_polyline) > 0:
                polyline_color = COLORS_LIST.get(found_polyline[0])
            if len(found_square) > 0:
                tile_real_size = found_square[0]
                tile_usable_size = []
                for x in tile_real_size:
                    tile_usable_size.append(str((int(x)-400)/300))
                if str(tile_usable_size) not in tab:
                    tab.append(str(tile_usable_size))
                i = 0
                for tile in TILE_LIST:
                    if tile == tile_usable_size:
                        if flag[i] is not None:
                            raise Exception
                        flag[i] = polyline_color
                    i += 1
                polyline_color = 'fuck'
        f.close()
        flags[filename.replace('Flag_','').replace('.fig','')] = flag
json.dump(flags, open('flags', 'wb'))