from enum import StrEnum


class ProviderQuery(StrEnum):
    GET_ALL_PROVIDERS = """
        EXEC [OSD].[sps_GetAllProviders] 
            @i_idExternalEnterprise = :external_enterprise_id,
            @i_numberPage = :number_pages,
            @i_totalRow = :total_row,
            @i_search = :search,
            @i_type = :type,
            @i_status = :status,
            @i_order = :order,
            @i_field = :field
    """

    GET_PROVIDER_BY_ID = """EXEC OSD.sps_GetProviderById 
        @i_idProvider =:id_provider"""

    GET_GROUP_BY_ID = """EXEC OSD.sps_GetGroupById 
        @i_idProviderGroup =:idProviderGroup"""

    GET_GROUPS_BY_EXTERNAL_ID = """EXEC OSD.sps_GetGroupByExternalId 
        @i_idExternal =:idExternal"""

    GET_PROVIDERS_BY_GROUP = """EXEC OSD.sps_GetProviderByGroup
        @i_idGroup =:idProviderGroup"""

    GET_TYPES = """EXEC OSD.sps_GetTypes
        @i_idExternalEnterprise =:external_enterprise_id"""

    GET_OVERLAPPED_USERS_BY_GROUP = """
        EXEC [OSD].[sps_GetOverlappedUsersByGroup]
            @i_idExternalEnterprise = :idExternalEnterprise,
            @i_idProviderGroup = :idProviderGroup
    """

    DELETE_GROUP_OF_PROVIDERS = """EXEC OSD.spu_DeleteGroupOfProviders 
        @i_idProviderGroup =:idProviderGroup,
        @i_user_id =:user_id"""

    CREATE_NEW_GROUP_ID = """EXEC OSD.spi_CreateNewGroupId 
        @i_idUser =:user_id,
        @i_groupName =:group_name,
        @i_osType =:os_type,
        @i_osSpecialty =:os_specialty,
        @i_osStartDate =:os_start_date,
        @i_osEndDate =:os_end_date,
        @i_payrollReferenceId =:payroll_reference_id,
        @i_notes =:notes,
        @i_idsProviders =:ids_providers,
        @i_formOrigin =:formOrigin,
        @i_idProviderGroup =:idProviderGroup,
        @i_user_id_log =:user_id_log,
        @i_idExternalEnterprise =:external_enterprise_id"""

    CREATE_PROVIDERS_GROUP = """EXEC OSD.spi_CreateProviderGroup 
        @i_idUser =:user_id,
        @i_groupName =:group_name,
        @i_osType =:os_type,
        @i_osSpecialty =:os_specialty,
        @i_osStartDate =:os_start_date,
        @i_osEndDate =:os_end_date,
        @i_payrollReferenceId =:payroll_reference_id,
        @i_notes =:notes,
        @i_idsProviders =:ids_providers,
        @i_formOrigin =:formOrigin,
        @i_idProviderGroup =:idProviderGroup,
        @i_newIdProviderGroup =:newIdProviderGroup,
        @i_user_id_log =:user_id_log,
        @i_idExternalEnterprise =:external_enterprise_id"""

    VALIDATE_NAME = """EXEC OSD.sps_GetGroupByName 
        @i_groupName =:group_name,
        @i_idExternalEnterprise =:idExternalEnterprise,
        @i_formOrigin =:formOrigin,
        @i_idProviderGroup =:idProviderGroup"""

    SAVE_BY_GROUP = """EXEC OSD.spi_SaveManagementsByGroup 
                @i_idProvider =:idProvider,
                @i_idProviderGroup =:idProviderGroup,
                @i_user_id =:user_id"""

    CHANGE_PROVIDER_STATUS = """EXEC OSD.spu_ChangeProviderStatus
        @i_idProviders =:id_provider, 
        @i_status =:status,
        @i_user_id =:user_id"""

    GET_ALL_CONTRACTS = """
        EXEC [OSD].[sps_GetAllProviderGroupContracts] 
            @i_idProviderGroup = :idProviderGroup
    """

    GET_CONTRACT_BY_ID = """EXEC OSD.sps_GetProviderGroupContractById 
        @i_idProviderGroupContract =:idProviderGroupContract"""

    GET_ALL_CONTRACTS_RULES = """EXEC OSD.sps_GetAllProviderGroupContractRules 
        @i_idProviderGroupContract =:idProviderGroupContract"""

    GET_CONTRACT_RULE_BY_ID = """EXEC OSD.sps_GetProviderGroupContractRuleById 
        @i_idProviderGroupContractRule =:idProviderGroupContractRule"""

    CREATE_PROVIDERS_GROUP_CONTRACT = """EXEC OSD.spi_CreateProviderGroupContract 
        @i_idProviderGroup =:idProviderGroup,
        @i_description =:description,
        @i_contractType =:contractType,
        @i_cycleFrequency =:cycleFrequency,
        @i_startDate =:startDate,
        @i_endDate =:endDate,
        @i_osCompType =:osCompType,
        @i_isDeleted =:isDeleted,
        @i_user_id =:user_id,
        @i_status =:status"""

    CREATE_PROVIDERS_GROUP_CONTRACT_RULE = """EXEC OSD.spi_CreateProviderGroupContractRule 
        @i_idProviderGroupContract =:idProviderGroupContract,
        @i_rulePriority =:rulePriority,
        @i_ruleType =:ruleType,
        @i_rulePercentage =:rulePercentage,
        @i_ruleAmount =:ruleAmount,
        @i_ruleMin =:ruleMin,
        @i_ruleMax =:ruleMax,
        @i_ruleFrequency =:ruleFrequency,
        @i_startDate =:startDate,
        @i_endDate =:endDate,
        @i_user_id =:user_id"""

    UPDATE_PROVIDER_GROUP_CONTRACT = """EXEC OSD.spu_UpdateProviderGroupContract 
        @i_idProviderGroupContract =:idProviderGroupContract,
        @i_idProviderGroup =:idProviderGroup,
        @i_description =:description,
        @i_contractType =:contractType,
        @i_cycleFrequency =:cycleFrequency,
        @i_startDate =:startDate,
        @i_endDate =:endDate,
        @i_osCompType =:osCompType,
        @i_user_id =:user_id"""

    UPDATE_PROVIDER_GROUP_CONTRACT_RULES = """EXEC OSD.spu_UpdateProviderGroupContractRule 
        @i_idProviderGroupContractRule =:idProviderGroupContractRule,
        @i_rulePriority =:rulePriority,
        @i_ruleType =:ruleType,
        @i_rulePercentage =:rulePercentage,
        @i_ruleAmount =:ruleAmount,
        @i_ruleMin =:ruleMin,
        @i_ruleMax =:ruleMax,
        @i_ruleFrequency =:ruleFrequency,
        @i_startDate =:startDate,
        @i_endDate =:endDate,
        @i_user_id =:user_id"""

    DELETE_PROVIDER_GROUP_CONTRACT = """EXEC OSD.spu_DeleteProviderGroupContract 
        @i_idProviderGroupContract =:idProviderGroupContract,
        @i_user_id =:user_id"""

    DELETE_ALL_CONTRACT_RULES = """EXEC OSD.spu_DeleteAllProviderGroupContractRule 
        @i_idProviderGroupContract =:idProviderGroupContract,
        @i_user_id =:user_id"""

    UPDATE_PROVIDER_GROUP_CONTRACT_STATUS = """
        EXEC [OSD].[spu_UpdateContractStatus] 
            @i_idProviderGroupContract = :idProviderGroupContract,
            @i_idProviderGroup = :idProviderGroup,
            @i_contractStatus = :contractStatus,
            @i_idUser = :userId
    """

    GET_PROVIDER_GROUP_DATA_BY_ID = """ EXEC [OSD].sps_GetProviderGroupDataById @i_idProviderGroup = :idProviderGroup """

    GET_PROVIDERS_GROUPS_BY_IDS = """ EXEC [OSD].sps_GetProvidersGroupsByIds @i_idsProvidersGroups = :idsProvidersGroups """

    GET_ALL_LOCATIONS_BY_CLIENT = """EXEC OSD.sps_GetAllLocationsByClient
        @i_idExternalEnterprise =:idExternalEnterprise"""
