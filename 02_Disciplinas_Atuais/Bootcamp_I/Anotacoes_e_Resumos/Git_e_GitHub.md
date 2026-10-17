# Git e GitHub — Resumo

## As três áreas do Git

```text
Working Directory ──git add──▶ Staging Area ──git commit──▶ Repositório Local ──git push──▶ GitHub
        ▲                                                                              │
        └──────────────────────────────── git pull ◀──────────────────────────────────┘
```

| Área | O que é |
|---|---|
| **Working Directory** | Os arquivos como estão na minha máquina |
| **Staging Area** | O que foi selecionado (`git add`) para o próximo commit |
| **Repositório** | O histórico de commits (`.git`) |
| **Remoto (GitHub)** | Cópia do repositório na nuvem, compartilhada |

## Comandos essenciais

| Comando | Para que serve |
|---|---|
| `git init` | Cria um repositório |
| `git clone <url>` | Copia um repositório remoto |
| `git status` | Mostra o estado dos arquivos |
| `git add <arquivo>` | Envia alterações para a staging area |
| `git commit -m "msg"` | Registra um snapshot no histórico |
| `git log --oneline --graph` | Mostra o histórico |
| `git switch -c <branch>` | Cria e muda para uma nova branch |
| `git merge <branch>` | Junta uma branch na atual |
| `git push` / `git pull` | Envia / recebe alterações do remoto |
| `git tag -a v1.0.0 -m "msg"` | Marca uma versão |

## Boas práticas

- Commits pequenos e com mensagem clara (`feat:`, `fix:`, `docs:`...);
- `main` sempre estável; trabalho novo em *branches* + *Pull Request*;
- Nunca versionar senhas ou arquivos gerados (use `.gitignore`).
