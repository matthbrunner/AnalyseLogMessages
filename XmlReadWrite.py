from xml.etree.ElementTree import ElementTree, Element, Comment, SubElement, tostring
# from ElementTree_pretty import prettify
import datetime


class ReadAndWriteXML:
    def __init__(self):
        pass

    @staticmethod
    def create_xml_file(self, document_path, message_log):
        root = Element('LogMessages')

        comment = Comment('This XML Document was created at {0}'.format(datetime.datetime.now()))
        root.append(comment)

        child = SubElement(root, 'LogMessages')

        # TODO: how to add the new node after?
        for key, value in message_log.items():
            sub_child = SubElement(child, 'LogMessage')
            sub_child.set('transformer', key)
            sub_child.set('user.log', value)

        print(tostring(root))

        tree = ElementTree(root)
        tree.write(document_path)
