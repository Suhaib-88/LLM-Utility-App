from typing import Any
from pydantic import Field, field_validator, warnings
from .input_mixin import BaseInputMixin, DatabaseLoadMixin, FileMixin, FieldTypes, DropDownMixin,LinkMixin, MultilineMixin, ListableInputMixin,MetadataTraceMixin, TableMixin, SerializableFieldTypes,InputTraceMixin
from template.field.base import Input
from schema.data import Data
from inputs.validators import CoalesceBool

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


class StrInput(BaseInputMixin, ListableInputMixin, DatabaseLoadMixin, MetadataTraceMixin):
    field_type: SerializableFieldTypes= FieldTypes.TEXT
    load_from_db: CoalenceBool= False

    @staticmethod
    def _validate_value(v:Any, _info):
        if not isinstance(v,str) and v is not None:
            if _info.data.get("input_types") and v.__class__.__name__ not in _info.data.get("input_types"):
                warnings.warn(
                    f"Invalid value type {type(v)} for input {_info.data.get('name')}. Expected types: {_info.data.get('input_types')}"
                )
            else:
                warnings.warn(f"Invalid value type {type(v)} for input {_info.data.get('name')}.")
        return v
    
    @field_validator("value")
    @classmethod
    def validate_value(cls, v:Any, _info):
        is_list = _info.data["is_list"]
        value = None
        if is_list:
            value = [cls._validate_value(vv, _info) for vv in v]
        else:
            value = cls._validate_value(v, _info)
        return value


class SecretStrInput(BaseInputMixin, DatabaseLoadMixin):
    field_type: SerializableFieldTypes = FieldTypes.PASSWORD
    password: CoalesceBool = Field(default=True)
    input_types: list[str] = ["Message"]
    load_from_db: CoalesceBool = True

    @field_validator("value")
    @classmethod
    def validate_value(cls, v: Any, _info):
        value: str | AsyncIterator | Iterator | None = None
        if isinstance(v, str):
            value = v
        elif isinstance(v, Message):
            value = v.text
        elif isinstance(v, Data):
            if v.text_key in v.data:
                value = v.data[v.text_key]
            else:
                keys = ", ".join(v.data.keys())
                input_name = _info.data["name"]
                raise ValueError(
                    f"The input to '{input_name}' must contain the key '{v.text_key}'."
                    f"You can set `text_key` to one of the following keys: {keys} or set the value using another Component."
                )
        elif isinstance(v, AsyncIterator | Iterator):
            value = v
        elif v is None:
            value = None
        else:
            raise ValueError(f"Invalid value type `{type(v)}` for input `{_info.data['name']}`")
        return value


class DropdownInput(BaseInputMixin, DropDownMixin, MetadataTraceMixin):
    field_type: SerializableFieldTypes = FieldTypes.TEXT
    options: list[str] = Field(default_factory=list)
    combobox: CoalesceBool = False


class FileInput(BaseInputMixin, ListableInputMixin, FileMixin, MetadataTraceMixin):
    field_type: SerializableFieldTypes= FieldTypes.FILE

class LinkInput(BaseInputMixin, LinkMixin):
    field_type: SerializableFieldTypes= FieldTypes.LINK


DEFAULT_PROMPT_INTUT_TYPES = ["Message", "Text"]

class DefaultPromptField(Input):
    name:str
    display_name:str |None= None
    field_type:str='str'
    advanced:bool= False
    multiline:bool= True
    input_types:list[str]= DEFAULT_PROMPT_INPUT_TYPES
    value:Any= ""


InputTypes = (
    Input
    | DefaultPromptField
    | BoolInput
    | DataInput
    | DictInput
    | DropdownInput
    | MultiselectInput
    | FileInput
    | FloatInput
    | HandleInput
    | IntInput
    | MultilineInput
    | MultilineSecretInput
    | NestedDictInput
    | PromptInput
    | CodeInput
    | SecretStrInput
    | StrInput
    | MessageTextInput
    | MessageInput
    | TableInput
    | LinkInput
)

InputTypesMap: dict[str, type[InputTypes]] = {t.__name__: t for t in get_args(InputTypes)}


def instantiate_input(input_type: str, data: dict) -> InputTypes:
    input_type_class = InputTypesMap.get(input_type)
    if "type" in data:
        # Replate with field_type
        data["field_type"] = data.pop("type")
    if input_type_class:
        return input_type_class(**data)
    else:
        raise ValueError(f"Invalid input type: {input_type}")
