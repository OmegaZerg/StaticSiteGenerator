class HTMLNode():
    def __init__(self, tag=None, value=None, props=None, children=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        kv_pairs = []
        if self.props is None:
            return ""
        for k, v in self.props.items():
            kv_pairs.append(f' {k}="{v}"')
        full_string = "".join(kv_pairs)
        return full_string
    
"""
Values used for switch statements in the to html method below:
h1 - <h1></h1>
h2 - <h2></h2>
h3 - <h3></h3>
p - <p></p>
a - <a href="">text here</a>
b - <b></b>
i - <i></i> -italic
code - <code></code>
img - <img alt="Image description" src="link" />
"""

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props, children=None)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
        """ ***This is no-man's land, we dont talk about no-man's land***
        match (self.tag):
            case ("h1"):
                return f"<h1>{self.value}</h1>"
            case ("h2"):
                return f"<h2>{self.value}</h2>"
            case ("h3"):
                return f"<h3>{self.value}</h3>"
            case ("p"):
                return f"<p>{self.value}</p>"
            case ("a"):
                return f"<a{self.props_to_html()}>{self.value}</a>"
            case ("b"):
                return f"<b>{self.value}</b>"
            case ("i"):
                return f"<i>{self.value}</i>"
            case ("code"):
                return f"<code>{self.value}</code>"
            case ("img"):
                return f"img insert image stuff here... DO IT NOWWWW!!!"
            case _:
                raise Exception("unknown tag")

    """