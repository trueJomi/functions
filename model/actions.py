class Action:
    def __init__(self, id, name, image, price=None):
        self.id = id
        self.name = name
        self.image = image
        self.price = price

    def to_dict(self):
        return {
            "name": self.name,
            "image": self.image,
            "price": self.price
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            image=data.get("image"),
            price=data.get("price")
        )