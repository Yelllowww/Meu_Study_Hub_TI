# Guia de Colaboração

## Estratégias

| Situação | Estratégia |
|---|---|
| Colega com acesso ao repositório (Projeto Integrador) | Adicionar como *collaborator* → cada um trabalha em sua branch → Pull Request |
| Pessoa externa quer sugerir algo | **Fork** → branch → Pull Request para este repositório |
| Reportar problema ou ideia | Abrir uma **Issue** usando os templates em `.github/ISSUE_TEMPLATE` |

## Boas práticas de Pull Request

- Um PR = um assunto; título no padrão Conventional Commits;
- Descrever **o que** mudou e **por quê** (o template `.github/pull_request_template.md` ajuda);
- Pedir revisão e resolver os comentários antes do merge;
- Usar `Closes #<n>` para fechar a issue relacionada automaticamente.

## Resolvendo conflitos

```bash
git switch main && git pull
git switch feature/x
git merge main          # resolver os arquivos marcados, depois:
git add . && git commit
```
