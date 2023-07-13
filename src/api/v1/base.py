from typing import List, Optional

from core.config import app_settings
from db.db import get_session
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.base import Url
from schemas import base as schema
from services.base import url_crud
from sqlalchemy.ext.asyncio import AsyncSession

SHORT_URL_PATTERN = app_settings.short_url_pattern
router = APIRouter()


@router.post(
    "/",
    response_model=schema.ShortUrlWithOrigin,
    status_code=status.HTTP_201_CREATED,
)
async def create_short_url(
    url_in: schema.CreateShortUrl,
    db: AsyncSession = Depends(get_session),
) -> schema.ShortUrlWithOrigin:
    url: Url = await url_crud.get_or_create(db=db, obj_in=url_in)
    return schema.ShortUrlWithOrigin(
        short_url=f"{SHORT_URL_PATTERN}{url.id}",
        original_url=url.original_url,
    )


@router.post(
    "/shorten/",
    response_model=List[schema.ShortUrlWithId],
    status_code=status.HTTP_201_CREATED,
)
async def bulk_create_short_url(
    urls_in: List[schema.CreateShortUrl],
    db: AsyncSession = Depends(get_session),
) -> List[schema.ShortUrlWithId]:
    url_objects = [
        await url_crud.get_or_create(db=db, obj_in=url) for url in urls_in
    ]
    result = [
        schema.ShortUrlWithId(
            short_id=url.id,
            short_url=f"{SHORT_URL_PATTERN}{url.id}",
        ) for url in url_objects
    ]
    return result


@router.get("/{obj_id}/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get_original_url(
    *,
    db: AsyncSession = Depends(get_session),
    obj_id: int,
    response: Response,
) -> None:
    url: Optional[Url] = await url_crud.get(db=db, obj_id=obj_id)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Url with id "{obj_id}" not found',
        )

    url.use_count += 1
    await db.commit()
    response.headers["Location"] = url.original_url
    return


@router.get("/{obj_id}/status", response_model=schema.ShortUrlStatic)
async def get_url_status(
    *,
    db: AsyncSession = Depends(get_session),
    obj_id: int,
) -> schema.ShortUrlStatic:
    url: Optional[Url] = await url_crud.get(db=db, obj_id=obj_id)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Url with id "{obj_id}" not found',
        )

    return schema.ShortUrlStatic(
        short_url=f"{SHORT_URL_PATTERN}{url.id}",
        original_url=url.original_url,
        use=url.use_count,
    )
