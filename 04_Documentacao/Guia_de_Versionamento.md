# Guia de Versionamento

## 1. Modelo de branches (GitHub Flow)

| Branch | Uso |
|---|---|
| `main` | Versão estável — é a que o GitHub Pages publica |
| `feature/<nome>` | Nova funcionalidade (ex.: `feature/slides`) |
| `docs/<nome>` | Mudanças só de documentação |
| `fix/<nome>` | Correções |

Fluxo: `git switch -c feature/x` → commits → `git push -u origin feature/x` → **Pull Request** → revisão → *merge* na `main` → apagar a branch.

## 2. Mensagens de commit (Conventional Commits)

```text
<tipo>(escopo opcional): descrição no imperativo
```

| Tipo | Quando usar | Exemplo |
|---|---|---|
| `feat` | Nova funcionalidade | `feat(site): adiciona seção de projetos` |
| `fix` | Correção | `fix(site): corrige link quebrado no menu` |
| `docs` | Documentação | `docs: atualiza README da disciplina` |
| `style` | Formatação/CSS sem mudar lógica | `style(site): ajusta cores do tema` |
| `chore` | Manutenção | `chore: adiciona .gitignore` |

## 3. Versões (SemVer) e tags

`MAJOR.MINOR.PATCH` — `MAJOR` muda a estrutura, `MINOR` adiciona conteúdo, `PATCH` corrige.

```bash
git tag -a v1.0.0 -m "Versão 1.0: estrutura inicial + GitHub Pages"
git push origin --tags
```

Cada tag gera uma **Release** no GitHub com as notas do [CHANGELOG](../CHANGELOG.md).

## 4. Histórico deste repositório

```bash
git log --oneline --graph --decorate --all
```
