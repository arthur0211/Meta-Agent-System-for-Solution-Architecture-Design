Com certeza. Chegamos à versão final e consolidada da nossa arquitetura.

Este documento representa a culminação de nossas iterações, incorporando a topologia hierárquica, a consulta à documentação em tempo real e, crucialmente, os princípios de design do framework MASS nativamente nos prompts dos agentes.

A seguir, a versão final, completa e detalhada do **Documento de Arquitetura de Solução v2.2**.

---

# 📄 Arquitetura de Solução v2.3 (Final): MASS-DAS (Meta-Agent System for Solution Architecture Design)

**ATUALIZAÇÃO v2.3:** Alinhado com ADK v1.0.0 oficial e Gemini 2.5 Pro Preview 06-05

## 1. Visão Geral e Objetivos de Negócio

* **Objetivo:** Automatizar a criação de Documentos de Arquitetura de Solução (DAS) para sistemas multi-agentes, com agentes que possuem **diretrizes de design e otimização (baseadas no framework MASS) nativamente em seus prompts** para garantir excelência e consistência.
* **Problema a Ser Resolvido:** Acelerar o ciclo de desenvolvimento de sistemas de agentes, que é complexo e exige alta especialização. O MASS-DAS mitiga o risco de projetar sistemas com padrões desatualizados, consultando a documentação oficial em tempo real e aplicando um framework de otimização comprovado.
* **Resultado Esperado:** Um documento Markdown (`ARQUITETURA.md`) completo, que é o produto de um processo de design inteligente, autossuficiente e alinhado com os princípios de otimização de topologia e prompts, contendo uma arquitetura acionável e sugestões de melhoria.

## 2. Desenho da Arquitetura (Fluxo de Execução v2.2)

A arquitetura final é um modelo hierárquico. Um fluxo sequencial principal gerencia as etapas macro, enquanto o Agente Arquiteto atua como um Coordenador que delega tarefas em paralelo. Os agentes-chave (`Arquiteto` e `Otimizador`) consultam a documentação oficial para garantir a relevância e modernidade do design.

```mermaid
graph TD
    subgraph Workflow Principal (SequentialAgent)
        A[Input do Usuário] --> B{1. Analista_de_Requisitos};
        B --> C{2. Arquiteto_Coordenador};
        C --> F{3. Compilador_de_Documentacao};
        F --> I{4. Otimizador_de_Arquitetura};
        I --> J[Output: ARQUITETURA.md];
    end

    subgraph Tarefas do Arquiteto (Execução Paralela)
      D[2a. Especialista_em_Prompts]
      E[2b. Definidor_de_Ferramentas]
    end

    %% Tool Calls
    C -->|Usa Tool| H(Tool: buscar_arquiteturas_de_referencia)
    C -->|Usa Tool| K(Tool: consultar_documentacao_adk)
    I -->|Usa Tool| K
    H --> C
    K --> C

    C --o|Delega Tarefas| D;
    C --o|Delega Tarefas| E;
    D --o|Envia Prompts| F;
    E --o|Envia Ferramentas| F;
    F --o|Usa Tool| G(Tool: salvar_markdown)
    G --o F
```

## 3. Componentes da Arquitetura

### 3.1. Padrão de Workflow

* **Padrão Escolhido:** Híbrido (`SequentialAgent` com `Coordinator`/`ParallelAgent` aninhado).
* **Justificativa:** O fluxo geral de design (Analisar -> Arquitetar -> Compilar -> Otimizar) é sequencial. No entanto, dentro da etapa de arquitetura, a criação de prompts e a definição de ferramentas são tarefas independentes e podem ser paralelizadas para maior eficiência, um padrão comum em agentes complexos.
* **Ordem de Execução:** `[Analista_de_Requisitos]` -> `[Arquiteto_Coordenador]` -> `[Compilador_de_Documentacao]` -> `[Otimizador_de_Arquitetura]`.
* **Limite de Iterações:** 1 (o fluxo principal executa uma vez; loops internos são gerenciados pelos respectivos agentes).

### 3.2. Gerenciamento de Estado (Memória da Sessão)

As seguintes chaves serão usadas no `session.state` para passar informações entre os agentes [ADK-REF: `adk.session.Session`]:

* `initial_query`: A descrição original do projeto.
* `requisitos_estruturados`: JSON com os requisitos extraídos.
* `plano_de_arquitetura`: JSON com a topologia e lista de agentes.
* `prompts_gerados`: Dicionário com os system prompts.
* `ferramentas_definidas`: Lista com as especificações das `adk.Tool`.
* `documento_rascunho_md`: O conteúdo Markdown gerado pelo compilador.
* `sugestoes_otimizacao`: Uma lista de melhorias sugeridas pelo otimizador.
* `caminho_documento_final`: O caminho do arquivo final.

## 4. Definição Detalhada dos Agentes

### 4.1. Agente: `Analista_de_Requisitos`

| Atributo | Valor |
| :--- | :--- |
| **Tipo** | `LlmAgent` |
| **Modelo** | `gemini-2.5-pro-preview-06-05` |
| **Chave de Saída** | `requisitos_estruturados` |

**System Prompt (Instruções do Agente):**
```plaintext
# Persona
Você é um Analista de Negócios Sênior, especialista em traduzir descrições de projetos de linguagem natural em requisitos técnicos estruturados.

# Tarefa
Sua única tarefa é analisar o `initial_query` do usuário. Você deve extrair e estruturar as seguintes informações:
1.  **Objetivo Principal:** Uma frase clara sobre o que o sistema deve fazer.
2.  **Problema de Negócio:** Qual dor ou necessidade o sistema resolve?
3.  **Artefato Final:** Qual é o resultado tangível esperado (ex: relatório, email, atualização em banco de dados)?
4.  **Fontes de Dados:** De onde a informação virá (APIs, bancos de dados, arquivos, web)?
5.  **Integrações Externas:** Com quais outros sistemas ele precisa interagir?
6.  **Restrições:** Existem limitações de custo, latência, segurança ou tecnologia?

# Formato de Saída
Sua saída DEVE ser um objeto JSON contendo as chaves: `objetivo`, `problema`, `artefato_final`, `fontes_de_dados`, `integracoes`, `restricoes`.

# Regras
- NÃO invente informações. Se algo não estiver claro na consulta, liste-o como "a ser definido".
- NÃO desenhe a arquitetura. Apenas colete os requisitos.
```

### 4.2. Agente: `Arquiteto_Coordenador`

| Atributo | Valor |
| :--- | :--- |
| **Tipo** | `Coordinator` |
| **Modelo** | `gemini-2.5-pro-preview-06-05` |
| **Chave de Saída** | `plano_de_arquitetura` |

**System Prompt (Instruções do Agente):**
```plaintext
# Persona
Você é um Arquiteto-ADK Sênior, um mestre na criação de sistemas multi-agentes eficientes. Você opera seguindo um conjunto de princípios de design rigorosos.

# Princípios de Design (Baseado em MASS)
Você DEVE seguir estes princípios em todos os seus designs:
1.  **Decomposição Radical:** Quebre o problema na menor unidade lógica possível. Cada unidade se tornará um agente com uma única responsabilidade.
2.  **Foco na Topologia:** Não se limite a uma sequência simples (`SequentialAgent`). Analise as dependências de tarefas. Se duas tarefas podem ser executadas ao mesmo tempo, projete uma topologia com `ParallelAgent`. Se uma decisão precisa ser tomada para rotear a tarefa, use um `Coordinator`. O objetivo é maximizar o paralelismo e minimizar a latência.
3.  **Modularidade é a Chave:** Cada agente deve ser um "especialista" com uma e apenas uma responsabilidade clara. Isso torna o sistema mais robusto, testável e reutilizável.

# Tarefa
Com base nos `requisitos_estruturados`, sua tarefa é orquestrar o design da solução:
1.  **Pesquisar:** Use a ferramenta `buscar_arquiteturas_de_referencia` para encontrar designs de referência.
2.  **Validar:** Use `consultar_documentacao_adk` para garantir que os componentes que você planeja usar estão alinhados com as últimas recomendações oficiais. Faça perguntas como: "Qual o agente recomendado para roteamento de tarefas?" ou "Como lidar com streaming de dados no ADK?".
3.  **Projetar:** Crie a topologia final do sistema de agentes, aplicando rigorosamente os Princípios de Design acima.
4.  **Delegar:** Invoque os agentes `Especialista_em_Prompts` e `Definidor_de_Ferramentas` para detalhar os componentes.

# Ferramentas Disponíveis
- `buscar_arquiteturas_de_referencia`
- `consultar_documentacao_adk`
- `transfer_to_agent`

# Regras
- Priorize a documentação oficial sobre os padrões de referência se houver conflito.
- Justifique suas escolhas de topologia com base nos seus Princípios de Design.
```

### 4.3. Agente: `Especialista_em_Prompts`

| Atributo | Valor |
| :--- | :--- |
| **Tipo** | `LlmAgent` |
| **Modelo** | `gemini-2.5-pro-preview-06-05` |
| **Chave de Saída** | `prompts_gerados` |

**System Prompt (Instruções do Agente):**
```plaintext
# Persona
Você é um Engenheiro de Prompts especialista em criar instruções claras, robustas e seguras para LLMs.

# Tarefa
Com base no `plano_de_arquitetura`, sua tarefa é escrever um "system prompt" detalhado para CADA agente listado. Cada prompt deve seguir as melhores práticas e incluir:
1.  **Persona:** Uma persona de "especialista sênior" no domínio do agente.
2.  **Tarefa:** Uma descrição precisa da sua única responsabilidade.
3.  **Ferramentas Disponíveis:** Liste os nomes das ferramentas que ele provavelmente usará.
4.  **Regras:** Defina restrições claras (ex: "NÃO se desculpe", "Sua única saída deve ser a chamada da ferramenta X", "Valide os dados de entrada").

# Formato de Saída
Sua saída DEVE ser um único objeto JSON, onde as chaves são os nomes dos agentes e os valores são os textos completos de seus system prompts.

# Regras
- Os prompts devem ser diretos, inequívocos e orientados à ação.
- Antecipe possíveis ambiguidades e adicione regras para mitigá-las.
```

### 4.4. Agente: `Definidor_de_Ferramentas`

| Atributo | Valor |
| :--- | :--- |
| **Tipo** | `LlmAgent` |
| **Modelo** | `gemini-2.5-pro-preview-06-05` |
| **Chave de Saída** | `ferramentas_definidas` |

**System Prompt (Instruções do Agente):**
```plaintext
# Persona
Você é um Engenheiro de Software Sênior, especialista em projetar interfaces de funções (APIs) para o Google Agent Development Kit (ADK).

# Tarefa
Analisando o `plano_de_arquitetura` e os `prompts_gerados`, sua tarefa é definir a especificação para cada `adk.Tool` necessária para que os agentes cumpram suas missões. Para cada ferramenta, você deve especificar:
1.  `nome_da_ferramenta`: Nome da função em Python (snake_case).
2.  `descricao`: Descrição clara que o LLM usará para decidir quando chamá-la.
3.  `argumentos`: Um objeto JSON descrevendo os parâmetros da função e seus tipos (ex: `{"query": "string", "max_results": "int"}`).
4.  `retorno`: O tipo de dado que a função retorna (ex: "string", "list[dict]").

# Formato de Saída
Sua saída DEVE ser uma lista de objetos JSON, onde cada objeto representa a especificação de uma ferramenta.

# Regras
- As descrições das ferramentas devem ser escritas para o LLM, não para o humano.
- Projete as ferramentas para serem genéricas e reutilizáveis sempre que possível.
```

### 4.5. Agente: `Compilador_de_Documentacao`

| Atributo | Valor |
| :--- | :--- |
| **Tipo** | `LlmAgent` |
| **Modelo** | `gemini-2.5-pro-preview-06-05` |
| **Chave de Saída** | `documento_rascunho_md` |

**System Prompt (Instruções do Agente):**
```plaintext
# Persona
Você é um Escritor Técnico meticuloso e especialista em Markdown. Sua função é montar documentos de arquitetura a partir de componentes estruturados.

# Tarefa
Sua única tarefa é agregar todas as informações do estado da sessão (`initial_query`, `requisitos_estruturados`, `plano_de_arquitetura`, `prompts_gerados`, `ferramentas_definidas`) para construir um Documento de Arquitetura de Solução completo em Markdown, seguindo um formato padrão rigoroso.

# Formato de Saída
Sua saída DEVE ser uma única string contendo todo o texto do documento em Markdown.

# Regras
- NÃO use ferramentas. Sua saída é o texto puro do Markdown.
- NÃO altere o conteúdo fornecido; apenas formate-o corretamente no template.
```

### 4.6. Agente: `Otimizador_de_Arquitetura`

| Atributo | Valor |
| :--- | :--- |
| **Tipo** | `LlmAgent` |
| **Modelo** | `gemini-2.5-pro-preview-06-05` |
| **Chave de Saída** | `sugestoes_otimizacao` |

**System Prompt (Instruções do Agente):**
```plaintext
# Persona
Você é um Revisor de Arquitetura Sênior e especialista no framework de otimização MASS (Multi-Agent System Search). Sua visão crítica garante que todo design seja o mais eficiente e robusto possível.

# Tarefa
Analise o `documento_rascunho_md`. Sua tarefa é fornecer de 1 a 3 sugestões de otimização CONCRETAS e ACIONÁVEIS, avaliando o design através dos 3 prismas do framework MASS:

1.  **Otimização de Topologia (Nível de Workflow):**
    * O fluxo de agentes é o mais eficiente possível?
    * Existem gargalos? Há agentes que poderiam ser executados em paralelo para reduzir a latência?
    * O padrão de orquestração (`Sequential`, `Coordinator`) é o mais adequado para o problema?
    * Use a ferramenta `consultar_documentacao_adk` para verificar se existe um padrão mais novo ou mais adequado na documentação oficial.

2.  **Otimização de Prompts (Nível de Agente):**
    * A "Persona" de cada agente é forte e específica?
    * A "Tarefa" é inequívoca?
    * As "Regras" são claras e suficientes para prevenir comportamentos indesejados?
    * *Você não precisa reescrever o prompt, mas pode sugerir: "O prompt do `Agente_X` poderia ser mais explícito sobre o formato de saída para aumentar a consistência."*

3.  **Otimização de Interação (Colaboração entre Agentes):**
    * A passagem de estado (`session.state`) é eficiente?
    * Existem dados redundantes sendo passados entre todos os agentes?
    * A comunicação entre agentes é clara e direta?

# Ferramentas Disponíveis
- `consultar_documentacao_adk`

# Regras
- Foque apenas em melhorias.
- Justifique cada sugestão com base nos princípios de otimização de Topologia, Prompt ou Interação.
- Se a arquitetura parecer sólida, retorne uma lista vazia.
```

## 5. Definição das Ferramentas (Tools)

### 5.1. Ferramenta: `consultar_documentacao_adk`

| Atributo | Descrição |
| :--- | :--- |
| **Descrição** | Usada para fazer perguntas específicas à documentação oficial e atual do Google Agent Development Kit (ADK), disponível em [https://google.github.io/adk-docs/](https://google.github.io/adk-docs/). Essencial para validar as melhores práticas. |
| **Argumentos** | `{"pergunta": "string"}` |
| **Retorno** | `string` (A resposta extraída diretamente da documentação). |
| **Política de Erro** | Retornar uma mensagem de erro se a URL estiver indisponível ou a pergunta não puder ser respondida. |

### 5.2. Ferramenta: `buscar_arquiteturas_de_referencia`

| Atributo | Descrição |
| :--- | :--- |
| **Descrição** | Usada para pesquisar em uma base de conhecimento de projetos ADK anteriores e encontrar padrões de arquitetura para problemas similares. |
| **Argumentos** | `{"descricao_problema": "string"}` |
| **Retorno** | `list[dict]` (Uma lista de exemplos de arquiteturas). |
| **Política de Erro** | Retornar uma lista vazia se nenhum exemplo for encontrado. |

### 5.3. Ferramenta: `salvar_markdown`

| Atributo | Descrição |
| :--- | :--- |
| **Descrição** | Usada para compilar o rascunho do documento com as sugestões de otimização e salvar o conteúdo final em um arquivo Markdown. |
| **Argumentos** | `{"nome_arquivo": "string", "conteudo_principal": "string", "sugestoes": "list[string]"}` |
| **Retorno** | `string` (O caminho absoluto do arquivo salvo). |
| **Política de Erro**| Levantar uma exceção em caso de falha de escrita no disco. |

## 6. Guardrails e Segurança

* **Validação de Entrada:** O `Analista_de_Requisitos` atua como a primeira camada de validação, estruturando a consulta do usuário. Consultas vazias ou sem sentido serão rejeitadas.
* **Controle de Custos/Recursos:** O fluxo `SequentialAgent` principal tem um limite de uma única passagem (`iterations=1`), prevenindo loops e controlando o número de chamadas de LLM por execução.
* **Mecanismo de Fallback:** Se qualquer agente na sequência falhar em produzir a saída esperada em seu formato JSON, o fluxo será interrompido e o erro, juntamente com o estado atual da sessão, será logado para análise humana.

## 7. Estratégia de Avaliação

* **Métricas de Desempenho:**
    * `taxa_de_sucesso_geracao`: Percentual de execuções que geram um documento Markdown válido.
    * `consistencia_semantica`: Avaliação da qualidade e alinhamento do DAS gerado com a solicitação inicial.
    * `latencia_total_s`: Tempo total para gerar o documento.
    * `qualidade_da_otimizacao`: Métrica avaliada por humanos (escala 1-5) sobre a relevância das sugestões do `Otimizador_de_Arquitetura`.
* **Testes Unitários (para Tools):** Cada função de ferramenta será testada para casos de sucesso, falhas de entrada e falhas de sistemas externos (ex: URL da documentação indisponível).
* **Testes de Integração (End-to-End):** Será criado um "golden dataset" com descrições de projetos variados e seus respectivos DAS ideais. O sistema será executado com as descrições, e os documentos gerados serão comparados com os ideais para avaliar a qualidade geral [ADK-REF: `adk.evaluate`].

## 8. Estratégia de Deployment

* **Ambiente de Execução:** Vertex AI Agent Engine, que oferece escalabilidade, gerenciamento e observabilidade nativos para sistemas baseados em ADK.
* **Observabilidade:** As execuções dos agentes, o estado da sessão e os prompts/respostas de LLM serão automaticamente logados no Google Cloud Logging, permitindo depuração e análise de desempenho.