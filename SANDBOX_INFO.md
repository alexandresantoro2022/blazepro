# Informações do Diretório /vercel/sandbox

## 📍 Localização

- **Caminho Absoluto**: `/vercel/sandbox`
- **Sistema Operacional**: Amazon Linux 2023
- **Ambiente**: Sandbox com Node.js 22 e Python
- **Gerenciador de Pacotes**: dnf (para sistema) e pip (para Python)

## 📂 Estrutura do Projeto

```
/vercel/sandbox/
├── main.py                 # Aplicação FastAPI principal
├── Procfile               # Configuração de deploy
├── README.md              # Documentação do projeto
├── requirements.txt       # Dependências Python
├── download_helper.py     # Script auxiliar para downloads
├── SANDBOX_INFO.md        # Este arquivo
├── .git/                  # Repositório Git
├── blaze_bot/
│   ├── blaze_client.py    # Cliente do bot
│   ├── config.json        # Configurações do bot
│   └── __pycache__/
├── static/
│   └── css/
│       └── style.css      # Estilos CSS
└── templates/
    ├── dashboard.html     # Dashboard principal
    ├── login.html         # Página de login
    ├── logs.html          # Página de logs
    └── settings.html      # Página de configurações
```

## 🔗 Como Acessar Arquivos para Download

### Método 1: Via API FastAPI (Recomendado)

Após iniciar a aplicação, você pode acessar os seguintes endpoints:

1. **Listar todos os arquivos**:
   ```
   GET http://127.0.0.1:8001/files
   ```
   Retorna JSON com lista de todos os arquivos e seus URLs de download

2. **Download do arquivo de configuração**:
   ```
   GET http://127.0.0.1:8001/download/config
   ```

3. **Download dos logs**:
   ```
   GET http://127.0.0.1:8001/download/logs
   ```

4. **Download de qualquer arquivo**:
   ```
   GET http://127.0.0.1:8001/download/file?path=caminho/do/arquivo
   ```
   Exemplo: `http://127.0.0.1:8001/download/file?path=main.py`

### Método 2: Via Linha de Comando

Se você tem acesso ao terminal:

```bash
# Navegar para o diretório
cd /vercel/sandbox

# Listar arquivos
ls -la

# Ver conteúdo de um arquivo
cat main.py

# Copiar arquivo para outro local
cp main.py /tmp/main.py

# Criar arquivo zip de todo o projeto
zip -r projeto.zip . -x "*.git*" -x "*__pycache__*"
```

### Método 3: Via Python Script

```python
import os
from pathlib import Path

# Caminho do sandbox
SANDBOX = Path("/vercel/sandbox")

# Listar todos os arquivos
for file in SANDBOX.rglob("*"):
    if file.is_file():
        print(f"Arquivo: {file}")
        print(f"Tamanho: {file.stat().st_size} bytes")
```

## 🚀 Como Iniciar a Aplicação

```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar o servidor
python main.py

# Ou usando uvicorn diretamente
uvicorn main:app --host 127.0.0.1 --port 8001
```

## 📥 Endpoints de Download Disponíveis

| Endpoint | Descrição | Autenticação |
|----------|-----------|--------------|
| `/files` | Lista todos os arquivos do projeto | Sim |
| `/download/config` | Download do config.json | Sim |
| `/download/logs` | Download dos logs do bot | Sim |
| `/download/file?path=X` | Download de qualquer arquivo | Sim |

## 🔐 Credenciais de Acesso

- **Usuário**: admin
- **Senha**: admin123

## 💡 Dicas Importantes

1. **Segurança**: Todos os endpoints de download requerem autenticação
2. **Caminhos Relativos**: Use caminhos relativos ao `/vercel/sandbox` nos downloads
3. **Arquivos Grandes**: Para arquivos grandes, considere usar streaming
4. **Git**: O diretório `.git` é ignorado nas listagens de arquivos

## 🛠️ Comandos Úteis

```bash
# Ver o diretório atual
pwd

# Espaço em disco
df -h

# Tamanho do projeto
du -sh /vercel/sandbox

# Encontrar arquivos Python
find /vercel/sandbox -name "*.py"

# Criar backup
tar -czf backup.tar.gz /vercel/sandbox
```

## 📝 Notas

- Este é um ambiente sandbox temporário
- Arquivos podem ser perdidos ao reiniciar o ambiente
- Sempre faça backup de arquivos importantes
- Use os endpoints de download para extrair arquivos do sandbox
