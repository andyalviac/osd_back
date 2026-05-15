from enum import StrEnum

class DashQuery(StrEnum):

    GET_AUDIT_LOG = '''
    EXEC CATALOG.sps_GetAuditLog
    @i_numberPage= :numberPage,
    @i_totalRow= :totalRow,
    @i_search = :search,
    @i_type = :type
    '''