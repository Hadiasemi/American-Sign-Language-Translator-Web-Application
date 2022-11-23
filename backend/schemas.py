from fastapi import Form, File, UploadFile
from pydantic import BaseModel


# https://stackoverflow.com/a/60670614
class AwesomeForm(BaseModel):
    file: UploadFile

    @classmethod
    def as_form(
        cls,
        file: UploadFile = File(...)
    ):
        return cls(
            file=file
        )