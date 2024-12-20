class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html not implemented")

    def props_to_html(self):
        if self.props == None:
            return ""
        prop_list = list(self.props.items())
        return "".join(list(map(lambda x: f' {x[0]}="{x[1]}"', prop_list)))

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag=tag, value=value, props=props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError("value property not set for LeafNode instance")

        if self.tag == None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def __eq__(self, value) -> bool:
        return self.tag == value.tag and self.value == value.value and self.props == value.props


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.children == None:
            raise ValueError("children property not set for ParentNode instance")
        
        if self.tag == None:
            raise ValueError("tag property not set for ParentNode instance")
        
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        node_html = f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
        
        return node_html
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

    
