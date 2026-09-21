
class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        string = ""
        if self.props is not None:
            for key in self.props:
                string+=f' {key}="{self.props[key]}"'
        return string

    def __repr__(self) -> str:
        return f"HTMLNode(TAG = {self.tag}, VALUE = {self.value}, CHILDREN = {self.children}, PROPS = {self.props_to_html()})"

class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode(TAG = {self.tag}, VALUE = {self.value}, PROPS = {self.props_to_html()})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self,indentation=0): #TODO:indentation by default is 2
        if self.tag is None:
            raise ValueError("Parent node requires a tag")

        if self.children is None:
            raise ValueError("Children variable is missing from parent node")
        
        message = f"<{self.tag}{self.props_to_html()}>\n"
        for index, children in enumerate(self.children):
            if isinstance(children,ParentNode):
                message+=children.to_html(indentation)
            else:
                message+=children.to_html()
            if index+1 != len(self.children):
                message += "\n"

            
        message = message.replace("\n",""+" "*indentation) #TODO:reaplace \n with \n+" "*indentation
        message+="\n"
        message += f"</{self.tag}>"

        return message

