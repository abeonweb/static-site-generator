from functools import reduce
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props and len(self.props.items()) > 0:
            attributes=reduce(lambda acc, t: f"{acc} {t[0]}=\"{t[1]}\"", self.props.items(), "")
            return attributes
        return ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("must have a value")
        if self.tag == None:
            return f"{self.value}"
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == "" or self.tag == None:
            raise ValueError("must have a tag")
        if self.children == None or len(self.children) < 1:
            raise ValueError("There are no children nodes")
        
        node=f"<{self.tag}{self.props_to_html()}>"
        children_html = ""
        for child in self.children:
           children_html += child.to_html()
        node += children_html
        node += f"</{self.tag}>"
        return node
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"