"""
Agente Compilador de Documentação do MASS-DAS
"""
import os
from google.adk.agents import Agent
from ..prompts import COMPILADOR_PROMPT

root_agent = Agent(
    model=os.getenv("COMPILADOR_MODEL", "gemini-2.5-pro-preview-06-05"),
    name="compilador_documentacao",
    instruction=COMPILADOR_PROMPT,
) 