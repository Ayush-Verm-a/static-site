class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        prop = ""
        if self.props is None:
            return prop
        for key in self.props:
            prop += " " + f"{key}=\"{self.props[key]}\""

        return prop
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError()
        
        if self.tag is None:
            return self.value
        
        prop_list = ''
        if self.props is not None:
            for prop in self.props:
                prop_list += f' {prop}="{self.props[prop]}"'

        return f"<{self.tag}{prop_list}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError()
    
        if self.children is None:
            raise ValueError("Children Missing")
        
        children_node = ""
        for child in self.children:
            children_node += child.to_html()

        return f"<{self.tag}>{children_node}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children})"

        
        