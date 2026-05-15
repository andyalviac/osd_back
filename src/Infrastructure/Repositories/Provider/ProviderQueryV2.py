from enum import StrEnum


class ProviderQuery(StrEnum):
    GET_ALL_PROVIDERS = """
        EXEC [OSD].[sps_GetAllProvidersV2] 
            @i_idExternalEnterprise = :idExternalEnterprise,
            @i_numberPage = :numberPage,
            @i_totalRow = :totalRow,
            @i_search = :search,
            @i_type = :type,
            @i_status = :status,
            @i_order = :order,
            @i_field = :field
    """

    GET_GROUPS_BY_CLIENT = """
        EXEC [OSD].[sps_GetGroupsByClient] 
            @i_idExternalEnterprise = :idExternalEnterprise
    """
