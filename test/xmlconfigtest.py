import unittest
import xmlconfigparse
import xml.etree.ElementTree as ET
import xml.etree.ElementPath as EP


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

    def test_elementinset(self):
        """Test method insert subelements
        """
        element_test = ET.Element("test")
        element_temp = ET.Element("test")
        new_temp = ET.SubElement(element_temp, "new")
        ET.SubElement(new_temp, "insert")
        token_iter = EP.xpath_tokenizer("new/insert")
        xmlconfigparse.elementinsert(token_iter, element_test)

        element_temp_string = ET.tostring(element_temp)
        element_test_string = ET.tostring(element_test)
        self.assertEqual(
            element_test_string, element_temp_string, msg="Unexpected string returned"
        )

    def test_predicate(self):
        """Test predicate addition
        """
        element_test = ET.Element("test")
        element_temp = ET.Element("test")
        element_temp.text = "Hey"
        element_temp.set("val", "8")
        ET.SubElement(element_temp, "ins")

        token_iter = EP.xpath_tokenizer("@val=8]")
        xmlconfigparse.add_predicate(token_iter, element_test)
        token_iter = EP.xpath_tokenizer("text()=Hey]")
        xmlconfigparse.add_predicate(token_iter, element_test)
        token_iter = EP.xpath_tokenizer("ins/]")
        xmlconfigparse.add_predicate(token_iter, element_test)

        element_temp_string = ET.tostring(element_temp)
        element_test_string = ET.tostring(element_test)
        self.assertEqual(
            element_test_string, element_temp_string, msg="Unexpected string returned"
        )

    def test_attribute(self):
        """Test attribute setting
        """
        # template elements
        attrib_element = ET.Element("test")
        text_element = ET.Element("test")
        attrib_element.set("val", "4")
        text_element.text = "foo"

        # testing elements
        no_text_element = ET.Element("test")
        no_attrib_element = ET.Element("test")

        xmlconfigparse.set_xml_attribute(["@", "="], ["val", "4"], no_attrib_element)
        xmlconfigparse.set_xml_attribute(["()", "="], ["text", "foo"], no_text_element)

        element_attrib_string = ET.tostring(attrib_element)
        element_text_string = ET.tostring(text_element)
        no_attrib_string = ET.tostring(no_attrib_element)
        no_text_string = ET.tostring(no_text_element)
        self.assertEqual(
            element_text_string, no_text_string, msg="Unexpected string returned"
        )
        self.assertEqual(
            element_attrib_string, no_attrib_string, msg="Unexpected string returned"
        )


if __name__ == "__main__":
    unittest.main()
