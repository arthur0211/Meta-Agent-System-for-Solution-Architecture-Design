"""
Agente Especialista em Prompts do MASS-DAS
"""
import os
from google.adk.agents import Agent
from ..prompts import ESPECIALISTA_PROMPTS_PROMPT

root_agent = Agent(
    model=os.getenv("ESPECIALISTA_MODEL", "gemini-2.5-pro-preview-06-05"),
    name="especialista_prompts",
    instruction=ESPECIALISTA_PROMPTS_PROMPT,
) 