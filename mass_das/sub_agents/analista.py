"""
Agente Analista de Requisitos do MASS-DAS
"""
import os
from google.adk.agents import Agent
from ..prompts import ANALISTA_PROMPT

root_agent = Agent(
    model=os.getenv("ANALISTA_MODEL", "gemini-2.5-pro-preview-06-05"),
    name="analista_requisitos",
    instruction=ANALISTA_PROMPT,
) 