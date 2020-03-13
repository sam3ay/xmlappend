import unittest
import xmlconfigparse
import xml.etree.ElementTree as ET


class XmlToDictTest(unittest.TestCase):
    """

    """

    @classmethod
    def setUpClass(cls):
        """Creates new xml file to test"""
        # Creates xml file to be modified by test
        root = ET.Element("root")
        foo = ET.SubElement(root, "foo")
        ET.SubElement(foo, "bar")
        ET.SubElement(foo, "bar")

        tree = ET.ElementTree(root)
        tree.write("test.xml")

        # Creates xml file to be tested against
        test_root = ET.Element("root")
        test_foo = ET.SubElement(test_root, "foo")
        ET.SubElement(test_foo, "bar")
        test_bar = ET.SubElement(test_foo, "bar")
        test_name = ET.SubElement(test_bar, "name")
        test_no = ET.SubElement(test_name, "no")
        ET.SubElement(test_no, "more")
        test_value = ET.SubElement(test_name, "value")
        test_name.text = "test"
        test_name.set("veg", "3")
        test_value.text = "total"
        test_tree = ET.ElementTree(test_root)
        test_tree.write("testcase.xml")

    def test_xmlinsert(self):
        """ Test module
        """
        xmlconfigparse.xmlinsert(
            "name[@veg=3 text()=test][no/more]/value[text()=total]",
            "test.xml",
            tag="foo/bar[last()]",
        )
        try:
            xmlroot = ET.parse("test.xml").getroot()
            xmltestroot = ET.parse("testcase.xml").getroot()
        except ET.ParseError:
            self.fail(msg="Xml Parse Error")
        xmlteststring = ET.tostring(xmlroot)
        xmltempstring = ET.tostring(xmltestroot)
        self.assertEqual(xmlteststring, xmltempstring, msg="Unexpected string returned")


if __name__ == "__main__":
    unittest.main()
