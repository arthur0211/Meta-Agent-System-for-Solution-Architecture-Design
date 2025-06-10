"""
Agente Otimizador de Arquitetura do MASS-DAS
"""
import os
from google.adk.agents import Agent
from ..prompts import OTIMIZADOR_PROMPT

root_agent = Agent(
    model=os.getenv("OTIMIZADOR_MODEL", "gemini-2.5-pro-preview-06-05"),
    name="otimizador_arquitetura",
    instruction=OTIMIZADOR_PROMPT,
) 