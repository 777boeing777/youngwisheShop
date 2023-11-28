from __future__ import annotations
from abc import ABC, abstractmethod


class IRepository(ABC):
    model = None

    @abstractmethod
    async def get(self):
        """Получить все объекты"""

    @abstractmethod
    async def get_by_pk(self, pk):
        """Получить объект по id"""

    @abstractmethod
    async def create(self, in_model):
        """Создать объект"""

    @abstractmethod
    async def delete(self):
        """Удалить объекты"""

    @abstractmethod
    async def delete_by_pk(self, pk):
        """Удалить объект"""


class IService(ABC):
    @abstractmethod
    async def get(self):
        """Получить все объекты"""

    @abstractmethod
    async def get_by_pk(self, pk):
        """Получить объект по id"""

    @abstractmethod
    async def create(self, in_model):
        """Создать объект"""

    @abstractmethod
    async def delete(self):
        """Удалить объекты"""

    @abstractmethod
    async def delete_by_pk(self, pk):
        """Удалить объект"""
