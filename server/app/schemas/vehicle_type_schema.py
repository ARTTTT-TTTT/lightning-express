from pydantic import BaseModel

# * name: 'motorcycle', 'truck', 'airplane'


class VehicleTypeBase(BaseModel):
    name: str
    description: str


class VehicleTypeCreate(VehicleTypeBase):
    pass


class VehicleTypeUpdate(VehicleTypeBase):
    pass


class VehicleOut(VehicleTypeBase):
    id: int

    model_config = {"from_attributes": True}
