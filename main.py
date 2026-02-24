import os
from firebase_functions import https_fn
from firebase_functions.options import MemoryOption, CorsOptions
from firebase_admin import initialize_app, credentials, firestore, db
import json
from datetime import date


cred = credentials.Certificate("service-account.json")
initialize_app(
    cred,
    {
        "storageBucket": "iq-strategy.appspot.com",
        "databaseURL": "https://iq-strategy-default-rtdb.firebaseio.com",
    },
)

cors_ops = CorsOptions(cors_origins="*", cors_methods=["get", "post", "options"])

from ai_model import AI_MODEL
from model.data_model import ContextFromModel, PredictContext
from model.enums import ResultType


@https_fn.on_call(memory=MemoryOption.MB_512, cors=cors_ops)
def sendMessage(req: https_fn.CallableRequest):
    if req.auth is None:
        raise Exception("No auth")
    message = req.data["message"]
    estrategy = req.data["estrategy"]
    data = req.data["data"]
    constext = ContextFromModel.from_dict(data)
    if message is None:
        raise Exception("No message provided")
    model = AI_MODEL(method=estrategy)
    response = model.generate_with_docs(message, context=constext)
    return {"response": response}


@https_fn.on_call(memory=MemoryOption.MB_512, cors=cors_ops, timeout_sec=60)
def getPredcitions(req: https_fn.CallableRequest):
    try:
        if req.auth is None:
            raise https_fn.HttpsError(
                code=https_fn.FunctionsErrorCode.UNAUTHENTICATED,
                message="No está autenticado",
            )

        if not req.data:
            raise https_fn.HttpsError(
                code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT,
                message="No se proporcionaron datos para la predicción",
            )

        # 2. Validar contexto y ejecutar el modelo de IA
        try:
            context = PredictContext.from_dict(req.data)
        except Exception as context_err:
            raise https_fn.HttpsError(
                code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT,
                message=f"Error en el formato de los datos: {context_err}",
            )

        # 1. Preparar clave de caché: prediction-YYYY-MM-DD
        today_str = date.today().strftime("%Y-%m-%d")
        cache_key = f"prediction-{today_str}-{context.action.id}"
        db_ref = db.reference(f"predictions/{cache_key}")

        # 2. Intentar recuperar del caché (Realtime Database)
        try:
            cached_data = db_ref.get()
            if cached_data:
                print(f"Retornando respuesta cacheada para: {cache_key}")
                return {"response": cached_data}
        except Exception as cache_err:
            print(f"Error al leer de la base de datos (ignorando cache): {cache_err}")

        model = AI_MODEL("labels", results_type=ResultType.JSON)
        response = model.generate("crear las prediciones", context)

        try:
            json_response = json.loads(response)
        except json.JSONDecodeError as json_err:
            raise https_fn.HttpsError(
                code=https_fn.FunctionsErrorCode.INTERNAL,
                message="La respuesta del modelo no es un JSON válido",
            )

        print(f"Nueva prediccion generada para {cache_key}:", json_response)

        # 4. Guardar en Realtime Database para el resto del día
        try:
            db_ref.set(json_response)
        except Exception as save_err:
            print(f"Error al guardar la prediccion en la base de datos: {save_err}")

        return {"response": json_response}

    except https_fn.HttpsError as he:
        raise he
    except Exception as e:
        print(f"Error inesperado en getPredcitions: {e}")
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.INTERNAL,
            message=f"Error interno del servidor: {str(e)}",
        )
