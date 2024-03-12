import xlwings as xw

_fpattern_map = {
    'none': 0,  # xlNone
    'solid': 1,  # xlSolid
    'gray50': 2,  # xlGray50
    'gray75': 3,  # xlGray75
    'gray25': 4,  # xlGray25
    'horstripe': 5,  # xlHorizontalStripe
    'verstripe': 6,  # xlVerticalStripe
    'diagstripe': 8,  # xlDiagonalDown
    'revdiagstripe': 7,  # xlDiagonalUp
    'diagcrosshatch': 9,  # xlDiagonalCrosshatch
    'thinhorstripe': 11,  # xlThinHorizontalStripe
    'thinverstripe': 12,  # xlThinVerticalStripe
    'thindiagstripe': 14,  # xlThinDiagonalDown
    'thinrevdiagstripe': 13,  # xlThinDiagonalUp
    'thinhorcrosshatch': 15,  # xlThinHorizontalCrosshatch
    'thindiagcrosshatch': 16,  # xlThinDiagonalCrosshatch
    'thickdiagcrosshatch': 10,  # xlThickDiagonalCrosshatch
    'gray12p5': 17,  # xlGray12.5
    'gray6p25': 18  # xlGray6.25
}

wb = xw.Book('test.xlsx')
sheet = wb.sheets[0]
start_cell = 'C1'
row = sheet.range(start_cell).row
col = sheet.range(start_cell).column

for i, (key, value) in enumerate(_fpattern_map.items()):
    print(key, value)
    sheet.range(row+i, col).value = key
    sheet.range(row+i, col+1).api.Interior.Pattern = value
    i += 1


foreground_color = (255, 0, 255)
background_color = '#FF0000'
foreground_color_int = xw.utils.rgb_to_int(foreground_color)
background_color_int = xw.utils.hex_to_int(background_color)
# sheet.range(19, 4).api.Interior.PatternColor = '#FF0000'
sheet.range(19, 4).api.Interior.Color = background_color_int

# sheet.range(19, 3).font.color = '#FF0000'

import xlwings as xw

# Your existing code...

# Convert hexadecimal color to RGB values
background_color = background_color.lstrip('#')
red = int(background_color[:2], 16)
green = int(background_color[2:4], 16)
blue = int(background_color[4:], 16)

# Create the integer color value
background_color_int = red | (green << 8) | (blue << 16)

# Set the background color of the cell
cell.color = background_color_int

##
# 1. solid 用的是前景还是后景
# 2. 完善fill_pattern