from firebase_functions import https_fn
from firebase_functions.options import MemoryOption, CorsOptions
from firebase_admin import initialize_app, credentials
import json

cred = credentials.Certificate("service-account.json")
initialize_app(cred, {
    'storageBucket': 'iq-strategy.appspot.com'
})

cors_ops = CorsOptions(
    cors_origins="*",
    cors_methods=["get", "post", "options"]
)

from ai_model import AI_MODEL
from model.data_model import ContextFromModel, PredictContext
from model.enums import ResultType

@https_fn.on_call(
    memory=MemoryOption.MB_512,
    cors=cors_ops
)
def sendMessage(req: https_fn.CallableRequest):
    if req.auth is None:
        raise Exception("No auth")
    message = req.data["message"]
    estrategy = req.data["estrategy"]
    data =  req.data["data"]
    constext =ContextFromModel.from_dict(data)
    if message is None:
        raise Exception("No message provided")
    model = AI_MODEL(method=estrategy)
    response = model.generate_with_docs(message, context=constext)
    return {
        "response": response
    }
    
@https_fn.on_call(
    memory=MemoryOption.MB_512,
    cors=cors_ops
)
def getPredcitions(req: https_fn.CallableRequest):
    if req.auth is None:
        raise Exception("No auth")
    context = PredictContext.from_dict(req.data)
    model = AI_MODEL("labels",results_type=ResultType.JSON)
    response = model.generate("crear las prediciones", context)
    json_response = json.loads(response)
    print(json_response)
    return {
        "response": json_response
    }