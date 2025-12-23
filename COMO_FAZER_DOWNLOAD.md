# 📥 Como Fazer Download de Arquivos do /vercel/sandbox

## 🎯 Resposta Rápida

O diretório `/vercel/sandbox` é o **diretório raiz do seu projeto** neste ambiente sandbox Linux.

**Localização**: `/vercel/sandbox` (caminho absoluto)

---

## 🔧 Métodos para Fazer Download

### ✅ Método 1: Via API Web (Mais Fácil)

Adicionei endpoints de download na sua aplicação FastAPI:

#### 1️⃣ Iniciar o servidor:
```bash
python main.py
```

#### 2️⃣ Acessar no navegador:
- **Login**: http://127.0.0.1:8001/
  - Usuário: `admin`
  - Senha: `admin123`

#### 3️⃣ Endpoints disponíveis:

| URL | Descrição |
|-----|-----------|
| `http://127.0.0.1:8001/files` | Lista todos os arquivos (JSON) |
| `http://127.0.0.1:8001/download/config` | Download do config.json |
| `http://127.0.0.1:8001/download/logs` | Download dos logs |
| `http://127.0.0.1:8001/download/file?path=main.py` | Download de qualquer arquivo |

#### Exemplo de uso:
```bash
# Listar arquivos
curl -b "logged_in=true" http://127.0.0.1:8001/files

# Download de arquivo específico
curl -b "logged_in=true" http://127.0.0.1:8001/download/file?path=main.py -o main.py
```

---

### ✅ Método 2: Via CLI Tool (Linha de Comando)

Criei uma ferramenta CLI para facilitar:

```bash
# Ver informações do sandbox
python download_cli.py info

# Listar todos os arquivos
python download_cli.py list

# Copiar arquivo para outro local
python download_cli.py copy main.py /tmp/main.py

# Criar ZIP de todo o projeto
python download_cli.py zip meu_projeto

# Ver ajuda
python download_cli.py help
```

---

### ✅ Método 3: Comandos Linux Diretos

```bash
# Ver onde você está
pwd
# Resultado: /vercel/sandbox

# Listar arquivos
ls -la

# Ver conteúdo de arquivo
cat main.py

# Copiar arquivo
cp main.py /tmp/backup_main.py

# Criar arquivo ZIP
zip -r projeto.zip . -x "*.git*" -x "*__pycache__*"

# Criar arquivo TAR.GZ
tar -czf projeto.tar.gz --exclude='.git' --exclude='__pycache__' .

# Encontrar todos os arquivos Python
find /vercel/sandbox -name "*.py"
```

---

### ✅ Método 4: Via Python Script

```python
import shutil
from pathlib import Path

# Copiar arquivo
shutil.copy('/vercel/sandbox/main.py', '/tmp/main.py')

# Copiar diretório inteiro
shutil.copytree('/vercel/sandbox', '/tmp/meu_projeto')

# Ler arquivo
with open('/vercel/sandbox/main.py', 'r') as f:
    conteudo = f.read()
    print(conteudo)
```

---

## 📊 Estrutura do Projeto

```
/vercel/sandbox/
├── 📄 main.py                    # Aplicação FastAPI principal
├── 📄 Procfile                   # Config de deploy
├── 📄 requirements.txt           # Dependências Python
├── 📄 download_helper.py         # Helper para downloads
├── 📄 download_cli.py            # CLI tool para downloads
├── 📄 SANDBOX_INFO.md            # Informações detalhadas
├── 📄 COMO_FAZER_DOWNLOAD.md     # Este arquivo
│
├── 📁 blaze_bot/
│   ├── blaze_client.py           # Cliente do bot
│   ├── config.json               # Configurações
│   └── __pycache__/
│
├── 📁 static/
│   └── css/
│       └── style.css
│
└── 📁 templates/
    ├── dashboard.html
    ├── login.html
    ├── logs.html
    └── settings.html
```

---

## 🚀 Exemplos Práticos

### Exemplo 1: Baixar arquivo de configuração
```bash
# Via CLI
python download_cli.py copy blaze_bot/config.json /tmp/config.json

# Via curl (com servidor rodando)
curl -b "logged_in=true" http://127.0.0.1:8001/download/config -o config.json
```

### Exemplo 2: Criar backup completo
```bash
# Criar ZIP
python download_cli.py zip backup_projeto

# Ou manualmente
zip -r backup.zip . -x "*.git*" -x "*__pycache__*"
```

### Exemplo 3: Copiar projeto para /tmp
```bash
# Copiar tudo
cp -r /vercel/sandbox /tmp/meu_projeto

# Verificar
ls -la /tmp/meu_projeto
```

---

## 💡 Informações Importantes

### 📍 Localização
- **Caminho Absoluto**: `/vercel/sandbox`
- **Sistema**: Amazon Linux 2023
- **Python**: 3.9.25
- **Espaço Livre**: ~26 GB

### ⚠️ Avisos
1. Este é um ambiente **temporário**
2. Arquivos podem ser perdidos ao reiniciar
3. Sempre faça backup de dados importantes
4. Use caminhos absolutos quando possível

### 🔐 Segurança
- Todos os endpoints de download requerem autenticação
- Credenciais padrão: `admin` / `admin123`
- Arquivos fora do sandbox são bloqueados

---

## 🆘 Solução de Problemas

### Problema: "Arquivo não encontrado"
```bash
# Verificar se o arquivo existe
ls -la /vercel/sandbox/main.py

# Ver diretório atual
pwd
```

### Problema: "Permissão negada"
```bash
# Dar permissão de execução
chmod +x download_cli.py

# Verificar permissões
ls -la
```

### Problema: "Servidor não inicia"
```bash
# Instalar dependências
pip install -r requirements.txt

# Verificar porta
netstat -tuln | grep 8001

# Iniciar em porta diferente
uvicorn main:app --host 127.0.0.1 --port 8002
```

---

## 📚 Recursos Adicionais

### Scripts Criados
1. **download_helper.py** - Funções auxiliares para downloads
2. **download_cli.py** - Ferramenta CLI completa
3. **SANDBOX_INFO.md** - Documentação detalhada

### Endpoints API
- `/files` - Lista arquivos
- `/download/config` - Download config
- `/download/logs` - Download logs
- `/download/file?path=X` - Download qualquer arquivo

---

## 📞 Comandos Úteis

```bash
# Ver informações do sistema
uname -a

# Espaço em disco
df -h

# Tamanho do projeto
du -sh /vercel/sandbox

# Processos rodando
ps aux | grep python

# Variáveis de ambiente
env | grep -i path

# Histórico de comandos
history
```

---

## ✅ Checklist de Download

- [ ] Identifiquei o arquivo que preciso
- [ ] Escolhi o método de download (API, CLI, ou comando direto)
- [ ] Testei se o arquivo existe (`ls -la`)
- [ ] Fiz o download/cópia
- [ ] Verifiquei o arquivo no destino
- [ ] Criei backup se necessário

---

**🎉 Pronto! Agora você sabe exatamente onde fica o `/vercel/sandbox` e como fazer download dos arquivos!**

Para mais informações, consulte:
- `SANDBOX_INFO.md` - Informações detalhadas
- `python download_cli.py help` - Ajuda da CLI
- `python download_helper.py` - Ver estrutura de arquivos
