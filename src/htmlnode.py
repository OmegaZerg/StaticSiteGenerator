import html

"""
HTMLNode class:
> This class will represent a "node" in an HTML document tree.
>> <p>This is a paragraph node</p>

> Outputs from objects of this class will be in HTML only.
> Child classes of HTMLNode:
>> LeafNode
>> ParentNode

> An HTMLNode without a tag will just render as raw text
> An HTMLNode without a value will be assumed to have children
> An HTMLNode without children will be assumed to have a value
> An HTMLNode without props simply won't have any attributes
> All values are optional and will default to None
"""

class HTMLNode():
    def __init__(self, tag=None, value=None, props=None, children=None):
        self.tag = tag  #String representation of the HTML tag itself: "p", "a", "h1", "b", "code", "i", "img"
        self.value = value  #String representation of the value/information to be contained within the tag.
        self.children = children  #A list of HTMLNode objects representing the children of this node (if any).
        self.props = props  #Dictionary Key/Value pairs representing the attributes for the HTML tag. Example: a link <a> tag might have {"href": "https://.google.com"}

    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        return False
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    #Children must implement this method
    def to_html(self):
        raise NotImplementedError
    
    #This method will return a string that represents the HTML attributes of the node. Only applicable for nodes that have attributes/props.
    """
    And example input:
    {
    "href": "https://www.google.com",
    "target": "_blank",
    }

    Would produce this output:
    " href="https://www.google.com" target="_blank"
    """
    def props_to_html(self):
        if not self.props:
            return ""
        attributes = []
        for key, value in self.props.items():
            if value is None:  # Skip props with None values
                continue
            attributes.append(f'{key}="{html.escape(str(value))}"')
        return " " + " ".join(attributes)
        #old code so issue with this code was is ONLY accepts strings as input. We COULD have an input of a number/integer so like "count": 5 ... and in cases like that it would fail to parse through the isinstance check
        return " " + " ".join(f'{html.escape(key)}="{html.escape(value)}"' for key, value in self.props.items() if isinstance(value, str))
        #old code before refactor, keeping for now
        kv_pairs = []
        if not self.props:
            return ""
        for k, v in self.props.items():
            kv_pairs.append(f' {k}="{v}"')
        full_string = "".join(kv_pairs)
        return full_string

"""
LeafNode Class:
> A LeafNode is a type of HTMLNode that represents a single HTML tag with no children. Example:
>> <p>This is a paragraph of text.</p>

> It is not possible to enter any children when creating this node object.
> Tag is required, but the None is acceptable.
> Value is required.
> Props is optional, default None
"""
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("Value cannot be None")
        super().__init__(tag, value, props, children=None)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

"""
ParentNode Class:
> The ParentNode class will handle the nesting of HTML nodes inside of one another. Any HTML node that is not a "leaf" node, is a "parent" node.
> Tag is required, and must not be None.
> Children is required, and must not be None
> Props is optional, default None
> There is no value for this object.

"""
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None or len(tag) < 1:
            raise ValueError("Tags cannot be None or empty")
        if not isinstance(children, list) or len(children) < 1:
            raise ValueError("Children must be a non-empty list")
        for child in children:
            if not isinstance(child, HTMLNode):
                raise ValueError("Children must be an HTMLNode object")
        self.tag = tag
        self.children = children
        self.props = props

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    
    def __eq__(self, other):
        if self.tag == other.tag and self.children == other.children and self.props == other.props:
            return True
        return False
        
    #Return a string representation of of the HTML tag of the node AND its children.
    def to_html(self):
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        