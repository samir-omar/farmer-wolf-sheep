# movement.py
def get_coords(item, side):
    # تحديد مكان كل عنصر بناءً على جانبه (0 يسار، 1 يمين)
    base_y = 350
    positions = {
        'farmer': [50, 650],
        'wolf': [100, 700],
        'sheep': [150, 750],
        'cabbage': [20, 600]
    }
    return (positions[item][side], base_y)