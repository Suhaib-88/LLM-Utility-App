from enum import Enum
from typing import Annotated, Any
from pydantic import (BaseModel, ConfigDict, Field, PlainSerializer, field_validator, model_serializer)



class FieldTypes (str, Enum):
    TEXT= "str"
    INTEGER= "int"
    PASSWORD= "str"
    FLOAT= "float"
    BOOLEAN= "bool"
    DICT= "str"
    NESTED_DICT= "str"
    FILE= "file"
    PROMPT= 'prompt'
    CODE= 'code'
    OTHER ='other'
    LINK = "link"
    TABLE = "table"
    

SerializableFieldTypes= Annotated[FieldTypes, PlainSerializer(lambda v:v.value, return_type=str)]

class BaseInputMixin(BaseModel, validate_assignment= True):
    model_config= ConfigDict(arbitrary_types_allowed=True, extra='forbid', populate_by_name=True)
    field_type: SerializableFieldTypes= Field(default=FieldTypes.TEXT,alias='type')
    required:bool = False

    placeholder:str= ""
    show:bool = True
    name:str= Field(description='Name of the field')

    value: Any = ''

    display_name : str| None = None

    advanced:bool = False

    input_types: list[str]|None= None

    dynamic:bool = False

    info:str |None= ""

    real_time_refresh: bool|None=None

    refresh_button:bool|None=None

    refresh_button_text: str |None=None

    title_case:bool|None=None

    def to_dict(self):
        return self.model_dump(exclude_none=True, by_alias=True)
    
    @field_validator
    @classmethod
    def validate_field_type(cls, v):
        try:
            return FieldTypes(v)
        
        except ValueError:
            return FieldTypes.OTHER
        
    
    @model_serializer(mode='wrap')
    def serialize_model(self, handler):
        dump = handler(self)
        if 'field_type' in dump:
            dump['type']= dump.pop('field_type')

        dump['_input_type']= self.__class__.__name__

        return dump
    
class InputTraceMixin(BaseModel):
    trace_as_input:bool=True

class MetadataTraceMixin(BaseModel):
    trace_as_metadata:bool = True

class ListableInputMixin(BaseModel):
    is_list:bool = Field(default=False, alias='list')


class DatabaseLoadMixin(BaseModel):
    load_from_db:bool = Field(default=True)

class FileMixin(BaseModel):
    file_path:str|None = Field(default="")
    file_types: list[str]= Field(default=[], alias='fileTypes')

    @field_validator('file_types')
    @classmethod
    def validate_file_types(cls, v):
        if not isinstance(v, list):
            raise ValueError('File_types mus be a list')
        
        for file_type in v:
            if not isinstance(v, list):
                raise ValueError('File_types mus be a list')
            
            if file_type.startswith('.'):
                raise ValueError('File_types must not start with a dot')
            
        return v
    
class DropDownMixin(BaseModel):
    options:list[str]|None = None
    combobox:CoalesceBool = False


class MultilineMixin(BaseModel):
    multiline:CoalesceBool= True



class LinkMixin(BaseModel):
    icon:str|None= None
    text: str|None = None

class TableMixin(BaseModel):
    table_schema: TableSchema|list[Column]| None = None

    @field_validator("table_schema")
    @classmethod
    def validate_table_schema(cls, v):
        if isinstance(v, list) and all(isinstance(column, Column) for column in v):
            return TableSchema(columns= v)
        
        if isinstance(v, TableSchema):
            return v
        raise ValueError("table_schema must be a TableSchema or a list of Columns")