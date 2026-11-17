from math import ceil

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserNotFoundError,EmailAlreadyExistsError
from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate,UserUpdate


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db)

    async def create_user(self, data: UserCreate):
        email = str(data.email).strip().lower()  # Normalize the email address

        # Check if the email already exists
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise EmailAlreadyExistsError(f"Email '{email}' already exists.")

        # Hash the password before creating the user
        user_data = {
            "name": data.name,
            "email": email,
            "password_hash": hash_password(data.password)
        }
        try:
            new_user = await self.user_repository.create(user_data)
            await self.db.commit()  # Commit the transaction after creating the user
            return new_user
        except IntegrityError as exc:
            await self.db.rollback()  # Rollback the transaction in case of an error
            raise EmailAlreadyExistsError(f"Email is already registered.") from exc
        except Exception:
            await self.db.rollback()  # Rollback the transaction in case of an error
            raise  # Re-raise the exception to be handled by the caller

    async def get_user_by_id(self, user_id: int):
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
        return user

    async def update_user(self, user_id: int, data: UserUpdate):
        user = await self.get_user_by_id(user_id)
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)

        if not update_data:
            return user  # No changes to update, return the existing user
        
        try:
            user = await self.user_repository.update(user, update_data)
            await self.db.commit()  # Commit the transaction after updating the user
            return user
        except Exception:
            await self.db.rollback()  # Rollback the transaction in case of an error
            raise  # Re-raise the exception to be handled by the caller

    async def delete_user(self, user_id: int):
        user = await self.get_user_by_id(user_id)
        try:
            await self.user_repository.delete(user)
            await self.db.commit()  # Commit the transaction after deleting the user
        except Exception:
            await self.db.rollback()  # Rollback the transaction in case of an error
            raise  # Re-raise the exception to be handled by the caller

    async def get_users(self, page: int = 1, size: int = 10):
        offset = (page - 1) * size
        users, total = await self.user_repository.get_all(offset, size)
        total_pages = ceil(total / size) if size > 0 else 0

        return {
            "items": users,
            "total": total,
            "page": page,
            "size": size,
            "pages": total_pages
        }