import html

class HTMLNode():
    def __init__(self, tag=None, value=None, props=None, children=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        return False
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError
    
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
        
    def to_html(self):
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        