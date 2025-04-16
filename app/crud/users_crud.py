import models
from crud.base_crud import SQLAlchemyCrud


class UserCrud(SQLAlchemyCrud):
    def __init__(self, session):
        super().__init__(session)
        self.model = models.User
