from enum import Enum


"""
==========
utilities
==========
This module contains classes and functions required for the non-functional work.

Contents
--------
* FileWriter - A class to open and write to the trace file.
* GameError - An enumeration class stating all possible game errors.
* PlayerType - An enumeration class stating player type.
* PreferenceType - An enumeration class stating player preference type.
* open_file_writer() - A static method to open the FileWriter for the trace file.
* write_to_trace_file() - A static method to write to the trace file.
* position_translation() - Function to translate the card position value to Python specific value.

"""


class FileWriter:
    """
    Instance represent a FileWriter Object.
    ===========
    Description
    ===========
    contains logic to open and write to the trace file.
    """
    print_trace_file = False
    file_name = 'trace_file'

    @staticmethod
    def open_file_writer():
        with open(FileWriter.file_name, 'w') as file:
            file.write('')

    @staticmethod
    def write_to_trace_file(heuristic_eval_count, current_level_heuristic_value, level2_heuristic_values):
        if FileWriter.print_trace_file:
            with open(FileWriter.file_name, 'a') as file:
                file.write(str(heuristic_eval_count) + '\n')
                file.write(str(current_level_heuristic_value) + '\n\n')
                for level2_value in level2_heuristic_values:
                    file.write(str(level2_value) + '\n')
                file.write('\n')


class GameError(Enum):
    UPNE = 'Upper position should be empty'
    LPE = 'Lower Position should not be empty'
    CVE = 'Column value should be between A-H'
    RVE = 'Row value should be between 1-12'
    IIP = 'Invalid Input Position'
    NPNE = 'New Position should be empty'
    IVE = "Input Value Error"
    CSLCPRN = 'Cards still left, Can''t play recycling move now'
    CMLCPOP = 'Recycle move: Can''t move the last card played by the other player'
    OPE = 'Recycle move: Previous position is empty'
    CCPSL = 'Recycle move: Card can''t be placed at the same location'
    ORMAN = 'Recycle move: Only recycle moves allowed now'
    IRV = 'Rotation Value should be between 1-8'
    FCE = 'Valid values for the first character are 0 for a regular move and A-H for a recycle move'
    RMOPE = 'Recycle move: New position should not be over the old position'
    ICP = 'Invalid card position'
    AIGIM = 'AI generated Invalid move'


def position_translation(row, column):
    if column.isnumeric():
        raise ValueError('Column value should be an alphabet')
    if row.isalpha():
        raise ValueError('Row value should be numeric')

    column = ord(column.lower()) - 96
    column = int(column) - 1
    row = int(row) - 1
    return row, column


class PlayerType(Enum):
    H = 'Human'
    AI = 'AI'


class PreferenceType(Enum):
    D = 'DOT'
    C = 'COLOR'
