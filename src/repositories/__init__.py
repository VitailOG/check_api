class BaseRepository:

    dbsession = property(lambda self: self.__dbsession)

    def __init__(self, dbsession) -> None:
        self.__dbsession = dbsession
