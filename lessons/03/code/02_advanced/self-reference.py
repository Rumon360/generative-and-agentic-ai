from typing import List, Optional
from pydantic import BaseModel


# Recursive model: a Comment can contain a list of other Comments (replies)
class Comment(BaseModel):
    id: int
    content: str

    # "Comment" is a forward reference (string) because the class
    # is not fully defined yet at this point
    replies: Optional[List["Comment"]] = None


# This resolves the forward reference ("Comment" → actual class)
# Required in recursive/self-referencing models
Comment.model_rebuild()


# Create a nested comment structure
comment = Comment(
    id=2,
    content="First Comment",
    replies=[
        # Simple reply (no nested replies)
        Comment(id=2, content="First Reply"),
        # Reply with its own nested replies
        Comment(
            id=3,
            content="Second Reply",
            replies=[
                # Nested reply inside second reply
                Comment(id=4, content="Nested Reply 1")
            ],
        ),
    ],
)
