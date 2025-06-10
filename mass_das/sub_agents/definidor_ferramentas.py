"""
Agente Definidor de Ferramentas do MASS-DAS
"""
import os
from google.adk.agents import Agent
from ..prompts import DEFINIDOR_FERRAMENTAS_PROMPT

root_agent = Agent(
    model=os.getenv("DEFINIDOR_MODEL", "gemini-2.5-pro-preview-06-05"),
    name="definidor_ferramentas",
    instruction=DEFINIDOR_FERRAMENTAS_PROMPT,
) 