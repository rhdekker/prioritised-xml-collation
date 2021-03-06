
# parse xml file
import re
from xml.dom.pulldom import CHARACTERS, START_ELEMENT, END_ELEMENT, parse

from prioritised_xml_collation.tokenizer import Stack


class Token(object):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.content


class TextToken(Token):
    def __init__(self, content, annot_info):
        self.annot_info = annot_info
        super(TextToken, self).__init__(content)


class AnnotationInformation(object):
    # TODO possible other fields are attribute, namespace (textual content?)
    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __str__(self):
        return self.tag_name

    def __repr__(self):
        return self.tag_name


def convert_xml_file_into_tokens(xml_filename):
    doc = parse(xml_filename)
    return convert_xml_doc_into_tokens(doc)


# convert xml document into tokens
def convert_xml_doc_into_tokens(xml_doc):
    tokens = []
    # keep administration with stack
    open_tags_in_witness = Stack()
    annot_info = None
    for event, node in xml_doc:
        if event == CHARACTERS:
            tokens.extend(tokenize_text(node.data, annot_info))
        elif event == START_ELEMENT:
            annot_info = AnnotationInformation(node.tagName)
            # append item annot_info to stack list
            open_tags_in_witness.push(annot_info)
        elif event == END_ELEMENT:
            # retrieve item from top of stack
            open_tags_in_witness.pop()
            if open_tags_in_witness:
                annot_info = open_tags_in_witness.peek()

    return tokens


# tokenize text
# data adds text to current element; data is a string
def tokenize_text(data, annot_info):
    return (TextToken(content, annot_info) for content in re.findall(r'\w+|[^\w\s]+', data))

# returns list of text token objects
