"""XML file configuration loader for conflog."""

import xml.etree.ElementTree as ET
from . import PARAMS


def load(conf_file: str) -> dict:
    """Load configuration values from an XML file.

    Matches direct child elements of the root node against :data:`PARAMS` and
    returns their text content.

    :param conf_file: Path to the XML configuration file.
    :type conf_file: str
    :returns: Dict of configuration parameters found in the file.
    :rtype: dict
    """
    conf = {}
    with open(conf_file, "r", encoding="utf-8") as stream:
        xml_tree = ET.ElementTree(ET.fromstring(stream.read()))
        conf_xml = xml_tree.getroot()
        for param in PARAMS:
            xml_elem = conf_xml.find(param)
            if xml_elem is not None:
                conf[param] = xml_elem.text
    return conf
