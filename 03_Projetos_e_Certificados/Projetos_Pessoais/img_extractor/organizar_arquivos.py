#!/usr/bin/env python3
"""
organizar_arquivos.py
---------------------
Para cada arquivo informado:
  1. Cria uma pasta com o mesmo nome (sem extensão).
  2a. Se o arquivo for ZIP válido por dentro (docx, xlsx, pptx, zip, jar, odt…)
      → extrai o conteúdo, move os arquivos de word/media/ para a pasta raiz
        e apaga todo o restante extraído (XMLs internos, _rels, etc.).
  2b. Caso contrário (txt, jpg, pdf…)
      → apenas move o arquivo para dentro da pasta, sem renomear.

Uso:
  python organizar_arquivos.py arquivo1.docx arquivo2.txt arquivo3.zip ...
  python organizar_arquivos.py --dir /caminho/pasta
  python organizar_arquivos.py --dir pasta1 pasta2 pasta3
  python organizar_arquivos.py --dir pasta1 pasta2 --recursive
  python organizar_arquivos.py --dir pasta1 pasta2 -R --dry-run
"""

import argparse
import sys
import shutil
import zipfile
from pathlib import Path


def eh_zip_valido(caminho: Path) -> bool:
    """Retorna True se o arquivo for um ZIP válido (independente da extensão)."""
    return zipfile.is_zipfile(caminho)


def extrair_midia_docx(pasta_destino: Path, dry_run: bool = False) -> tuple[int, list[str]]:
    """
    Após a extração de um ZIP do tipo Office (docx, pptx, etc.):
      1. Localiza TODOS os arquivos dentro de qualquer subpasta chamada 'media'
         (ex: word/media/, ppt/media/, xl/media/).
      2. Move esses arquivos para a pasta_destino (raiz).
      3. Apaga tudo o que sobrou dentro de pasta_destino (subpastas e XMLs).

    Retorna (quantidade_de_midias_movidas, lista_de_nomes_movidos).
    """
    # Coleta todos os arquivos de mídia em qualquer pasta 'media' dentro do ZIP
    arquivos_midia = []
    for item in pasta_destino.rglob("*"):
        if item.is_file() and item.parent.name.lower() == "media":
            arquivos_midia.append(item)

    if dry_run:
        nomes = [f.name for f in arquivos_midia]
        return len(nomes), nomes

    # Move mídias para a raiz da pasta_destino, evitando colisão de nomes
    movidos = []
    for arquivo in arquivos_midia:
        destino = pasta_destino / arquivo.name
        # Se já existe um arquivo com o mesmo nome, adiciona sufixo numérico
        contador = 1
        while destino.exists():
            destino = pasta_destino / f"{arquivo.stem}_{contador}{arquivo.suffix}"
            contador += 1
        shutil.move(str(arquivo), str(destino))
        movidos.append(destino.name)

    # Remove tudo que não é arquivo direto na raiz (subpastas e seus conteúdos)
    for item in list(pasta_destino.iterdir()):
        if item.is_dir():
            shutil.rmtree(item)

    return len(movidos), movidos


def processar_arquivo(caminho: Path, dry_run: bool = False) -> tuple[bool, str]:
    if not caminho.exists():
        return False, f"[ERRO]   Arquivo não encontrado: {caminho}"
    if not caminho.is_file():
        return False, f"[AVISO]  Ignorado (não é arquivo): {caminho}"

    pasta_destino = caminho.parent / caminho.stem

    if pasta_destino.exists() and any(pasta_destino.iterdir()):
        return False, f"[AVISO]  Pasta já existe e não está vazia, pulando: {pasta_destino}"

    zip_valido = eh_zip_valido(caminho)

    # ── ZIP válido por dentro: extrai, promove mídias e limpa o resto ────────
    if zip_valido:
        zip_temporario = caminho.parent / (caminho.stem + ".zip")

        if dry_run:
            with zipfile.ZipFile(caminho, "r") as zf:
                membros = zf.namelist()
            # Simula quais mídias seriam movidas
            pasta_destino.mkdir(parents=True, exist_ok=True)
            if caminho != zip_temporario:
                caminho.rename(zip_temporario)
            with zipfile.ZipFile(zip_temporario, "r") as zf:
                zf.extractall(pasta_destino)
            qtd_midia, nomes_midia = extrair_midia_docx(pasta_destino, dry_run=True)
            # Desfaz a extração temporária
            shutil.rmtree(pasta_destino)
            if zip_temporario != caminho and zip_temporario.exists():
                zip_temporario.rename(caminho)
            midia_info = (
                f"\n           Mídias encontradas : {qtd_midia} arquivo(s)"
                + (f"\n           → {', '.join(nomes_midia)}" if nomes_midia else "")
            )
            return True, (
                f"[DRY-RUN] {caminho.name}  (ZIP válido)\n"
                f"           Criaria pasta : {pasta_destino}\n"
                f"           Extrairia     : {len(membros)} item(ns) internos\n"
                f"           Moveria mídias para a raiz da pasta"
                f"{midia_info}\n"
                f"           Apagaria      : subpastas e XMLs internos"
            )

        try:
            pasta_destino.mkdir(parents=True, exist_ok=True)
            # Renomeia para .zip (se já não for)
            if caminho != zip_temporario:
                caminho.rename(zip_temporario)
            with zipfile.ZipFile(zip_temporario, "r") as zf:
                membros = zf.namelist()
                zf.extractall(pasta_destino)
            zip_temporario.unlink()

            # Extrai mídias para a raiz e limpa o restante
            qtd_midia, nomes_midia = extrair_midia_docx(pasta_destino)

            if qtd_midia == 0:
                return True, (
                    f"[OK]     {caminho.name}  →  extraído em '{pasta_destino.name}/'\n"
                    f"         [AVISO] Nenhum arquivo de mídia encontrado em word/media/"
                )

            return True, (
                f"[OK]     {caminho.name}  →  {qtd_midia} mídia(s) salvas"
                f" em '{pasta_destino.name}/'\n"
                f"         Arquivos: {', '.join(nomes_midia)}"
            )
        except Exception as exc:
            return False, f"[ERRO]   {caminho}: {exc}"

    # ── Outros (jpg, png, pdf, txt…): ignora e deixa no lugar ───────────────
    return False, f"[SKIP]   {caminho.name}  (não é ZIP, ignorado)"


def coletar_arquivos_recursivo(raiz: Path) -> list[Path]:
    """
    Percorre o diretório raiz recursivamente (equivalente a find -R / os.walk).

    Regras para evitar loops e reprocessamento:
      - Ignora pastas que já foram criadas por uma execução anterior do script
        (heurística: pasta cujo nome bate com um arquivo-irmão sem extensão).
      - Visita subdiretórios em ordem alfabética para comportamento previsível.
      - Coleta apenas arquivos regulares (não symlinks de pasta, etc.).
    """
    arquivos: list[Path] = []

    def _visitar(pasta: Path, profundidade: int = 0) -> None:
        try:
            entradas = sorted(pasta.iterdir())
        except PermissionError:
            print(f"[AVISO]  Sem permissão para acessar: {pasta}", file=sys.stderr)
            return

        # Nomes de arquivos presentes nesta pasta (sem extensão) — usados para
        # detectar pastas que já são "destino" de uma extração/movimentação.
        nomes_arquivo = {e.stem for e in entradas if e.is_file()}

        for entrada in entradas:
            if entrada.is_file():
                arquivos.append(entrada)
            elif entrada.is_dir():
                # Pula pastas que parecem ter sido criadas pelo próprio script
                # (mesmo nome que um arquivo-irmão sem extensão) para não
                # reprocessar conteúdo já organizado.
                if entrada.name in nomes_arquivo:
                    indent = "  " * profundidade
                    print(
                        f"{indent}[SKIP]   Subpasta ignorada (parece destino já criado):"
                        f" {entrada}"
                    )
                    continue
                _visitar(entrada, profundidade + 1)

    _visitar(raiz)
    return arquivos


def coletar_arquivos(args) -> list[tuple[Path, int, Path]]:
    """
    Retorna lista de (caminho, profundidade, raiz) para exibição hierárquica no log.
    Profundidade 0 = raiz informada pelo usuário.
    Suporta múltiplos diretórios em --dir (separados por espaço).
    """
    if args.dir:
        resultado = []
        for dir_str in args.dir:
            pasta = Path(dir_str)
            if not pasta.is_dir():
                print(f"[ERRO] Diretório não encontrado: {pasta}", file=sys.stderr)
                continue

            if args.recursive:
                arquivos_brutos = coletar_arquivos_recursivo(pasta)
            else:
                arquivos_brutos = [p for p in pasta.iterdir() if p.is_file()]

            if not arquivos_brutos:
                print(f"[AVISO] Nenhum arquivo encontrado em: {pasta}")
                continue

            for p in sorted(arquivos_brutos):
                try:
                    profundidade = len(p.relative_to(pasta).parts) - 1
                except ValueError:
                    profundidade = 0
                resultado.append((p, profundidade, pasta))

        if not resultado:
            sys.exit(1)
        return resultado

    # Arquivos passados diretamente na linha de comando
    return [(Path(f), 0, Path(f).parent) for f in args.arquivos]


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Organiza arquivos em pastas individuais.\n"
            "  ZIP válido (docx, xlsx, zip…) → extrai o conteúdo na pasta.\n"
            "  Outros (txt, jpg, pdf…)        → apenas move para a pasta.\n\n"
            "  Use --recursive / -R para percorrer subdiretórios."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("arquivos", nargs="*", metavar="ARQUIVO")
    parser.add_argument(
        "--dir", metavar="DIRETÓRIO", nargs="+",
        help="Um ou mais diretórios a processar (separados por espaço).",
    )
    parser.add_argument(
        "--recursive", "-R", action="store_true",
        help=(
            "Percorre subdiretórios recursivamente (requer --dir). "
            "Equivale ao comportamento de 'find -R' do Linux."
        ),
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Simula as operações sem alterar nada.",
    )

    args = parser.parse_args()

    if args.recursive and not args.dir:
        parser.error("--recursive / -R só pode ser usado junto com --dir.")

    if not args.arquivos and not args.dir:
        parser.print_help()
        sys.exit(0)

    pares = coletar_arquivos(args)  # lista de (Path, profundidade, raiz)
    if not pares:
        print("Nenhum arquivo para processar.")
        sys.exit(0)

    num_dirs = len({raiz for _, _, raiz in pares}) if args.dir else 0
    modo = "RECURSIVO" if args.recursive else "SIMPLES"
    print(f"\n{'='*60}")
    print(f"  Modo                 : {modo}")
    if num_dirs > 1:
        print(f"  Diretórios           : {num_dirs}")
    print(f"  Arquivos a processar : {len(pares)}")
    if args.dry_run:
        print("  MODO DRY-RUN ativo   : nenhuma alteração será feita")
    print(f"{'='*60}\n")

    # Rastreia pasta atual para exibir cabeçalhos de seção
    raiz_atual: Path | None = None
    pasta_atual: Path | None = None
    sucessos = falhas = ignorados = 0

    for caminho, profundidade, raiz in pares:
        # Cabeçalho de diretório raiz (sempre que muda, inclusive sem -R)
        if args.dir and raiz != raiz_atual:
            raiz_atual = raiz
            pasta_atual = None  # reseta subpasta ao trocar de raiz
            print(f"\n📂 {raiz}")
            print(f"{'═' * 55}")

        # Cabeçalho de subdiretório (modo recursivo, quando muda dentro da raiz)
        if args.recursive and caminho.parent != pasta_atual:
            pasta_atual = caminho.parent
            if caminho.parent != raiz_atual:
                indent = "  " * profundidade
                print(f"\n{indent}📁 {caminho.parent}")
                print(f"{'  ' * profundidade}{'─' * (55 - profundidade * 2)}")

        indent = "  " * profundidade
        ok, msg = processar_arquivo(caminho, dry_run=args.dry_run)

        # Indenta cada linha da mensagem de acordo com a profundidade
        msg_indentada = "\n".join(f"{indent}{linha}" for linha in msg.splitlines())
        print(msg_indentada)

        if ok:
            sucessos += 1
        elif "[SKIP]" not in msg:
            falhas += 1
        else:
            ignorados += 1

    print(f"\n{'='*60}")
    print(f"  Concluído — Sucesso: {sucessos}  |  Ignorados: {ignorados}  |  Falhas/Avisos: {falhas}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
