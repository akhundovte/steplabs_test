import re

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, validator
from .timezone import localtime

MIN_LENGTH_PASSWORD = 6


class UserBase(BaseModel):
    email: str
    name: str
    surname: str
    patronymic: Optional[str]


class UserCreate(UserBase):
    password: str

    @validator('password')
    def password_contain_digit_or_letter(cls, v, **kwargs):
        if not re.findall(r'\d', v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')

        if not re.findall(r'[A-Za-z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну букву')
        return v

    @validator('password')
    def password_min_length(cls, v):
        if len(v) < MIN_LENGTH_PASSWORD:
            raise ValueError('Пароль должен быть не менее 6 символов')
        return v


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda value: localtime(value).isoformat(),
            }
        orm_mode = True
