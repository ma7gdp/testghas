from lxml import etree

xml_data = input("Enter XML: ")
parser = etree.XMLParser(resolve_entities=True, load_dtd=True)
root = etree.fromstring(xml_data.encode("utf-8"), parser=parser)
print(root.tag)
