<div align="center">

# 📚 Meu Study Hub TI

**Portfólio acadêmico e profissional de Eduardo do Vale Giannetti**
Ciência da Computação · Turma A (Noturno)

[![GitHub Pages](https://img.shields.io/badge/site-GitHub%20Pages-0b3d91?logo=github)](https://yelllowww.github.io/Meu_Study_Hub_TI/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Eduardo%20Giannetti-0A66C2?logo=linkedin)](https://www.linkedin.com/in/eduardo-do-vale-giannetti-90a27032b)
![Versão](https://img.shields.io/github/v/tag/Yelllowww/Meu_Study_Hub_TI?label=vers%C3%A3o)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green)

</div>

---

## 🎯 Sobre este repositório

O **Study Hub** é o ponto central onde organizo tudo o que produzo durante o curso de Ciência da Computação: atividades das disciplinas, anotações, projetos acadêmicos e pessoais e certificados. Cada material é versionado com Git, documentado com um `README.md` próprio e publicado em um site estático via **GitHub Pages**.

Objetivos:

- **Organizar** a produção do curso em uma estrutura previsível e padronizada;
- **Demonstrar evolução** prática através do histórico de commits e versões (tags);
- **Compor um perfil profissional** integrado ao LinkedIn.

🌐 **Site:** https://yelllowww.github.io/Meu_Study_Hub_TI/

---

## 🗂️ Arquitetura de pastas

```text
Meu_Study_Hub_TI/
├── 01_Apresentacao_e_Perfil/          → quem sou, objetivos e áreas de interesse
├── 02_Disciplinas_Atuais/
│   ├── Bootcamp_I/
│   │   ├── Atividades_e_Entregas/     → Etapa Inicial e Etapa Intermediária
│   │   └── Anotacoes_e_Resumos/       → resumos de Git, GitHub e Markdown
│   ├── Sistemas_Tempo_Real_e_Embarcados/
│   ├── Testes_e_Qualidade_de_Software/
│   ├── Projeto_Integrador/
│   ├── Seguranca_Digital/
│   ├── Analise_e_Producao_de_Texto/
│   └── Etica_Cidadania_e_Realidade_Brasileira/
├── 03_Projetos_e_Certificados/
│   ├── Projetos_Academicos/
│   ├── Projetos_Pessoais/
│   └── Certificados/
├── assets/                             → CSS, JS e imagens do site
├── index.html                          → página inicial (GitHub Pages)
├── slides.html                         → apresentação do repositório
├── CHANGELOG.md · LICENSE
```

### Convenções de nomenclatura

| Regra | Exemplo |
|---|---|
| Pastas de nível 1 numeradas para manter a ordem | `01_`, `02_`, `03_`, `04_` |
| Palavras separadas por `_`, sem acentos ou espaços | `Seguranca_Digital` |
| Toda pasta tem um `README.md` explicando seu conteúdo | `Bootcamp_I/README.md` |
| Arquivos de entrega com data ISO | `2026-10-17_Etapa_Intermediaria.pdf` |

---

## 🔖 Versionamento

O projeto segue **[Versionamento Semântico](https://semver.org/lang/pt-BR/)** e **[Conventional Commits](https://www.conventionalcommits.org/pt-br/)**. As versões são marcadas com *tags* e descritas no [CHANGELOG](CHANGELOG.md).

| Versão | Conteúdo |
|---|---|
| `v1.0.0` | Estrutura inicial do repositório + página web no GitHub Pages |
| `v1.1.0` | Slides de apresentação do repositório |

Fluxo de trabalho:

```text
main ──●────────●──────────●───────── (sempre estável, publicada no Pages)
        \      /  \        /
feature  ●──●─●    ●──●──●            (uma branch por funcionalidade → Pull Request)
```

---

## 🚀 Destaques

| Projeto | Descrição | Tecnologias |
|---|---|---|
| [Site do Study Hub](index.html) | Portfólio publicado com GitHub Pages | HTML, CSS, JavaScript |
| [Planejamento do Study Hub](02_Disciplinas_Atuais/Bootcamp_I/Atividades_e_Entregas/) | Fase 1 e Fase 2 do projeto integrador do Bootcamp I | Git, GitHub, Markdown |

---

## 💻 Como executar localmente

```bash
git clone https://github.com/Yelllowww/Meu_Study_Hub_TI.git
cd Meu_Study_Hub_TI
# abra o index.html no navegador ou rode um servidor simples:
python -m http.server 8000   # acesse http://localhost:8000
```

---

## 📬 Contato

- **LinkedIn:** [eduardo-do-vale-giannetti](https://www.linkedin.com/in/eduardo-do-vale-giannetti-90a27032b)
- **GitHub:** [@Yelllowww](https://github.com/Yelllowww)

<sub>Conteúdo licenciado sob [MIT](LICENSE). Materiais de disciplinas são de autoria própria; enunciados pertencem às respectivas instituições.</sub>
