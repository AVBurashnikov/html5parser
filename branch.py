class AttributeList:
    """
    Вспомогательный класс для более удобного обращения к атрибутам
    элемента(BaseElement)
    """

    def __init__(self, attr_dict: dict):
        self._attr_dict = {}
        for k, v in attr_dict.items():
            self._attr_dict[k] = v
            self.__setattr__(k, v)

    def __str__(self):
        return "({})>".format(self._attr_dict)


class Branch:
    """
    Базовый класс элемента дерева html-документа.
    """

    def __init__(
            self,
            id_: int,
            level: int,
            tag: str,
            position: int,
            parent_id: int = None,
            child_set: list = None,
            attributes: dict = None,
            content: str = None
    ):

        self.id = id_
        self.level = level
        self.tag = tag
        self.position = position
        self.parent_id = parent_id
        self.child_set = child_set

        if attributes is not None:
            self.attributes = AttributeList(attributes)

        self.content = content

    def __str__(self):
        return "<object Branch id[{}] | tag[{}] | level[{}] |attrs[{}] |>".format(
            self.id,
            self.tag,
            self.level,
            self.attributes
        )
