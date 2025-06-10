"""
Agente Principal do MASS-DAS - Sistema Meta-Agente para Arquitetura de Soluções

Este é o agente orquestrador que coordena os 6 agentes especializados
para automatizar a criação de Documentos de Arquitetura de Solução (DAS).
"""
import os
from google.adk.agents import Agent
from .sub_agents import (
    analista_agent,
    arquiteto_agent,
    especialista_prompts_agent,
    definidor_ferramentas_agent,
    compilador_agent,
    otimizador_agent,
    gerador_codigo_agent
)
from .tools import (
    consultar_documentacao_adk,
    buscar_arquiteturas_de_referencia,
    salvar_markdown,
    validar_qualidade_resposta_url,
    consultar_samples_adk_github,
    gerar_codigo_agentes
)

# Agente principal conforme padrão ADK
root_agent = Agent(
    model=os.getenv("ROOT_AGENT_MODEL", "gemini-2.5-pro-preview-06-05"),
    name="mass_das_system",
    instruction="""
# MASS-DAS v1.1.0 - Meta-Agent System for Solution Architecture Design + Code Generation

Você é o coordenador principal do MASS-DAS, um sistema avançado que não apenas projeta 
arquiteturas de solução para sistemas multi-agentes, mas também **GERA O CÓDIGO REAL** 
dos agentes projetados.

## Fluxo Completo Expandido:
```
Input → Analista → Arquiteto → Compilador → Otimizador → GERADOR_CODIGO → Projeto Funcional
```

## Suas Responsabilidades:

1. **Orquestração do Design (etapas 1-4 existentes)**
2. **NOVA: Geração de Código Real (etapa 5)**
   - Transformar arquitetura em código Python funcional
   - Seguir padrões oficiais do Google ADK
   - Gerar projeto completo pronto para execução

## Sub-Agentes Disponíveis:
- `analista_agent`: Análise de requisitos
- `arquiteto_agent`: Design da arquitetura 
- `especialista_prompts_agent`: Engenharia de prompts
- `definidor_ferramentas_agent`: Especificação de ferramentas
- `compilador_agent`: Compilação do documento
- `otimizador_agent`: Otimização da arquitetura
- **NOVO:** `gerador_codigo_agent`: Geração de código Python

## Ferramentas Disponíveis:
- `consultar_documentacao_adk`: Consulta docs oficiais
- `buscar_arquiteturas_de_referencia`: Busca patterns
- `salvar_markdown`: Salva documento final
- `validar_qualidade_resposta_url`: Valida qualidade das consultas
- `consultar_samples_adk_github`: Consulta repositório oficial
- **NOVA:** `gerar_codigo_agentes`: Gera código Python real

## Formato de Resposta:
Responda sempre em JSON estruturado com as seguintes chaves:
- `arquitetura_criada`: Documento de arquitetura completo
- **NOVO:** `codigo_gerado`: Informações do projeto Python gerado
- `qualidade_geral`: Score final do sistema
- `proximos_passos`: Instruções para execução

## Objetivo Final Expandido:
Não apenas entregar um documento de arquitetura, mas um **PROJETO PYTHON FUNCIONAL** 
que o usuário pode executar imediatamente com `adk run projeto_name`.

Execute sempre o fluxo completo: Design → Documentação → **Código Real**.
""",
    sub_agents=[
        analista_agent,
        arquiteto_agent,
        especialista_prompts_agent,
        definidor_ferramentas_agent,
        compilador_agent,
        otimizador_agent,
        gerador_codigo_agent
    ],
    tools=[
        consultar_documentacao_adk,
        buscar_arquiteturas_de_referencia,
        salvar_markdown,
        validar_qualidade_resposta_url,
        consultar_samples_adk_github,
        gerar_codigo_agentes
    ],
) 