from typing import Self, final, override

class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[Self] | None = None,
        props: dict[str, str] | None = None
        ):

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        output_str = ""
        if self.tag is None:
            return self.value
        if self.props is None:
            output_str = f"<{self.tag}>{self.value}</{self.tag}>"
        if self.props is  not None:
            output_str = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return output_str

    def props_to_html(self):
        output_str = ""
        if self.props is None:
            return output_str
        for k,v in self.props.items():
            output_str = output_str + f' {k}="{v}"'
        return output_str

    @override
    def __repr__(self) -> str:
        output_str = f"---\ntag: {self.tag}\nvalue: {self.value}"
        if self.children is not None:
            output_str = output_str + "\nchildren:"
            for item in self.children:
                output_str = output_str + f"\n - {item}"
        if self.props is not None:
            output_str = output_str + "\nprops:"
            for k, v in self.props.items():
                output_str = output_str + f"\n - {k}, {v}"
        return output_str

@final
class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: dict[str, str] | None = None
        ):
        super().__init__(tag, value, None, props)

    @override
    def to_html(self):
        output_str = ""
        if self.value is None:
            raise ValueError("value missing")
        if self.tag is None:
            return self.value
        if self.props is None:
            output_str = f"<{self.tag}>{self.value}</{self.tag}>"
        if self.props is  not None:
            output_str = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return output_str
        
    @override
    def __repr__(self) -> str:
        output_str = f"---\ntag: {self.tag}\nvalue: {self.value}"
        if self.props is not None:
            output_str = output_str + "\nprops:"
            for k, v in self.props.items():
                output_str = output_str + f"\n - {k}, {v}"
        return output_str

@final
class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: list[HTMLNode] | None,
        props: dict[str, str] | None = None
        ):
        super().__init__(tag, None, children, props)

    @override
    def to_html(self):
        output_str = ""
        if self.tag is None:
            raise ValueError("tag missing")
        if self.children is None:
            raise ValueError("children missing")
        if self.props is None:
            output_str = f"<{self.tag}>"
        if self.props is not None:
            output_str = f"<{self.tag}{self.props_to_html()}>"
        for item in self.children:
            output_str = output_str + item.to_html()
        output_str = output_str + f"</{self.tag}>"

        return output_str

if __name__ == "__main__":
    unittest.main()

