from typing import Any
from pydantic import Field, field_validator
from .input_mixin import BaseInputMixin, DatabaseLoadMixin, FileMixin, FieldTypes, LinkMixin, MultilineMixin, ListableInputMixin,MetadataTraceMixin, TableMixin, SerializableFieldTypes,InputTraceMixin


class TableInput(BaseInputMixin, MetadataTraceMixin, TableMixin, ListableInputMixin):
    field_type: SerializableFieldTypes = FieldTypes.TABLE
    is_list:bool= True

    @field_validator('value')
    @classmethod
    def validate_value(cls, v:Any, _info):
        if not isinstance(v, list):
            raise ValueError(f"TableInput value must be a list of dictionaries or Data. Value {v}")
        
        for item in v:
            if not isinstance(item, dict|Data):
                raise ValueError('TableInput must be a list of dictionaries or data')
        
        return v
    

class HandleInput(BaseInputMixin, ListableInputMixin, MetadataTraceMixin):
    input_types: list[str]= Field(default_factory= list)
    field_type: SerializableFieldTypes= FieldTypes.OTHER


class DataInput(HandleInput, InputTraceMixin, ListableInputMixin):
    input_types:list[str]= ["Data"]


class PromptInput(BaseInputMixin, ListableInputMixin, InputTraceMixin):
    field_type: SerializableFieldTypes = FieldTypes.PROMPT

class CodeInput(BaseInputMixin, ListableInputMixin, InputTraceMixin):
    field_type: SerializableFieldTypes = FieldTypes.CODE














class SecretStrInput(BaseInputMixin, DatabaseLoadMixin):
    field_type: SerializableFieldTypes = FieldTypes.PASSWORD
    # begin here