# !/usr/bin/python3
# type: ignore

# ** info: python imports
from enum import Enum

# ** info: pydantic imports
from pydantic import field_validator
from pydantic import ValidationInfo
from pydantic import BaseModel
from pydantic import Field

# ** info: typing imports
from typing import Optional

# **info: metadata for the model imports
from src.modules.waste.ports.rest_routers_dtos.waste_dtos_metadata import waste_filter_by_status_request_dto
from src.modules.waste.ports.rest_routers_dtos.waste_dtos_metadata import waste_full_data_response_list_ex
from src.modules.waste.ports.rest_routers_dtos.waste_dtos_metadata import collect_request_classify_req_ex
from src.modules.waste.ports.rest_routers_dtos.waste_dtos_metadata import collect_request_classify_res_ex
from src.modules.waste.ports.rest_routers_dtos.waste_dtos_metadata import waste_clasification_req_ex
from src.modules.waste.ports.rest_routers_dtos.waste_dtos_metadata import waste_clasification_res_ex
from src.modules.waste.ports.rest_routers_dtos.waste_dtos_metadata import waste_update_status_req

# ** info: sidecards imports
from src.sidecards.artifacts.uuid_provider import UuidProvider

__all__: list[str] = ["WasteClasificationRequestDto", "WasteClasificationResponseDto", "WasteClassifyRequestDto", "WasteFullDataResponseDto", "WasteFilterByStatusRequestDto"]


# !------------------------------------------------------------------------
# ! info: sumbodule dtos section start
# ! warning: all models in this section are the ones that are going to be used as submodels in request or response models
# ! warning: a model only can be declared in this section if it is going to be used as a submodel in a request or response models
# !------------------------------------------------------------------------


class StateWasteOptions(str, Enum):
    gaseous: str = "gaseous"
    liquid: str = "liquid"
    paslm: str = "paslm"
    solid: str = "solid"


# !------------------------------------------------------------------------
# ! info: request model section start
# ! warning: all models in this section are the ones that are going to be used as request dto models
# ! warning: a model only can be declared in this section if it is going to be used as a request dto model
# !------------------------------------------------------------------------


class WasteClasificationRequestDto(BaseModel):
    stateWaste: StateWasteOptions = Field(...)
    isotopesNumber: float = Field(...)
    weightInKg: float = Field(...)
    model_config = waste_clasification_req_ex

    @field_validator("isotopesNumber", "weightInKg")
    @classmethod
    def int_validator(cls, value: float, info: ValidationInfo) -> int:
        if isinstance(value, float):
            value = float(value)
        else:
            raise ValueError(f"{info.field_name} is not a double input")
        return value


class WasteClassifyRequestDto(BaseModel):
    wasteId: str = Field(...)
    isotopesNumber: float = Field(...)
    stateWaste: int = Field(...)
    storeId: int = Field(...)

    @field_validator("isotopesNumber")
    @classmethod
    def float_validator(cls, value: str, info: ValidationInfo) -> int:
        if isinstance(value, float):
            value = float(value)
        else:
            raise ValueError(f"{info.field_name} is not a float input")
        return value

    @field_validator("stateWaste", "storeId")
    @classmethod
    def int_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, int):
            value = int(value)
        else:
            raise ValueError(f"{info.field_name} is not a integer input")
        return value

    @field_validator("wasteId")
    @classmethod
    def uuid_validator(cls, value: str, info: ValidationInfo) -> int:
        if UuidProvider.check_str_uuid(value):
            value = str(value)
        else:
            raise ValueError(f"{info.field_name} is not a valid uuid input")
        return value

    model_config = collect_request_classify_req_ex


class WasteFilterByStatusRequestDto(BaseModel):
    processStatus: int = Field(...)

    @field_validator("processStatus")
    @classmethod
    def int_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, int):
            value = int(value)
        else:
            raise ValueError(f"{info.field_name} is not a integer input")
        return value

    model_config = waste_filter_by_status_request_dto


class WasteUpdateStatusRequestDto(BaseModel):
    wasteId: str = Field(...)
    processStatus: int = Field(...)

    @field_validator("wasteId")
    @classmethod
    def uuid_validator(cls, value: str, info: ValidationInfo) -> int:
        if UuidProvider.check_str_uuid(value):
            value = str(value)
        else:
            raise ValueError(f"{info.field_name} is not a valid uuid input")
        return value

    @field_validator("processStatus")
    @classmethod
    def int_validator(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(value, int):
            value = int(value)
        else:
            raise ValueError(f"{info.field_name} is not a integer input")
        return value

    model_config = waste_update_status_req


# !------------------------------------------------------------------------
# ! info: response model section start
# ! warning: all models in this section are the ones that are going to be used as response dto models
# ! warning: a model only can be declared in this section if it is going to be used as a response dto model
# !------------------------------------------------------------------------


class WasteClasificationResponseDto(BaseModel):
    storeType: int = Field(...)
    model_config = waste_clasification_res_ex


class WasteFullDataResponseDto(BaseModel):
    id: str = Field(...)
    requestId: str = Field(...)
    type: int = Field(...)
    packaging: int = Field(...)
    processStatus: int = Field(...)
    weightInKg: float = Field(...)
    volumeInL: float = Field(...)
    isotopesNumber: Optional[float] = None
    stateWaste: Optional[int] = None
    storeType: Optional[int] = None
    description: str = Field(...)
    note: Optional[str] = None
    create: str = Field(...)
    update: str = Field(...)

    model_config = collect_request_classify_res_ex


class WasteFullDataResponseListDto(BaseModel):
    values: list[WasteFullDataResponseDto] = Field(...)

    model_config = waste_full_data_response_list_ex
