#!/usr/bin/env python3
"""
CLI Tool para Download de Arquivos do /vercel/sandbox

Uso:
    python download_cli.py list                    # Lista todos os arquivos
    python download_cli.py info                    # Mostra informações do sandbox
    python download_cli.py copy <arquivo> <destino> # Copia arquivo para destino
    python download_cli.py zip <nome_arquivo>      # Cria arquivo ZIP do projeto
"""

import sys
import os
import shutil
import zipfile
from pathlib import Path
import json

SANDBOX_DIR = Path("/vercel/sandbox")

def list_files():
    """Lista todos os arquivos no sandbox"""
    print(f"\n📂 Arquivos em {SANDBOX_DIR}:\n")
    print(f"{'Arquivo':<50} {'Tamanho':<15}")
    print("-" * 65)
    
    total_size = 0
    file_count = 0
    
    for item in sorted(SANDBOX_DIR.rglob("*")):
        if item.is_file() and not str(item).startswith(str(SANDBOX_DIR / ".git")):
            relative_path = item.relative_to(SANDBOX_DIR)
            size = item.stat().st_size
            total_size += size
            file_count += 1
            
            # Formatar tamanho
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.2f} KB"
            else:
                size_str = f"{size / (1024 * 1024):.2f} MB"
            
            print(f"{str(relative_path):<50} {size_str:<15}")
    
    print("-" * 65)
    print(f"\nTotal: {file_count} arquivos, {total_size / 1024:.2f} KB")

def show_info():
    """Mostra informações sobre o sandbox"""
    print("\n" + "=" * 70)
    print("📍 INFORMAÇÕES DO SANDBOX")
    print("=" * 70)
    print(f"\n🗂️  Diretório: {SANDBOX_DIR}")
    print(f"📂 Diretório Atual: {os.getcwd()}")
    print(f"💻 Sistema: {os.uname().sysname} {os.uname().release}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # Espaço em disco
    stat = os.statvfs(SANDBOX_DIR)
    free_space = (stat.f_bavail * stat.f_frsize) / (1024 ** 3)
    total_space = (stat.f_blocks * stat.f_frsize) / (1024 ** 3)
    
    print(f"\n💾 Espaço em Disco:")
    print(f"   Total: {total_space:.2f} GB")
    print(f"   Livre: {free_space:.2f} GB")
    
    # Tamanho do projeto
    total_size = sum(f.stat().st_size for f in SANDBOX_DIR.rglob("*") if f.is_file())
    print(f"\n📦 Tamanho do Projeto: {total_size / (1024 ** 2):.2f} MB")
    
    print("\n" + "=" * 70)

def copy_file(source, destination):
    """Copia um arquivo para o destino especificado"""
    source_path = SANDBOX_DIR / source
    
    if not source_path.exists():
        print(f"❌ Erro: Arquivo '{source}' não encontrado!")
        return False
    
    try:
        dest_path = Path(destination)
        
        # Se o destino é um diretório, mantém o nome do arquivo
        if dest_path.is_dir():
            dest_path = dest_path / source_path.name
        
        shutil.copy2(source_path, dest_path)
        print(f"✅ Arquivo copiado com sucesso!")
        print(f"   De: {source_path}")
        print(f"   Para: {dest_path}")
        return True
    except Exception as e:
        print(f"❌ Erro ao copiar arquivo: {e}")
        return False

def create_zip(output_name):
    """Cria um arquivo ZIP do projeto"""
    if not output_name.endswith('.zip'):
        output_name += '.zip'
    
    output_path = SANDBOX_DIR / output_name
    
    print(f"\n📦 Criando arquivo ZIP: {output_name}")
    print("⏳ Aguarde...")
    
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            
            for item in SANDBOX_DIR.rglob("*"):
                if item.is_file():
                    # Ignorar .git e __pycache__
                    if ".git" in str(item) or "__pycache__" in str(item):
                        continue
                    
                    relative_path = item.relative_to(SANDBOX_DIR)
                    zipf.write(item, relative_path)
                    file_count += 1
                    
                    if file_count % 10 == 0:
                        print(f"   Processados: {file_count} arquivos...")
            
            print(f"\n✅ ZIP criado com sucesso!")
            print(f"   Arquivo: {output_path}")
            print(f"   Arquivos incluídos: {file_count}")
            print(f"   Tamanho: {output_path.stat().st_size / 1024:.2f} KB")
            return True
    except Exception as e:
        print(f"❌ Erro ao criar ZIP: {e}")
        return False

def show_help():
    """Mostra ajuda de uso"""
    print(__doc__)

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_files()
    elif command == "info":
        show_info()
    elif command == "copy":
        if len(sys.argv) < 4:
            print("❌ Uso: python download_cli.py copy <arquivo> <destino>")
        else:
            copy_file(sys.argv[2], sys.argv[3])
    elif command == "zip":
        if len(sys.argv) < 3:
            print("❌ Uso: python download_cli.py zip <nome_arquivo>")
        else:
            create_zip(sys.argv[2])
    elif command == "help":
        show_help()
    else:
        print(f"❌ Comando desconhecido: {command}")
        show_help()

if __name__ == "__main__":
    main()
