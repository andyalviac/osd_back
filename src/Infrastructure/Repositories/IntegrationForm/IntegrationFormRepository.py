from typing import List, Optional, Dict, Any
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from Osdental.Database.BaseRepository import BaseRepository
from Osdental.Shared.Utils.CaseConverter import CaseConverter

# from src.Infrastructure.Schemas.IntegrationForm import IntegrationForm
from src.Domain.Ports.IIntegrationFormRepository import IIntegrationFormRepository
from . import IntegrationFormQuery


class IntegrationFormRepository(BaseRepository, IIntegrationFormRepository):

    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def get_integration_form_resource_by_provider_id(
        self, provider_id: str, form_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:

        params = {"idProvider": provider_id, "formType": form_type}

        return await self._execute_query(
            IntegrationFormQuery.GET_INTEGRATION_FORM_RESOURCES_BY_PROVIDER_ID,
            params=params,
            many=True,
            as_dict=True,
        )

    async def create_integration_provider_form(
        self, user_id: str, data: List, provider_id: Optional[str] = None
    ) -> None:
        form_details_params = []
        compponents_params = []

        for item in data:
            form_id = str(uuid4())
            params = {
                "idUser": user_id,
                "idProvider": item.id_provider or provider_id,
                "idForm": form_id,
                "formType": item.form_type,
            }

            await self._execute_command(
                IntegrationFormQuery.CREATE_INTEGRATION_PROVIDER_FORM, params=params
            )

            if item.fields:
                for field in item.fields:
                    form_detail_id = str(uuid4())
                    form_details_params.append(
                        {
                            "idUser": user_id,
                            "idForm": form_id,
                            "idFormDetail": form_detail_id,
                            "formType": item.form_type,
                            "typeComponent": field.type,
                            "idMasterCatalog": field.id_catalog,
                            "name": field.field,
                            "key": field.label,
                        }
                    )

                    for key, value in field.__dict__.items():
                        if key not in ("extra", "id_catalog"):
                            compponents_params.append(
                                {
                                    "idUser": user_id,
                                    "idFormDetail": form_detail_id,
                                    "attrName": key,
                                    "attrValue": value,
                                }
                            )
                    for key, value in (field.extra or {}).items():
                        compponents_params.append(
                            {
                                "idUser": user_id,
                                "idFormDetail": form_detail_id,
                                "attrName": CaseConverter.snake_to_camel(key),
                                "attrValue": value,
                            }
                        )

        for param in form_details_params:
            await self._execute_command(
                IntegrationFormQuery.CREATE_INTEGRATION_FORM_DETAILS, params=param
            )

        for param in compponents_params:
            await self._execute_command(
                IntegrationFormQuery.CREATE_COMPONENTS_ATTRIBUTE, params=param
            )

    async def delete_integration_form_by_provider_id(self, provider_id: str) -> None:

        await self._execute_command(
            IntegrationFormQuery.DELETE_DYNAMIC_INTEGRATION_FORM_BY_PROVIDER_ID,
            params={"idProvider": provider_id},
        )

    async def provider_has_integration_form(self, provider_id: str) -> bool:
        return await self._execute_scalar(
            IntegrationFormQuery.PROVIDER_HAS_INTEGRATION_FORM,
            params={"idProvider": provider_id},
        )
