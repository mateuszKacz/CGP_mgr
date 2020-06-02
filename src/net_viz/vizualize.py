import json
from tkinter import Tk, Canvas, ALL
import functools


def draw_net(_canvas, _coords, _data, _i):
    
    _canvas.delete(ALL)

    # create boxes
    for coords in _coords:

        _canvas.create_rectangle(coords)
        _canvas.create_text((coords[0]+coords[2])/2, (coords[1]+coords[3])/2, text=_data['net'][_i][_coords.index(coords)]['gate_func'])

    _canvas.after(500, draw_net, _canvas, _coords, _data, _i)

    # increment iterator
    _i += 1
    print(_i)


def calc_coords(_initial_cords, _rows, _columns, _row_spacing, _column_spacing):

    coordinates = []
    for column in range(_columns):
        for row in range(_rows):
            coords = (_initial_cords[0] + column * (_initial_cords[2] + _column_spacing),
                      _initial_cords[1] + row * (_initial_cords[3] + _row_spacing),
                      (column + 1) * _initial_cords[2] + _column_spacing * column,
                      (row + 1) * _initial_cords[3] + _row_spacing * row)

            coordinates.append(coords)
    return coordinates


def main():
    with open("viz_data.txt", 'r') as file:
        data = json.load(file)

    master = Tk()
    master.title("CGP")
    canvas = Canvas(master, width=1000, height=600)
    canvas.pack(fill='both')

    # boxes params
    initial_cords = (20, 20, 180, 100)
    rows = 5
    columns = 4
    row_spacing = 20
    column_spacing = 50

    i = 0

    coords = calc_coords(initial_cords, rows, columns, row_spacing, column_spacing)
    draw_net(canvas, coords, data, i)

    master.mainloop()


if __name__ == "__main__":
    main()
