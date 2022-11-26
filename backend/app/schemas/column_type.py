from enum import Enum

from pydantic import BaseModel
from sqlalchemy.dialects import postgresql as ps


class ExtendedEnum(Enum):
    @classmethod
    def dict(cls) -> dict[str, list[str]]:
        return {cls.__name__: list(map(lambda c: c.value, cls))}


class UserRole(BaseModel):
    user: str
    admin: str
    manager: str
    ranker: str
    client: str


class ClientType(BaseModel):
    current: str
    potential: str


class TaskPriority(BaseModel):
    high: str
    medium: str
    low: str


class EquipmentStatus(BaseModel):
    accepted: str
    progress: str
    completed: str
    terminated: str


class MarketSector(BaseModel):
    healthcare: str
    materials: str
    real_estate: str
    consumer_staples: str
    consumer_discretionary: str
    energy: str
    industrials: str
    consumer_services: str
    financials: str
    technology: str
    utilities: str


class CompanySize(BaseModel):
    individual: str
    small: str
    medium: str
    big: str
    huge: str


class ContractStage(BaseModel):
    generation: str
    negotiation: str
    routing: str
    approval: str
    storage: str


class TaskType(BaseModel):
    website_design: str
    ui_design: str
    phone_call: str
    copywriting: str
    other: str


# ----------------------------------------------------------------------------------------------------------------------

userRole = UserRole(user='user',
                    admin='admin',
                    manager='manager',
                    ranker='ranker',
                    client='client')

clientType = ClientType(current='current',
                        potential='potential')

taskType = TaskType(website_design='website_design',
                    ui_design='ui_design',
                    phone_call='phone_call',
                    copywriting='copywriting',
                    other='other')

taskPriority = TaskPriority(high='high',
                            medium='medium',
                            low='low')

equipmentStatus = EquipmentStatus(accepted='accepted',
                                  progress='progress',
                                  completed='completed',
                                  terminated='terminated')

marketSector = MarketSector(healthcare='healthcare',
                            materials='materials',
                            real_estate='real_estate',
                            consumer_staples='consumer_staples',
                            consumer_discretionary='consumer_discretionary',
                            energy='energy',
                            industrials='industrials',
                            consumer_services='consumer_services',
                            financials='financials',
                            technology='technology',
                            utilities='utilities')

companySize = CompanySize(individual='individual',
                          small='small',
                          medium='medium',
                          big='big',
                          huge='huge')

contractStage = ContractStage(generation='generation',
                              negotiation='negotiation',
                              routing='routing',
                              approval='approval',
                              storage='storage')

# ----------------------------------------------------------------------------------------------------------------------

userRoleEnum = ExtendedEnum(value=UserRole.__name__, names=userRole.dict())

clientTypeEnum = ExtendedEnum(value=ClientType.__name__, names=clientType.dict())

taskTypeEnum = ExtendedEnum(value=TaskType.__name__, names=taskType.dict())

taskPriorityEnum = ExtendedEnum(value=TaskPriority.__name__, names=taskPriority.dict())

equipmentStatusEnum = ExtendedEnum(value=EquipmentStatus.__name__, names=equipmentStatus.dict())

marketSectorEnum = ExtendedEnum(value=MarketSector.__name__, names=marketSector.dict())

companySizeEnum = ExtendedEnum(value=CompanySize.__name__, names=companySize.dict())

contractStageEnum = ExtendedEnum(value=ContractStage.__name__, names=contractStage.dict())

# ----------------------------------------------------------------------------------------------------------------------

userRolePostgresEnum = ps.ENUM(*userRole.schema().get('required'), name=UserRole.__name__)

clientTypePostgresEnum = ps.ENUM(*clientType.schema().get('required'), name=ClientType.__name__)

taskTypePostgresEnum = ps.ENUM(*taskType.schema().get('required'), name=TaskType.__name__)

taskPriorityPostgresEnum = ps.ENUM(*taskPriority.schema().get('required'), name=TaskPriority.__name__)

equipmentStatusPostgresEnum = ps.ENUM(*equipmentStatus.schema().get('required'), name=EquipmentStatus.__name__)

marketSectorPostgresEnum = ps.ENUM(*marketSector.schema().get('required'), name=MarketSector.__name__)

companySizePostgreseEnum = ps.ENUM(*companySize.schema().get('required'), name=CompanySize.__name__)

contractStagePostgreseEnum = ps.ENUM(*contractStage.schema().get('required'), name=ContractStage.__name__)
