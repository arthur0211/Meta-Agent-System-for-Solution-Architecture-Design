"""
Agente Arquiteto Coordenador do MASS-DAS
"""
import os
from google.adk.agents import Agent
from ..prompts import ARQUITETO_PROMPT

root_agent = Agent(
    model=os.getenv("ARQUITETO_MODEL", "gemini-2.5-pro-preview-06-05"),
    name="arquiteto_coordenador",
    instruction=ARQUITETO_PROMPT,
) 