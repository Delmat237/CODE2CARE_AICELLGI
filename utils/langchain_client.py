from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config.settings import settings
import requests

def get_llm_response(query: str, language: str) -> str:
    # Simuler une interaction avec un LLM séparé via API
    prompt = PromptTemplate(
        input_variables=["query", "language"],
        template="Répondez à la question suivante en {language}: {query}"
    )
    llm = OpenAI(api_key="your-openai-api-key")  # Remplacez par l'API réelle
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({"query": query, "language": language})
    return response