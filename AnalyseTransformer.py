# coding=utf-8
import logging.handlers
import os
import XmlReadWrite
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
    def replace_hash(self, line, character):
        result_dic = {}
        ori_line = line
        language_expression = [pos for pos, char in enumerate(line) if char == character]

        if len(language_expression) % 2 != 0:
            logging.error("odd number of char {} in message {}".format(character, line))
        else:
            temp_dict = {}
            for i in range(0, len(language_expression) - 1, 2):
                test = line[language_expression[i] + 1: language_expression[i + 1]]
                to_replace = '{}{:d}{}'.format(str('{'), int(test[:test.index('|')]), str('}'))
                temp_dict[line[language_expression[i]: language_expression[i + 1] + 1]] = to_replace

            for key, value in temp_dict.items():
                line = line.replace(str(key), str(value))

        return line

    # ---------------------------------------------------------------------------
    def read_all_lines_from_transformer(self, file, file_name, use_file_path = False):
        result_list = []

        # Open a file
        line = ""
        try:
            fo = open(file)
            for line in fo:
                if r'XFORM_PARM PARM_NAME="MESSAGE_TEXT"' in line:
                    tmp_line = line.replace(r'#! <XFORM_PARM PARM_NAME="MESSAGE_TEXT" PARM_VALUE="', '')
                    tmp_line = tmp_line.replace(r'"/>', '').strip()
                    temp_list = []
                    if use_file_path == True:
                        temp_list.append(os.path.basename(file_name).encode("utf-8"))
                    else:
                        temp_list.append(file.encode("utf-8"))
                    start_index = 5
                    temp_code = tmp_line[:4].strip()
                    if temp_code.isnumeric():
                        temp_list.append(tmp_line[:4])
                    else:
                        temp_list.append('')
                        start_index = 0
                    temp_list.append(tmp_line[start_index:].encode("utf-8"))
#                     result_list.append("{0}; {1}; {2}".format(os.path.basename(file_name), tmp_line[:4], tmp_line[5:]))
                    result_list.append(temp_list)

        except Exception as e:
            logging.fatal("Something went wrong %s %s" % (e, line))
            temp_list = []
            temp_list.append(file_name)
            result_list.append(temp_list)
        finally:
            # Close open file
            fo.close()

        return result_list

    # ---------------------------------------------------------------------------
    def write_all_messages_from_transformer(self, output, contents):
        file = open(output, "w")

        for content in contents:
            for items in content:
                file.write(str("{0}; {1}; {2}".format(items[0].decode("utf-8"),items[1], items[2].decode("utf-8")))+'\n')

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
            messages.append(at.read_all_lines_from_transformer(os.path.join(transformer_path, each_file), each_file), True)
        else:
            messages.append(at.read_all_lines_from_transformer(os.path.join(workbench_path, each_file), each_file), True)
     
    dct = {}
    if len(messages) > 0:
        at.write_all_messages_from_transformer(os.path.join(transformer_path, "test.csv"), messages)
        for message in messages:
            for items in message:
#                 print()
                # print("{0} {1}".format(items[1], items[2]))
                origin = "{0} {1}".format(items[1], items[2].decode("utf-8"))
                value = at.replace_hash(origin, '#')
                if origin not in dct:
                    dct[origin] = value
                                          

    # TODO: include methode [replace_hash_with_format]
    # TODO: Add method to replace the language file if it's different
#     transformer_path = r'C:\temp'
#     message_dict = {'1000 #0|$(GN_FIELD)#': '1000 {0}', '1001 #0|$(GN_FIELD)#': '1001 {0}'}
    xml_path = os.path.join(transformer_path, 'messages.xml')
    xrw = XmlReadWrite.ReadAndWriteXML()
    xrw.create_xml_file(xml_path, dct)
#     xrw.read_xml_document(xml_path)
#     mess = xrw.get_messages()
#     for k, v in mess.items():
#         print('{0} {1}'.format(k, v))
