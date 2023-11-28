class JSONRepresentationMixin:
    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
