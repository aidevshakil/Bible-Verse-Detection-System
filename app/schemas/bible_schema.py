from pydantic import BaseModel
from typing import Optional, Union

class UserInput(BaseModel):
    translation: Optional[str] = None
    translation_id: Optional[str] = None
    book: Optional[str] = None
    book_id: Optional[str] = None
    chapter: Optional[Union[int, str]] = None
    verse: Optional[Union[str, int]] = None
    text: Optional[str] = None


class ModelOutput(BaseModel):
    book: Optional[str] = None
    book_id: Optional[str] = None
    translation: Optional[str] = None
    translation_id: Optional[str] = None
    chapter: Optional[Union[int, str]] = None
    verse: Optional[Union[str, int]] = None
    content: Optional[str] = None
