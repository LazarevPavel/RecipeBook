#почему-то без этого импорта (CustomUser) в этом файле при AUTH_USER_MODEL
# в сеттинге падает ошибка, будто бы этой модельки не существует ¯\_(ツ)_/¯
from .user import CustomUser