# 🔧 Configuração do MASS-DAS

Para executar o MASS-DAS, você precisa criar um arquivo `.env` na raiz do projeto com:

```bash
# Configurações do MASS-DAS
# =========================

# Google Gemini API Key (obrigatório)
# Obtenha em: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=sua_chave_gemini_aqui

# Modelo padrão do agente principal 
ROOT_AGENT_MODEL=gemini-2.5-pro-preview-06-05

# GitHub Token (opcional - para rate limit maior)
# Obtenha em: https://github.com/settings/tokens
# GITHUB_TOKEN=seu_token_github_aqui

# Configurações adicionais
DEBUG=true
ENVIRONMENT=development
```

## Como obter as chaves:

### 1. Gemini API Key (Obrigatório)
1. Acesse: https://makersuite.google.com/app/apikey
2. Clique em "Create API Key"
3. Copie a chave gerada
4. Cole no campo `GEMINI_API_KEY`

### 2. GitHub Token (Opcional)
1. Acesse: https://github.com/settings/tokens
2. Clique em "Generate new token" → "Classic"
3. Selecione escopo "public_repo"
4. Copie o token gerado
5. Descomente e cole no campo `GITHUB_TOKEN`

## Comandos para execução:

```bash
# Executar CLI interativo
poetry run adk run mass_das

# Executar interface web
poetry run adk web

# Ver ajuda
poetry run adk run mass_das --help
``` 