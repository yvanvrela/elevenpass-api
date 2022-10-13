from fastapi import APIRouter, Depends, Body, Path, HTTPException, status, Query
from typing import List
from sqlalchemy.orm import Session
from src.infra.schemas import vault_schema
from src.infra.database.models import user_model, vault_model
from src.infra.database.repositories.vault_repository import VaultRepository
from src.infra.database.config.database import get_db
from src.utils.auth_utils import get_current_user


router = APIRouter()


@router.post(path='/',
             status_code=status.HTTP_201_CREATED,
             response_model=vault_schema.VaultOut,
             summary='Create a vault',
             )
def create_vault(
    vault: vault_schema.VaultBase,
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    # Verify user
    if current_user.id != vault.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.',
        )

    # Verify vault name reference
    vault_name_reference = VaultRepository(session).get_vault_by_name(
        vault_name=vault.name, user_id=vault.user_id)
    if vault_name_reference:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Vault name already exists.'
        )

    # Add to db
    vault_db = VaultRepository(session).create_vault(vault)

    return vault_db


@router.get(path='/{id}',
            status_code=status.HTTP_200_OK,
            response_model=vault_schema.VaultOut,
            summary='Get vault by id',
            )
def get_vault(
    id: int = Path(..., gt=0, example=1),
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    vault_db = VaultRepository(session).get_vault_by_id(
        vault_id=id, user_id=current_user.id)
    if not vault_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Vault not found',
        )

    return vault_db


@router.get(path='/',
            status_code=status.HTTP_200_OK,
            response_model=List[vault_schema.VaultOut],
            summary='Get all user vaults',
            )
def get_vaults(
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    vaults_db = VaultRepository(session).get_vaults(user_id=current_user.id)
    if not vaults_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Vaults not found',
        )

    return vaults_db


@router.put(path='/{id}',
            status_code=status.HTTP_200_OK,
            response_model=vault_schema.VaultOut,
            summary='Update a vault',
            )
def update_vault(
    id: int = Path(..., gt=0, example=1,),
    update_data: vault_schema.VaultBase = Body(...,),
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    # Verify vault
    vault_reference = VaultRepository(session).get_vault_by_id(
        vault_id=id, user_id=current_user.id)
    if not vault_reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Vault not found.',
        )

    # Verify vault name duplicate in db
    if update_data.name != vault_reference.name:
        vault_name_reference = VaultRepository(session).get_vault_by_name(
            vault_name=update_data.name, user_id=current_user.id)
        if vault_name_reference:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Vault name already exists.'
            )

    # Update vault data
    vault_db = VaultRepository(session).update_vault(
        user_id=current_user.id, vault_id=id, update_data=update_data)

    return vault_db


@router.delete(path='/{id}',
               status_code=status.HTTP_200_OK,
               response_model=vault_schema.VaultOut,
               summary='Delete a vault',
               )
def delete_vault(
    id: int = Path(..., gt=0, example=1,),
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    # Verify vault reference by id
    vault_reference = VaultRepository(session).get_vault_by_id(
        vault_id=id, user_id=current_user.id)
    if not vault_reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Vault not found.'
        )

    # Delete the vault
    vault_db = VaultRepository(session).delete_vault(vault_id=id, user_id=current_user.id)

    return vault_db
