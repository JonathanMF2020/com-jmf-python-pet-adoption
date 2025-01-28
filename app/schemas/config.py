from pydantic import BaseModel


class ConfigRequest(BaseModel):
    key: str
    value: str