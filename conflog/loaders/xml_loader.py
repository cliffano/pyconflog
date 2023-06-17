"""XML configuration loader.
"""
import xml.etree.ElementTree as ET
from . import PARAMS

def load(conf_file: str) -> dict:
    """Get configuration values from XML file.
    """
    conf = {}
    with open(conf_file, 'r', encoding='utf-8') as stream:
        xml_tree = ET.ElementTree(ET.fromstring(stream.read()))
        conf_xml = xml_tree.getroot()
        for param in PARAMS:
            xml_elem = conf_xml.find(param)
            if xml_elem is not None:
                conf[param] = xml_elem.text
    return conf
