import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig
from bucket_service import exist_file
from model.data_model import ContextFromModel, PredictContext

from model.enums import ResultType

def generate_base_prompt(data: dict) -> str:
    return """Eres un asitente que se encargar de responer preguntas y hacer analisis de datos que son proporcionados por el usaurios 
    a los usuarios a tomar deciones financieras, con ditinta estrategias planteadas en documentos que se te proporcionaron"""

# AI MODEL

class AI_MODEL():

  def __init__(
      self,
      indications: str = "agente",
      method: str | None = None,
      results_type: ResultType = ResultType.TEXT ,
    ):
    self.indications = indications
    self.method = method
    self.results_type = results_type
    if self.method is not None:
      self.list_of_files = self.validate_files()
    vertexai.init(project="iq-strategy", location="us-central1")
    self.model = self.load_model()
  
  def validate_files(self):
    current_list = [f'{i+1}-{self.method}' for i in range(5)]
    files_validated = []
    for file in current_list:
        if exist_file(f'{self.method}/{file}.pdf'):
            files_validated.append(f'{self.method}/{file}.pdf')
    return files_validated

  def load_model(self):
    try:
        instructions: str
        with open(f"prompts/{self.indications}.txt", mode="r", encoding="utf-8") as file:
            instructions = file.read()
        return GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=GenerationConfig(
                temperature=0.8,
                response_mime_type=self.results_type.value
            ),
            system_instruction=instructions
        )
    except Exception as e:
        raise ValueError(f"Error loading model: {e}")

  def generate_with_docs(self, prompt:str, context: ContextFromModel) -> str:
    parts_list = [Part.from_uri(f"gs://iq-strategy.appspot.com/{file}", mime_type="application/pdf") for file in self.list_of_files]
    
    print(context.to_dict())
    
    response = self.model.generate_content([
        *parts_list,
        f"ten en cunta lo siguitnes datos para dar tu respuesta: {context.to_dict()}",
        prompt,
    ])
    return response.text
  
  def generate(self, prompt:str, context: PredictContext) -> str:
    
    response = self.model.generate_content([
        f"ten en cunta lo siguitnes datos para dar tu respuesta: {context.to_dict()}",
        prompt,
    ])
    return response.text
  