from basesettings import *

ALLOWED_HOSTS = ['127.0.0.1']

AUTH_PASSWORD_VALIDATORS = [
    # Проверяет несоответствие пароля нескольким атрибутам пользователя:
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # Проверяет минимальную длину паролей.
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 5,
        }
    },
    # Проверяет, что пароль не соответствует текущему паролю.
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    #  Пароль не полностью цифровой
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]