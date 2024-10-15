class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
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
        return "".join(list(map(lambda x: f' {x[0]}="{x[1]}"',prop_list)))
    
    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
            
props = {
    "href": "https://www.google.com",
    "target": "_blank",
}
n = HTMLNode(tag="div", value="paragraph text", children=None, props=props)
print(n)