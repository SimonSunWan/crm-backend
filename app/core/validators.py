from pydantic import field_validator
from typing import Any
import re


class Validators:
    """验证器集合"""
    
    @staticmethod
    def validate_email(email: str) -> str:
        """验证邮箱格式"""
        if not email:
            return email
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError('邮箱格式不正确')
        return email
    
    @staticmethod
    def validate_phone(phone: str) -> str:
        """验证手机号格式"""
        if not phone:
            return phone
        
        phone_pattern = r'^1[3-9]\d{9}$'
        if not re.match(phone_pattern, phone):
            raise ValueError('手机号格式不正确')
        return phone
    
    @staticmethod
    def validate_password(password: str) -> str:
        """验证密码强度"""
        if len(password) < 8:
            raise ValueError('密码长度至少8位')
        
        if not re.search(r'[A-Za-z]', password):
            raise ValueError('密码必须包含字母')
        
        if not re.search(r'\d', password):
            raise ValueError('密码必须包含数字')
        
        return password
    
    @staticmethod
    def validate_username(username: str) -> str:
        """验证用户名格式"""
        if len(username) < 3:
            raise ValueError('用户名长度至少3位')
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError('用户名只能包含字母、数字和下划线')
        
        return username


def email_validator(field_name: str = "email"):
    """邮箱验证装饰器"""
    return field_validator(field_name)(Validators.validate_email)


def phone_validator(field_name: str = "phone"):
    """手机号验证装饰器"""
    return field_validator(field_name)(Validators.validate_phone)


def password_validator(field_name: str = "password"):
    """密码验证装饰器"""
    return field_validator(field_name)(Validators.validate_password)


def username_validator(field_name: str = "user_name"):
    """用户名验证装饰器"""
    return field_validator(field_name)(Validators.validate_username)
