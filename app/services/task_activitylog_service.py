from math import ceil
from sqlalchemy.ext.asyncio import AsyncSession

# Transaction Related Imports
from app.core.exceptions import TransactionNotFound,TransactionAlreadyExistsError,TransactionLimitExceededError
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreate,TransactionResponse,TransactionUpdate

class TransactionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.transaction_repository = TransactionRepository(db)

    async def create_transaction(self, data: TransactionCreate, user_id: int):
        
        if data.amount <= 0:
            raise TransactionLimitExceededError(
                f"Transaction amount must be a positive value."
            )

        transaction_data = {
            "amount": data.amount,
            "type": data.type,
            "description": data.description,
            "category_id": data.category_id,
            "transaction_date": data.transaction_date,
            "user_id": user_id,
        }
        try:
            new_transaction = await self.transaction_repository.create(transaction_data)
            response = TransactionResponse(
                id=new_transaction.id,
                amount=new_transaction.amount,
                type=new_transaction.type,
                description=new_transaction.description,
                transaction_date=new_transaction.transaction_date,
                category_id=new_transaction.category_id,
                user_id=new_transaction.user_id,
            )
            await self.db.commit()
            return response
        except Exception:
            await self.db.rollback()
            raise
    
    async def get_transaction_by_id(self, transaction_id: int, user_id: int):
        transaction = await self.transaction_repository.get_by_id(transaction_id, user_id)
        if not transaction:
            raise TransactionNotFound(f"Transaction with ID {transaction_id} not found.")
        return transaction

    async def update_transaction(
        self, transaction_id: int, data: TransactionUpdate, user_id: int
    ):
        transaction = await self.get_transaction_by_id(transaction_id, user_id)
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)

        if not update_data:
            return transaction
        
        try:
            transaction = await self.transaction_repository.update(transaction, update_data)
            await self.db.commit()
            return transaction
        except Exception:
            await self.db.rollback()
            raise

    async def delete_transaction(self, transaction_id: int, user_id: int):
        transaction = await self.get_transaction_by_id(transaction_id, user_id)
        try:
            await self.transaction_repository.delete(transaction)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

    async def get_transactions(self, user_id: int, page: int = 1, size: int = 10):
        offset = (page - 1) * size
        transactions, total = await self.transaction_repository.get_all(
            user_id, offset, size
        )
        total_pages = ceil(total / size) if size > 0 else 0

        return {
            "items": transactions,
            "total": total,
            "page": page,
            "size": size,
            "pages": total_pages
        }