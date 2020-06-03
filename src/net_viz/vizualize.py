import json
from tkinter import Tk, Canvas, ALL


def draw_net(_canvas, _box_coords, _center_coords, _entry_coords, _output_coords, _data, _i):
    """
    Method redraws the whole net on the Canvas in every iteration.
    :param _canvas: tkinter Canvas object
    :param _box_coords: coordinates of the boxes to plot (coordinates of the corners to be specific)
    :param _center_coords: coordinates of the center of the boxes
    :param _entry_coords: coordinates of the entry point of a connection
    :param _output_coords: coordinates of the output point of a connection
    :param _data: data from simulation, json format, holds data about every step of the simulation
    :param _i: iterator of the simulation used mainly to filter the _data object
    :return: None
    """
    # clear the Canvas
    _canvas.delete(ALL)

    # create boxes
    for coords in _box_coords:

        _canvas.create_rectangle(coords, outline="lightgray")

    # create text in boxes
    for coords in _center_coords:
        _canvas.create_text(coords[0], coords[1], text=_data['net'][_i][_center_coords.index(coords)]['gate_func'])

    # create connections between Gates
    for gate_number in range(5, len(_center_coords)):
        _canvas.create_line(_entry_coords[gate_number][0], _entry_coords[gate_number][1],
                            _output_coords[_data['net'][_i][gate_number]['active_input_index'][0]][0],
                            _output_coords[_data['net'][_i][gate_number]['active_input_index'][0]][1], fill="lightgray")

        _canvas.create_line(_entry_coords[gate_number][0], _entry_coords[gate_number][1],
                            _output_coords[_data['net'][_i][gate_number]['active_input_index'][1]][0],
                            _output_coords[_data['net'][_i][gate_number]['active_input_index'][1]][1], fill="lightgray")

    # draw actual best subnet
    net_crawl(_canvas, _box_coords, _center_coords,_entry_coords, _output_coords, _data['net'][_i], _data['params'][_i])

    # draw parameters
    _canvas.create_text(300, 10, text='Obj func: {:.3f} \t Annealing param value: {:.2f}'.
                        format(_data['params'][_i]['potential'], _data['params'][_i]['temperature']))

    # increment iterator
    _i += 1

    # next frame
    if _i < len(_data['net']):
        _canvas.after(500, draw_net, _canvas, _box_coords, _center_coords, _entry_coords, _output_coords, _data, _i)


def net_crawl(_canvas, _box_coords, _center_coords, _entry_coords, _output_coords, _net, _params):
    """
    This method is a crawler through the Net to find all the gates which form actual solution.
    :param _canvas: tkinter Canvas object
    :param _box_coords: coordinates of the boxes to plot (coordinates of the corners to be specific)
    :param _center_coords: coordinates of the center of the boxes
    :param _entry_coords: coordinates of the entry point of a connection
    :param _output_coords: coordinates of the output point of a connection
    :param _net: Net data from actual step of simulation, json format
    :param _params: actual parameters of the simulation
    :return:
    """

    gates = [_params['output_gate_index']]

    _canvas.create_text((_center_coords[gates[0]][0], _center_coords[gates[0]][1] + 20), text="OUTPUT GATE")

    while gates:
        _canvas.create_rectangle(_box_coords[gates[0]])
        _canvas.create_line(_entry_coords[gates[0]][0], _entry_coords[gates[0]][1],
                            _output_coords[_net[gates[0]]['active_input_index'][0]][0],
                            _output_coords[_net[gates[0]]['active_input_index'][0]][1],
                            )
        _canvas.create_line(_entry_coords[gates[0]][0], _entry_coords[gates[0]][1],
                            _output_coords[_net[gates[0]]['active_input_index'][1]][0],
                            _output_coords[_net[gates[0]]['active_input_index'][1]][1],
                            )

        if _net[gates[0]]['active_input_index'][0] > 4:
            gates.append(_net[gates[0]]['active_input_index'][0])
        if _net[gates[0]]['active_input_index'][1] > 4:
            gates.append(_net[gates[0]]['active_input_index'][1])

        gates.pop(0)


def calc_coords(_initial_cords, _rows, _columns, _row_spacing, _column_spacing):
    """
    Method calculates coordinates for future graphics creation
    :param _initial_cords: coordinates of the first box
    :param _rows: number of rows
    :param _columns: number of columns
    :param _row_spacing: space between boxes vertically
    :param _column_spacing: space between boxes horizontally
    :return: list of lists
    """

    box_coords = []
    for column in range(_columns):
        for row in range(_rows):
            coords = (_initial_cords[0] + column * (_initial_cords[2] + _column_spacing),
                      _initial_cords[1] + row * (_initial_cords[3] + _row_spacing),
                      (column + 1) * _initial_cords[2] + _column_spacing * column,
                      (row + 1) * _initial_cords[3] + _row_spacing * row)

            box_coords.append(coords)
    # calc box-center coords
    center_coords = [((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2) for coords in box_coords]
    # calc box entry coords
    entry_coords = [(coords[0], coords[1] + _initial_cords[3]/2 - _row_spacing/2) for coords in box_coords]
    # calc box output coords
    output_coords = [(coords[2], coords[1] + _initial_cords[3]/2 - _row_spacing/2) for coords in box_coords]

    return box_coords, center_coords, entry_coords, output_coords


def main():
    with open("viz_data.txt", 'r') as file:
        data = json.load(file)

    master = Tk()
    master.title("CGP")
    canvas = Canvas(master, width=1000, height=600)
    canvas.pack(fill='both')

    # box-grid parameters
    initial_cords = (20, 20, 180, 100)
    rows = 5
    columns = 4
    row_spacing = 20
    column_spacing = 50

    i = 0
    # calc box coords
    box_coords, center_coords, entry_coords, output_coords = calc_coords(initial_cords, rows, columns, row_spacing, column_spacing)

    draw_net(canvas, box_coords, center_coords, entry_coords, output_coords, data, i)

    master.mainloop()


if __name__ == "__main__":
    main()
