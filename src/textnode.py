from enum import Enum

#We only allow a TextNode class object to be created with one of the following Text Type enums.
class TextType(Enum):
    NORMAL = "Normal text"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

"""
TextNode class:
> This class will provide a way to represent all the different types of inline text.
> Utilizes the TextType Enum to enforce rules on which text type we will allow the class objects to be created with.
> Text is required.
> Text Type is required.
> URL is optional, default None.
"""

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text  #The text content of this node
        self.text_type = text_type  #The textype of this node, which is a member of the TextType Enum class
        self.url = url  #The URL of a link or image if applicable. Default is None

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def to_html(self):
        return self.text
