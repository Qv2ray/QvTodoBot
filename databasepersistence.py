from typing import Dict, List, Optional
from telegram.ext import BasePersistence
from sqlalchemy.ext.declarative import declarative_base


class DatabasePersistence(BasePersistence):
    def __init__(
        self,
        store_user_data: bool = True,
        store_chat_data: bool = True,
        store_bot_data: bool = True,
    ) -> None:
        super().__init__(
            store_user_data=store_user_data,
            store_chat_data=store_chat_data,
            store_bot_data=store_bot_data,
        )
        self.user_data: Optional[Dict[str, List[str]]] = None
