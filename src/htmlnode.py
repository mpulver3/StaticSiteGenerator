class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
       self.tag = tag
       self.value = value
       self.children = children
       self.props = props

    def to_html(self):
        raise NotImplemented()

    def props_to_html(self):
        string_props = ""
        for key in self.props:
            string_props.append(f" {key[1:-1]}={self.props[key]}")
        return string_props
    
    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"