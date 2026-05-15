
from enum import StrEnum 

class IntegrationFormQuery(StrEnum):

    GET_INTEGRATION_FORM_RESOURCES_BY_PROVIDER_ID = ''' 
    EXEC CATALOG.sps_GetIntegrationResourcesById
    @i_idProvider = :idProvider,
    @i_formType = :formType
    '''


    CREATE_INTEGRATION_PROVIDER_FORM = ''' 
    EXEC CATALOG.spi_IntegrationProviderForm 
    @i_idUser = :idUser,
    @i_idProvider = :idProvider,
    @i_idForm = :idForm,
    @i_formType = :formType
    ''' 
    
    CREATE_INTEGRATION_FORM_DETAILS = ''' 
    EXEC CATALOG.spi_IntegrationFormDetails 
    @i_idUser = :idUser,
    @i_idFormDetail = :idFormDetail,
    @i_idForm = :idForm,
    @i_formType = :formType,
    @i_typeComponent = :typeComponent,
    @i_idMasterCatalog = :idMasterCatalog,
    @i_name = :name,
    @i_key = :key
    ''' 
    
    CREATE_COMPONENTS_ATTRIBUTE = ''' 
    EXEC CATALOG.spi_ComponentsAttribute 
    @i_idUser = :idUser,
    @i_idFormDetail = :idFormDetail,
    @i_attrName = :attrName,
    @i_attrValue = :attrValue
    ''' 

    DELETE_DYNAMIC_INTEGRATION_FORM_BY_PROVIDER_ID = '''
    EXEC CATALOG.spd_DeleteDynamicIntegrationForm
    @i_idProvider = :idProvider
    '''

    PROVIDER_HAS_INTEGRATION_FORM = '''
    EXEC CATALOG.sps_ProviderHasIntegrationForm
    @i_idProvider = :idProvider
    '''
    