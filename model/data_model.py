from model.folder import Folder
from model.result_data import ResultAlpaca
from model.actions import Action
from model.predictions import Predictions

class ContextFromModel:
    def __init__(self, folder:Folder, history:list[ResultAlpaca], predictions:list[Predictions]):
        self.folder = folder
        self.history = history
        self.predictions = predictions

    def to_dict(self):
        return {
            "folder": self.folder.to_dict(),
            "history": [history.to_dict() for history in self.history],
            "predictions": [prediction.to_dict() for prediction in self.predictions]
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            folder=Folder.from_dict(data.get("currentAction")),
            history=[ResultAlpaca.from_dict(history) for history in data.get("history", [])],
            predictions= [Predictions.from_dict(prediction) for prediction in data.get("predictions", [])]
        )
        
class ContextFromIndividualModel:
    def __init__(self, current_action:Folder, history: list[ResultAlpaca], predictions:list[Predictions]):
        self.current_action = current_action
        self.history = history
        self.predictions = predictions

    def to_dict(self):
        return {
            "currentAction": self.current_action.to_dict() if self.current_action else None,
            "cantidad": self.cantidad,
            "amount": self.amount,
            "history": [result.to_dict() for result in self.history] if self.history else [],
            "predictions": [result.to_dict() for result in self.predictions] if self.predictions else []
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            current_action=Folder.from_dict(data.get("currentAction")) if data.get("currentAction") else None,
            history=[ResultAlpaca.from_dict(item) for item in data.get("history", [])],
            predictions=[Predictions.from_dict(item) for item in data.get("predictions", [])]
        )
        
class PredictContext:
    def __init__(self, action:Action, history:list[ResultAlpaca]):
        self.action = action
        self.history = history
    
    def to_dict(self):
        return {
            "action": self.action.to_dict(),
            "history": [history.to_dict() for history in self.history]
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            action=Action.from_dict(data.get("action")),
            history=[ResultAlpaca.from_dict(history) for history in data.get("history", [])]
        )