from enum import Enum


class FileWriter:
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
    UPNE = 'Upper Position Not Empty'
    LPE = 'Lower Position Empty'
    OPE = 'Old Position Empty'
    CCPSL = 'Card can''t be placed at the same location'
    ORMAN = 'Only Recycle moves allowed now'
    CVE = 'Column value should be between A-H'
    RVE = 'Row value should be between 1-12'
    IIP = 'Invalid Input Position'
    NPNE = 'New Position not Empty'
    CSLCPRN = 'Cards still left, Can''t play recycling move now'
    CMLCPOP = 'Can''t move the last card played by the other player'
    IVE = "Input Value Error"


def position_translation(row, column):
    if column.isnumeric():
        raise ValueError('Column value should be an alphabet')
    if row.isalpha():
        raise ValueError('Row value should be numeric')

    column = ord(column.lower()) - 96
    column = int(column) - 1
    row = int(row) - 1
    return row, column


