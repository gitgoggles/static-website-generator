from enum import Enum, auto

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()

    def tag(self):
        match self:
            case BlockType.PARAGRAPH:
                return 'p'
            case BlockType.HEADING:
                return 'h1'
            case BlockType.CODE:
                return 'code'
            case BlockType.QUOTE:
                return 'blockquote'
            case BlockType.UNORDERED_LIST:
                return 'ul'
            case BlockType.ORDERED_LIST:
                return 'ol'


