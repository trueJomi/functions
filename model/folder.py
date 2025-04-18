from model.actions import Action

class Folder:
    def __init__(self, action: Action, countActions: float, totalValue: float):
        self.action = action
        self.countActions = countActions
        self.totalValue = totalValue

    def to_dict(self):
        return {
            "action": self.action.to_dict(),
            "countActions": self.countActions,
            "totalValue": self.totalValue
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            action=Action.from_dict(data.get("action")),
            countActions=data.get("countActions"),
            totalValue=data.get("totalValue")
        )