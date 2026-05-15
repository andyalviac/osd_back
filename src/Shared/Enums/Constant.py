from enum import Enum


class Status(str):
    CODE = "STATUS_CODE"
    MESSAGE = "STATUS_MESSAGE"


class MeasureTypesShortNames(str, Enum):
    COLLECTIONS = "Coll."
    NET_PRODUCTION = "Net Prod."
    NET_COLLECTIONS = "Net Coll."
    EBITDA = "EBITDA"


class Constant(str, Enum):
    REDIS_TTL = 600
    REDIS_PROVIDERS_KEY = "providers"
    REDIS_CONTRACTS_KEY = "contracts"
    REDIS_CONTRACT_KEY = "contract"

    GUID_EMPTY = "00000000-0000-0000-0000-000000000000"

    # General Fields
    ID_EXTERNAL = "idExternalEnterprise"
    ID_PRACTICE_NAME = "idPracticeName"
    ID_USER = "idUser"
    START_DATE = "startDate"
    END_DATE = "endDate"
    DROPDOWN_FIELD_LABEL = "name"
    DROPDOWN_FIELD_VALUE = "id"
    FIELD_DISABLED = "disabled"
    COMPENSATIONS = "compensations"

    # Compensation/Cycle Fields
    ID_CYCLE = "idProviderCompensationCycle"
    ID_CYCLE_HEADER = "idProviderCompensationHeader"
    ID_CYCLE_DETAIL = "idProviderCompensationDetail"
    ID_CYCLE_TYPES = "idsCycleTypes"
    ID_LOCATION = "idLocation"
    LOCATION_NAME = "locationName"
    CYCLE_DESCRIPTION = "cycleDescription"
    CYCLE_STATUS = "statusCycle"
    HEADER_STATUS = "statusHeader"
    PAYROLL_TYPE = "idPayrollType"
    PAYROLL_CALCULATION_TYPE = "payrollCalculationType"
    RANGE_TYPE = "rangeType"
    MEASURE_TYPE = "measureType"
    ID_RULE = "idProviderGroupContractRule"
    AMOUNT = "amount"
    CALC_RULE_TYPE = "calculationRuleType"
    RULE_AMOUNT = "ruleAmount"
    RULE_PERC = "rulePercentage"
    ID_DEDUCTION = "idProviderCompensationDeduction"
    DEDUCTION_TOTAL = "deductionTotalAmount"
    DEDUCTIONS_TABLE = "deductionsTable"
    STATUS_HISTORY = "statusHistory"
    ACTIVE_CONTRACT_FLAG = "hasActiveContract"
    COMP_DETAIL_DATE = "detailDate"

    # Provider Fields
    ID_PROVIDER = "idProvider"
    ID_CONTRACT = "idProviderGroupContract"
    ID_PROVIDER_GROUP = "idProviderGroup"
    IDS_PROVIDERS_GROUPS = "idsProvidersGroups"
    PMS_SOURCE = "pmsSource"
    PMS_NAME = "pmsName"
    SPECIALTY = "osSpecialty"
    CONTRACT_TYPE = "contractType"
    CONTRACT_FREQUENCY = "cycleFrequency"
    CONTRACT_STATUS = "contractStatus"
    GROUP_NAME = "groupName"

    SPECIALTY_CATALOG_DENTIST = "OSD_GET_DENTIST_TYPE"
    SPECIALTY_CATALOG_ADMIN = "OSD_GET_ADMIN_TYPE"
    SPECIALTY_CATALOG_HYGIENIST = "OSD_GET_HYGIENIST_TYPE"

    REQUEST_SEARCH = "search"
    REQUEST_TYPE = "type"
    REQUEST_FIELD = "field"
    REQUEST_ORDER = "order"
    REQUEST_STATUS = "status"
    REQUEST_PAGE_NUMBER = "numberPage"
    REQUEST_PAGE_SIZE = "totalRow"

    # Catalogs Fields
    ID_MASTER_CATALOG = "idMasterCatalog"
    ID_DETAIL_CATALOG = "idDetailCatalog"

    CATALOG_FIELD_ID = "idDetail"
    CATALOG_FIELD_CODE = "code"
    CATALOG_FIELD_NAME = "name"
    CATALOG_FIELD_VALUE = "value"
    CATALOG_FIELD_CHILDREN = "options"

    # Catalog Names List
    CATALOG_CYCLE_TYPES = "OSD_GET_OSTYPE"
    CATALOG_RULE_TYPES = "OSD_GET_RULETYPE"
    CATALOG_MEASURE_TYPES = "OSD_GET_OSCOMPTYPE"
    CATALOG_CONTRACT_TYPES = "OSD_GET_CONTRACTTYPE"

    # Catalog Codes
    CODE_TRUE_UP = "TRUE-UP"


CYCLE_STATUS_LABELS = {
    1: "Open",
    2: "Pending",
    3: "Closed",
}

COMPENSATION_STATUS_LABELS = {
    1: "Open",
    2: "Submitted",
    3: "Approved",
    4: "Declined",
    5: "Closed",
}

CYCLE_STATUS_CODES = {
    0: "ALL",
    1: "OPEN",
    2: "PENDING",
    3: "PARTIALLY_REJECTED",
    4: "PENDING_APPROVAL",
    5: "APPROVED",
    6: "REJECTED",
    7: "CLOSED",
}

CYCLE_STATUS_CODES_REVERSE = {value: key for key, value in CYCLE_STATUS_CODES.items()}
