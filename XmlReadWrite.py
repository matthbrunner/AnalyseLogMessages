# coding=utf-8
from xml.etree.ElementTree import ElementTree, Element, Comment, SubElement, tostring
import xml.dom.minidom as dom
import datetime


class ReadAndWriteXML:
    def __init__(self):
        self.message_log = {}

    def get_messages(self):
        return self.message_log

    def create_xml_file(self, document_path, message_log):
        tree = dom.Document()
        root = dom.Element('LogMessages')
        
        for key, value in message_log.items():
            element_tag = dom.Element('LogMessag')
            attr = dom.Attr("transformer")
            attr.value = str(key) # also sets nodeValue
            element_tag.setAttributeNode(attr)
            attr = dom.Attr("user.log")
            attr.value = str(value) # also sets nodeValue
            element_tag.setAttributeNode(attr)

            root.appendChild(element_tag)
            
        tree.appendChild(root)
        
        f = open(document_path, "w") 
        tree.writexml(f, "", "    ", "\n") 
        f.close()


    def read_xml_document(self, document_path):
        tree = ElementTree(file=document_path)
        root = tree.getroot()

        messages_dict = {}
        for child in root.iterfind('LogMessages/LogMessage'):
            transformer = child.attrib['transformer']
            user_message = child.attrib['user.log']
            messages_dict[transformer] = user_message

        self.message_log = messages_dict


