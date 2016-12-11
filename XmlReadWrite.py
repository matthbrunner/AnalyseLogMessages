from xml.etree.ElementTree import ElementTree, Element, Comment, SubElement, tostring
from xml.dom import minidom
import datetime


class ReadAndWriteXML:
    def __init__(self):
        self.message_log = {}

    def get_messages(self):
        return self.message_log

    def create_xml_file(self, document_path, message_log):
        root = Element('LogMessages')

        comment = Comment('This XML Document was created at {0}'.format(datetime.datetime.now()))
        root.append(comment)

        child = SubElement(root, 'LogMessages')

        for key, value in message_log.items():
            sub_child = SubElement(child, 'LogMessage')
            sub_child.set('transformer', key)
            sub_child.set('user.log', value)

        print(tostring(root))

        tree = ElementTree(root)
        tree.write(document_path)

    def read_xml_document(self, document_path):
        tree = ElementTree(file=document_path)
        root = tree.getroot()

        messages_dict = {}
        for child in root.iterfind('LogMessages/LogMessage'):
            transformer = child.attrib['transformer']
            user_message = child.attrib['user.log']
            messages_dict[transformer] = user_message

        self.message_log = messages_dict


