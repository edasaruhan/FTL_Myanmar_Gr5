from pydantic import BaseModel


class TextRequestModel(BaseModel):
    user_input: str
