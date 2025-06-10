"""
Sub-agentes especializados do MASS-DAS v1.0.0
"""
from .analista import root_agent as analista_agent
from .arquiteto import root_agent as arquiteto_agent
from .especialista_prompts import root_agent as especialista_prompts_agent
from .definidor_ferramentas import root_agent as definidor_ferramentas_agent
from .compilador import root_agent as compilador_agent
from .otimizador import root_agent as otimizador_agent
from .gerador_codigo import gerador_codigo_agent

__all__ = [
    "analista_agent",
    "arquiteto_agent", 
    "especialista_prompts_agent",
    "definidor_ferramentas_agent",
    "compilador_agent",
    "otimizador_agent",
    "gerador_codigo_agent"
] 