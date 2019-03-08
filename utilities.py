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


def position_translation(row, column):
    column = ord(column.lower()) - 96
    row = int(row) - 1
    column = int(column) - 1
    return row, column
