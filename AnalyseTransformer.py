# coding=utf-8
import logging.handlers
import os
from fnmatch import fnmatch


class AnalyseTransformer:
    # ---------------------------------------------------------------------------
    def __init__(self):
        self.logger_configuration()

    @staticmethod
    def logger_configuration():
        # Set up a specific logger with the desired output level
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        # Set the output logfile name and location
        handler = logging.handlers.RotatingFileHandler('analyseTransformer.log', maxBytes=10485760, backupCount=5)
        logger.addHandler(handler)
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

    # ---------------------------------------------------------------------------
    def read_all_files_in_folder(self, path, extension):
        result_list = []
        for file in os.listdir(path):
            if file.endswith(extension):
                result_list.append(os.path.join(path, file))

        return result_list

    # ---------------------------------------------------------------------------
    def replace_hash_with_format(self, line, character):
        dict = {}
        language_expression = [pos for pos, char in enumerate(line) if char == character]

        if len(language_expression) % 2 != 0:
            logging.error("odd number of char {} in message {}".format(character, line))
        else:
            for i in range(0, len(language_expression) - 1, 2):
                test = line[language_expression[i] + 1: language_expression[i + 1]]
                to_replace = '{}{:d}{}'.format(str('{'), int(test[:test.index('|')]), str('}'))
                dict[line[language_expression[i]: language_expression[i + 1] + 1]] = to_replace

            for key, value in dict.items():
                line = line.replace(str(key), str(value))

        return dict

    # ---------------------------------------------------------------------------
    def read_all_lines_from_transformer(self, file, file_name):
        result_list = []
        result_dict = {}

        # Open a file
        line = ""
        try:
            fo = open(file)
            for line in fo:
                if r'XFORM_PARM PARM_NAME="MESSAGE_TEXT"' in line:
                    tmp_line = line.replace(r'#! <XFORM_PARM PARM_NAME="MESSAGE_TEXT" PARM_VALUE="', '')
                    tmp_line = tmp_line.replace(r'"/>', '')
                    result_list.append("{0}; {1}; {2}".format(os.path.basename(file_name), tmp_line[:4], tmp_line[5:]))

        except Exception as e:
            logging.fatal("Something went wrong %s %s" % (e, line))
            result_list.append(file_name)
        finally:
            # Close open file
            fo.close()

        return result_list

    # ---------------------------------------------------------------------------
    def write_all_messages_from_transformer(self, output, content):
        file = open(output, "w")

        # file.write(transformer)
        for c in content:
            for e in c:
                if '\n' in e:
                    file.write(str(e))
                else:
                    file.write(str(e)+'\n')

        file.close()

    # ---------------------------------------------------------------------------
    def get_all_workbenches(self, root, pattern, result_list):
        for path, subdirs, files in os.walk(root):
            for name in files:
                if fnmatch(name, pattern):
                    result_list.append(os.path.join(path, name))
                    # print(os.path.join(path, name))

        return result_list


# ---------------------------------------------------------------------------
# -- START the process----
if __name__ == '__main__':
    at = AnalyseTransformer()

    logging.info("--! START Read Transformers")

    transformer_path = r"C:\Users\brma\Documents\FME\Transformers"
    workbench_path = r'C:\Workspace\ArcProjects\GNDC_Workshop\media'
    transformer_extension = ".fmx"
    workbench_extension = "*.fmw"

    file_list = []
    file_list = at.read_all_files_in_folder(transformer_path, transformer_extension)
    file_list = at.get_all_workbenches(workbench_path, workbench_extension, file_list)

    messages = []
    for each_file in file_list:
        logging.debug(each_file)
        if each_file.endswith(transformer_extension):
            messages.append(at.read_all_lines_from_transformer(os.path.join(transformer_path, each_file), each_file))
        else:
            messages.append(at.read_all_lines_from_transformer(os.path.join(workbench_path, each_file), each_file))

    if len(messages) > 0:
        at.write_all_messages_from_transformer(os.path.join(transformer_path, "test.csv"), messages)

    # TODO: include methode [replace_hash_with_format]
    # TODO: Add method to replace the language file if it's different
