from .ProviderResolver import ProviderResolver

# from .ProviderResolverV2 import ProviderResolver as ProviderResolverV2

provider_query_resolvers = {
    "getAllManagements": ProviderResolver.resolve_get_all_providers,
    "getTypesForClient": ProviderResolver.resolve_get_types,
    "getManagementById": ProviderResolver.resolve_get_provider_by_id,
    "getAllContracts": ProviderResolver.resolve_get_all_contracts,
    "getContractById": ProviderResolver.resolve_get_contract_by_id,
    "getGroupsByClient": ProviderResolver.resolve_get_groups_by_external_id,
    "getUsersByGroup": ProviderResolver.resolve_get_users_by_group,
    # "getProvidersCount": ProviderResolverV2.resolve_get_providers_count,
    # "getGroupsByClientV2": ProviderResolverV2.resolve_get_groups_by_client,
}


provider_mutation_resolvers = {
    "updateManagement": ProviderResolver.resolve_create_providers_group,
    "changeStatusManagement": ProviderResolver.resolve_change_provider_status,
    "saveManagementsByGroup": ProviderResolver.resolve_save_by_group,
    "createContract": ProviderResolver.resolve_create_providers_group_contract,
    "updateContract": ProviderResolver.resolve_update_providers_group_contract,
    "deleteContract": ProviderResolver.resolve_delete_providers_group_contract,
    "updateContractStatus": ProviderResolver.resolve_update_providers_group_contract_status,
}
