#!/usr/bin/env python

import xml.etree.ElementPath as EP
import xml.etree.ElementTree as ET


def xmlinsert(xpath, xmlfile, tag=".", findall=False):
    """Inserts elements from an xpath

    refs: xml.etree.ElementPath
          https://github.com/python/cpython/blob/3.7/Lib/xml/etree/ElementPath.py

    Args:
        xpath (str): xml elements separated by back slash
            (no whitespace outside of attributes)
        xmlfile (str): path to xml file; created if it doesn't exist
        tag (str): xml element to serve as parent (/ or . = root)
        findall (bool): If true finds all matching times matching tag
            and inserts xml elements from xpaths after deepest member
    Returns:
        str: location of updated xml file

    Notes:
        xpath (str): expects paths which only descend.  And supports
            the following symbols in xpath /()[]@= excludes (//, ..)
            ex. a[bar=/hello/world]/be[text()="there"]/can[@nope=there]/day

        tag (str): used by implementation of Elementree's iterfind function
            so see xml.etree.elementree for limitations.

    dev:
        if no pattern is provided:
        parse input through
        loop through list try to append subelement from previous subelement
        except catches failure and creates initial subelement in the
        in the specified root
        else:
        findall patterns of that satisfy pattern and add subelements to these
        use ET.Element.iterfind()
    """
    # import xml and convert to element
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    # no absolute paths
    if xpath[0] == "/":
        raise SyntaxError("Can't create another root directory in an xml file")
    token_iter = EP.xpath_tokenizer(xpath)
    # check recursive
    if findall:
        for element in root.iterfind(tag):
            elementinsert(token_iter, element)
    else:
        # if tag defined root replaced
        elementinsert(token_iter, root.find(tag))
    tree.write(xmlfile)
    return xmlfile

    # [tag] add to direct descendents
    # [tag='text'] add subelements with an xpath as text
    # add to all descendents


def elementinsert(token_iter, xmlelement):
    """takes element and adds subelements

    Args
        xpath (str): xml elements separated by back slash
        xmlelement (obj): element class from elementtree package

    Returns:
        Element Class

    Notes:
        Supports simple xpath syntax
    """
    try:
        token = next(token_iter)
    except StopIteration:
        return
    # if delimiter is a '/' skip token
    if token[0] == "" and len(token[1]) > 0:
        subelement = ET.SubElement(xmlelement, token[1])
        return elementinsert(token_iter, subelement)
    elif token[0] == "[":
        add_predicate(token_iter, xmlelement)
    elif token[0] == "]":
        return
    return elementinsert(token_iter, xmlelement)


def add_predicate(token_iter, xmlelement, predicate=[], modifiers=[]):
    """takes element and updates values

    Args
        xmlelement (obj: 'str'): element class from elementtree package
        token_iter (obj): iterator type object containing tuples of strings
        attribute_flag (str): determines whether input is attribute of
    Returns:
        (obj: 'str'): element class

    Notes:
        when we hit either ](base case) we resolve additions and end recursion
        we use signature to determine the course of action
          if signature has @ it's an attribute,
          if signature has () it's a value of the tag
          if signature has / or empty or [ it's an xpath
    """

    try:
        token = next(token_iter)
    except StopIteration:
        return
    # ] represents end of attributes
    if token[0] == "]":
        # Add property to xml object
        set_xml_attribute(modifiers, predicate, xmlelement)
        # Clear list
        modifiers.clear()
        predicate.clear()
        return
    # Maybe remove, only due to User Error
    elif token == ("", ""):
        if modifiers:
            # Add property to xml object
            set_xml_attribute(modifiers, predicate, xmlelement)
            # Clear list
            predicate.clear()
            modifiers.clear()
    elif token[0] == "":
        predicate.append(token[1])
    elif token[0] == "/":
        print(predicate[0])
        subelement = ET.SubElement(xmlelement, predicate[0])
        predicate.clear()
        modifiers.clear()
        return elementinsert(token_iter, subelement)
    elif token[1] == "":
        modifiers.append(token[0])
    else:
        raise SyntaxError("invalid character")
    return add_predicate(token_iter, xmlelement, predicate, modifiers)


def set_xml_attribute(signature, text, xmlelement):
    """set xml element attribute or text

    Args:
        signature (list): list of symbols dictating how text is handled
        text (list): list of strings
        xmlelement (obj: 'str'): element class from elementtree package
    Dev Notes:
        wip
    """
    identifier = "".join(signature)
    if identifier == "@=":
        xmlelement.set(text[0], text[1])
    elif identifier == "()=":
        xmlelement.text = text[1]
