class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
       self.tag = tag
       self.value = value
       self.children = children
       self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        '''
        string_props = ""
        if self.props is None:
            return string_props
        for key in self.props:
            string_props.append(f" {key[1:-1]}={self.props[key]}")
        return string_props
        '''
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("invalid HTML: no value")
        elif self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        leaf = LeafNode("b", "Bold text")
        if self.tag is None:
            raise ValueError("invalid HTML for parent: no value")
        elif self.children is None:
            raise ValueError("invalid HTML for parent: no children")
        else:
            string_value = ""
            if not isinstance(self.children, list):
                self.children = [self.children] 
            for child in self.children:
                string_value += child.to_html() 
            return f"<{self.tag}{self.props_to_html()}>{string_value}</{self.tag}>"
        
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"