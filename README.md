# 🎨 Bemasnap Background Removal API

> API REST de alta performance para remoção automática de fundo de imagens usando deep learning com U²-Net

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Características](#-características)
- [Tecnologias](#-tecnologias)
- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Endpoints da API](#-endpoints-da-api)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Performance](#-performance)
- [Deploy](#-deploy)
- [Testes](#-testes)
- [Troubleshooting](#-troubleshooting)
- [Contribuindo](#-contribuindo)

---

## 🎯 Sobre o Projeto

O **Bemasnap Background Removal API** é uma solução profissional para remoção automática de fundo de imagens, desenvolvida para auxiliar pequenos comerciantes, profissionais de marketing digital e e-commerces na criação de imagens mais atrativas.

### 💡 Problema que Resolve

- ❌ Ferramentas pagas caras (ex: remove.bg)
- ❌ Necessidade de edição manual em Photoshop
- ❌ Processamento lento
- ❌ Necessidade de upload para serviços de terceiros

### ✅ Nossa Solução

- ✅ **100% Gratuito e Open Source**
- ✅ **Processamento em Memória** - Sem salvar arquivos temporários
- ✅ **Alta Performance** - ~0.5-1s por imagem após carregamento do modelo
- ✅ **Privacidade Total** - Imagens não são armazenadas
- ✅ **Fácil Integração** - API REST com documentação Swagger
- ✅ **Deploy Simples** - Pronto para produção

---

## 🚀 Características

### Core Features

| Funcionalidade | Descrição |
|----------------|-----------|
| 🎯 **Remoção Inteligente** | Usa modelo U²-Net pré-treinado para segmentação precisa |
| ⚡ **Processamento em Memória** | Zero arquivos temporários, tudo em RAM |
| 🔄 **Múltiplos Formatos de Saída** | PNG com transparência, JSON com base64 |
| 📦 **Batch Ready** | Preparado para processar múltiplas imagens |
| 🌐 **CORS Habilitado** | Integração fácil com frontends web |
| 📊 **Documentação Automática** | Swagger UI integrado em `/docs` |

### Formatos Suportados

**Entrada**: JPEG, PNG, WebP, BMP, TIFF  
**Saída**: PNG com canal alfa (transparência)

---

## 💻 Tecnologias

### Backend

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e performático
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI de alta performance
- **[PyTorch](https://pytorch.org/)** - Framework de deep learning
- **[Torchvision](https://pytorch.org/vision/)** - Processamento de imagens

### IA/ML

- **U²-Net** - Modelo de segmentação semântica de última geração
- **PIL (Pillow)** - Manipulação de imagens
- **NumPy** - Computação numérica eficiente

### Arquitetura

- **Clean Architecture** - Separação clara de responsabilidades
- **Domain-Driven Design** - Foco no domínio do negócio
- **Dependency Injection** - Baixo acoplamento

---

## 🏗️ Arquitetura

O sistema segue os princípios de **Clean Architecture**, garantindo:
- ✅ Separação de responsabilidades
- ✅ Testabilidade
- ✅ Manutenibilidade
- ✅ Independência de frameworks

```
┌──────────────────────────────────────────────────────────────┐
│                     Presentation Layer                        │
│                    (FastAPI Endpoints)                        │
│  └─ api.py: Endpoints REST, validação de entrada, respostas │
├──────────────────────────────────────────────────────────────┤
│                    Application Layer                          │
│              (Business Logic & Orchestration)                 │
│  └─ services.py: Orquestração do fluxo de negócio           │
├──────────────────────────────────────────────────────────────┤
│                   Infrastructure Layer                        │
│              (External Services & I/O)                        │
│  └─ u2net_service.py: Integração com modelo U²-Net          │
├──────────────────────────────────────────────────────────────┤
│                      Domain Layer                             │
│                 (Core Business Logic)                         │
│  └─ Entidades e interfaces de domínio                       │
└──────────────────────────────────────────────────────────────┘
```

### Fluxo de Processamento

```
1. Cliente envia imagem via POST
         ↓
2. API (Presentation) recebe e valida
         ↓
3. Service (Application) orquestra processamento
         ↓
4. U2NetService (Infrastructure) processa com IA
         ↓
5. Resultado retorna como PNG ou JSON
         ↓
6. Cliente recebe imagem sem fundo
```

---

## 📦 Instalação

### Pré-requisitos

- **Python 3.8+** (recomendado: 3.10 ou 3.11)
- **pip** (gerenciador de pacotes)
- **4GB+ RAM** (8GB recomendado para melhor performance)
- **Git** (para clonar o repositório)

### Passo a Passo

#### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/G2J-Labs/bemasnap-backend-api.git
cd bemasnap-backend-api
```

#### 2️⃣ Crie um Ambiente Virtual (Recomendado)

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Instale as Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4️⃣ Verifique o Modelo U²-Net

O modelo deve estar em: `U-2-Net/saved_models/u2net/u2net.pth` (173.6 MB)

Se não estiver presente, baixe de: [U²-Net Model](https://drive.google.com/file/d/1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ/view)

#### 5️⃣ Inicie o Servidor

```bash
cd backend
python main.py
```

Você verá:
```
Carregando modelo U2Net de C:\...\U-2-Net\saved_models\u2net\u2net.pth...
Modelo carregado na CPU
Modelo U2Net carregado com sucesso!
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

#### 6️⃣ Acesse a Documentação

Abra seu navegador em: **http://127.0.0.1:8000/docs**

---

## 🎮 Como Usar

### 1. Via Documentação Interativa (Swagger)

1. Acesse: http://127.0.0.1:8000/docs
2. Clique em qualquer endpoint
3. Clique em "Try it out"
4. Faça upload da imagem
5. Clique em "Execute"
6. Veja o resultado!

### 2. Via cURL (Terminal)

**Download da imagem processada:**
```bash
curl -X POST "http://127.0.0.1:8000/remover-fundo/?visualizar=false" \
  -F "file=@sua_imagem.jpg" \
  --output resultado.png
```

**Visualização inline:**
```bash
curl -X POST "http://127.0.0.1:8000/remover-fundo/?visualizar=true" \
  -F "file=@sua_imagem.jpg" \
  --output resultado.png
```

**JSON com base64:**
```bash
curl -X POST "http://127.0.0.1:8000/processar-imagem/" \
  -F "file=@sua_imagem.jpg" \
  -o resultado.json
```

### 3. Via Python

```python
import requests

# Enviar imagem
with open("sua_imagem.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://127.0.0.1:8000/remover-fundo/",
        files=files,
        params={"visualizar": False}
    )

# Salvar resultado
if response.status_code == 200:
    with open("resultado.png", "wb") as f:
        f.write(response.content)
    print("✅ Imagem processada com sucesso!")
else:
    print(f"❌ Erro: {response.json()}")
```

### 4. Via JavaScript (Frontend)

```javascript
async function removerFundo(arquivo) {
    const formData = new FormData();
    formData.append('file', arquivo);
    
    try {
        const response = await fetch('http://127.0.0.1:8000/remover-fundo/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            
            // Exibir ou baixar a imagem
            const img = document.getElementById('resultado');
            img.src = url;
        } else {
            console.error('Erro ao processar imagem');
        }
    } catch (error) {
        console.error('Erro:', error);
    }
}
```

---

## 📡 Endpoints da API

### `GET /`
Informações sobre a API

**Resposta:**
```json
{
  "nome": "Bemasnap Background Removal API",
  "versao": "2.0.0",
  "descricao": "API para remoção de fundo de imagens usando U²-Net",
  "endpoints": {
    "/remover-fundo/": "Remove fundo e retorna imagem PNG",
    "/processar-imagem/": "Remove fundo e retorna JSON com base64",
    "/docs": "Documentação interativa da API"
  }
}
```

---

### `POST /remover-fundo/`
Remove o fundo e retorna a imagem processada

**Parâmetros:**
- `file` (multipart/form-data): Arquivo de imagem **[OBRIGATÓRIO]**
- `visualizar` (query): `true` para inline, `false` para download (padrão: `false`)

**Resposta:**
- Content-Type: `image/png`
- Body: Imagem PNG com fundo transparente

**Exemplo com cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/remover-fundo/?visualizar=false" \
  -F "file=@produto.jpg" \
  -o produto_sem_fundo.png
```

---

### `POST /processar-imagem/`
Remove o fundo e retorna JSON com imagens em base64

**Parâmetros:**
- `file` (multipart/form-data): Arquivo de imagem **[OBRIGATÓRIO]**

**Resposta:**
```json
{
  "status": "sucesso",
  "mensagem": "Fundo removido com sucesso!",
  "imagem_original": {
    "data": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
    "tamanho_bytes": 123456,
    "formato": "image/jpeg"
  },
  "imagem_processada": {
    "data": "data:image/png;base64,iVBORw0KGgo...",
    "tamanho_bytes": 234567,
    "formato": "PNG",
    "transparencia": true
  },
  "info": {
    "algoritmo": "U²-Net",
    "processamento_concluido": true,
    "economia_armazenamento": "Nenhum arquivo salvo localmente"
  }
}
```

**Casos de Erro:**
```json
{
  "status": "erro",
  "mensagem": "Descrição do erro"
}
```

---

## 📁 Estrutura do Projeto

```
bemasnap-backend-api/
├── backend/                          # Backend da aplicação
│   ├── __init__.py
│   ├── main.py                      # ⭐ Entry point da aplicação
│   └── app/
│       ├── __init__.py
│       ├── application/             # Camada de aplicação
│       │   ├── __init__.py
│       │   └── services.py          # Serviços de orquestração
│       ├── infrastructure/          # Camada de infraestrutura
│       │   ├── __init__.py
│       │   └── segmentation/
│       │       ├── __init__.py
│       │       └── u2net_service.py # ⭐ Serviço U²-Net
│       └── presentation/            # Camada de apresentação
│           ├── __init__.py
│           └── api.py               # ⭐ Endpoints FastAPI
│
├── U-2-Net/                         # Modelo U²-Net
│   ├── data_loader.py              # Carregamento de dados
│   ├── u2net_test.py               # Script de teste
│   ├── model/
│   │   ├── __init__.py
│   │   └── u2net.py                # ⭐ Arquitetura do modelo
│   └── saved_models/
│       └── u2net/
│           └── u2net.pth           # ⭐ Pesos do modelo (173.6 MB)
│
├── requirements.txt                 # ⭐ Dependências Python
├── README.md                        # ⭐ Este arquivo
├── test_api_v2.py                  # Script de testes
└── .gitignore                       # Arquivos ignorados pelo Git
```

### Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `backend/main.py` | Entry point que inicia o servidor Uvicorn |
| `backend/app/presentation/api.py` | Define os endpoints REST da API |
| `backend/app/application/services.py` | Orquestra a lógica de negócio |
| `backend/app/infrastructure/segmentation/u2net_service.py` | Integra com o modelo U²-Net |
| `U-2-Net/model/u2net.py` | Arquitetura neural do modelo |
| `U-2-Net/saved_models/u2net/u2net.pth` | Pesos pré-treinados do modelo |

---

## ⚡ Performance

### Métricas

| Métrica | Valor |
|---------|-------|
| **Primeira Requisição** | ~2-3s (inclui carregamento do modelo) |
| **Requisições Subsequentes** | ~0.5-1s (apenas inferência) |
| **Uso de Memória** | ~800MB (modelo em RAM) |
| **Uso de Disco** | 0 bytes (sem arquivos temporários) |
| **Throughput** | ~1-2 imagens/segundo (CPU) |

### Otimizações Implementadas

✅ **Carregamento Único do Modelo** - Modelo carregado apenas uma vez na inicialização  
✅ **Processamento em Memória** - Zero I/O de disco durante processamento  
✅ **Inferência Direta** - Sem subprocess ou chamadas externas  
✅ **Normalização Otimizada** - Processamento vetorizado com NumPy  

### Comparação com Versão Anterior

| Versão | Tempo/Imagem | Uso de Disco | Escalabilidade |
|--------|--------------|--------------|----------------|
| V1.0 | ~5-10s | Alto | Baixa |
| **V2.0** | **~0.5-1s** | **Zero** | **Alta** |

**Ganho de Performance: ~10x mais rápido!** 🚀

---

## 🌐 Deploy

### Opção 1: Deploy Local/VPS

#### 1. Preparar o Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.10
sudo apt install python3.10 python3.10-venv python3-pip -y
```

#### 2. Configurar a Aplicação

```bash
# Clonar repositório
git clone https://github.com/G2J-Labs/bemasnap-backend-api.git
cd bemasnap-backend-api

# Criar ambiente virtual
python3.10 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Configurar para Produção

Edite `backend/main.py`:

```python
if __name__ == "__main__":
    uvicorn.run(
        "app.presentation.api:app",
        host="0.0.0.0",  # Permite conexões externas
        port=8000,
        reload=False,    # Desabilitar reload em produção
        workers=2        # Múltiplos workers
    )
```

#### 4. Usar Systemd (Autostart)

Crie `/etc/systemd/system/bemasnap.service`:

```ini
[Unit]
Description=Bemasnap Background Removal API
After=network.target

[Service]
Type=simple
User=seu_usuario
WorkingDirectory=/caminho/para/bemasnap-backend-api/backend
Environment="PATH=/caminho/para/venv/bin"
ExecStart=/caminho/para/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Ativar:
```bash
sudo systemctl daemon-reload
sudo systemctl enable bemasnap
sudo systemctl start bemasnap
sudo systemctl status bemasnap
```

#### 5. Configurar Nginx (Proxy Reverso)

```nginx
server {
    listen 80;
    server_name seu_dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Timeout para uploads grandes
        client_max_body_size 50M;
        proxy_read_timeout 300s;
    }
}
```

---

### Opção 2: Deploy com Docker

#### 1. Criar Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY backend/ ./backend/
COPY U-2-Net/ ./U-2-Net/

WORKDIR /app/backend

EXPOSE 8000

CMD ["python", "main.py"]
```

#### 2. Criar docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./U-2-Net/saved_models:/app/U-2-Net/saved_models
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

#### 3. Build e Run

```bash
docker-compose build
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

---

### Opção 3: Deploy na Nuvem

#### AWS EC2

1. **Lançar EC2 (t2.medium ou maior)**
2. **Seguir passos de Deploy Local/VPS**
3. **Configurar Security Group** (porta 8000 aberta)
4. **Opcional: Configurar Load Balancer**

#### Google Cloud Run

```bash
# Build container
gcloud builds submit --tag gcr.io/seu-projeto/bemasnap-api

# Deploy
gcloud run deploy bemasnap-api \
  --image gcr.io/seu-projeto/bemasnap-api \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --timeout 300s \
  --allow-unauthenticated
```

#### Heroku

```bash
heroku create bemasnap-api
git push heroku main
heroku ps:scale web=1
heroku logs --tail
```

---

## 🧪 Testes

### Teste Manual (Script)

```bash
# Certifique-se de ter uma imagem de teste
python test_api_v2.py
```

Saída esperada:
```
🚀 TESTE DA API DE REMOÇÃO DE FUNDO (V2.0)
============================================================

🧪 Testando endpoint raiz...
Status: 200
✅ Resposta: {"nome": "Bemasnap Background Removal API", ...}

🧪 Testando /remover-fundo/ (download)...
Status: 200
✅ Imagem salva em: teste_resultado_download.png
Tamanho: 234567 bytes

🧪 Testando performance (3 requisições)...
  Requisição 1: ✅ 2.34s
  Requisição 2: ✅ 0.67s
  Requisição 3: ✅ 0.59s

📊 Tempo médio: 1.20s
📊 Primeira requisição: 2.34s (com carregamento do modelo)
📊 Requisições subsequentes: 0.63s (apenas inferência)

============================================================
🎯 5/5 testes passaram
🎉 Todos os testes passaram com sucesso!
```

### Teste com Pytest (Desenvolvimento)

```bash
# Instalar pytest
pip install pytest pytest-asyncio httpx

# Criar tests/test_api.py
# ... (código de testes)

# Executar testes
pytest tests/ -v
```

---

## 🔧 Troubleshooting

### Problema: Modelo não carrega

**Sintoma:**
```
ERRO: Modelo não encontrado em ...
```

**Solução:**
1. Verifique se `U-2-Net/saved_models/u2net/u2net.pth` existe
2. O arquivo deve ter ~173.6 MB
3. Se não existir, baixe de: [U²-Net Model](https://drive.google.com/file/d/1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ/view)

---

### Problema: Erro de memória

**Sintoma:**
```
RuntimeError: CUDA out of memory
```

**Solução:**
- O modelo automaticamente usa CPU se GPU não tiver memória
- Para forçar CPU, edite `u2net_service.py`:
```python
device = torch.device("cpu")  # Sempre usar CPU
```

---

### Problema: Porta ocupada

**Sintoma:**
```
ERROR: Address already in use
```

**Solução (Windows):**
```powershell
# Encontrar processo na porta 8000
netstat -ano | findstr :8000

# Matar processo (substitua PID)
taskkill /PID <PID> /F
```

**Solução (Linux/Mac):**
```bash
# Encontrar e matar processo
lsof -ti:8000 | xargs kill -9
```

---

### Problema: ImportError do modelo

**Sintoma:**
```
ImportError: cannot import name 'U2NET' from 'model'
```

**Solução:**
1. Verifique se `U-2-Net/model/u2net.py` existe
2. Verifique se `U-2-Net/model/__init__.py` existe
3. Reinicie o servidor

---

### Problema: Imagem muito grande

**Sintoma:**
```
Request Entity Too Large
```

**Solução:**
Configure o limite no servidor (Nginx/Apache) ou ajuste o FastAPI:
```python
# Em api.py
from fastapi import FastAPI, File, UploadFile
from fastapi.exceptions import RequestValidationError

# Aumentar limite (exemplo: 50MB)
app = FastAPI(max_request_size=50 * 1024 * 1024)
```

---

## 📚 Recursos Adicionais

### Documentação Técnica

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [U²-Net Paper](https://arxiv.org/abs/2005.09007)

### Artigos Relacionados

- [Background Removal with Deep Learning](https://towardsdatascience.com/)
- [Deploying ML Models with FastAPI](https://testdriven.io/blog/fastapi-machine-learning/)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga estes passos:

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### Guidelines

- Mantenha o código limpo e documentado
- Adicione testes para novas features
- Atualize a documentação quando necessário
- Siga os padrões de código do projeto

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👥 Autores

**G2J Labs**
- GitHub: [@G2J-Labs](https://github.com/G2J-Labs)

---

## 🙏 Agradecimentos

- [U²-Net](https://github.com/xuebinqin/U-2-Net) - Modelo de segmentação
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web
- [PyTorch](https://pytorch.org/) - Framework de deep learning
- Comunidade open source

---

## 📞 Suporte

Encontrou um bug? Tem uma sugestão?

- 🐛 [Abra uma issue](https://github.com/G2J-Labs/bemasnap-backend-api/issues)
- 💬 [Discussões](https://github.com/G2J-Labs/bemasnap-backend-api/discussions)
- 📧 Email: suporte@g2jlabs.com

---

<p align="center">
  Feito com ❤️ por <a href="https://github.com/G2J-Labs">G2J Labs</a>
</p>

<p align="center">
  <sub>Se este projeto te ajudou, considere dar uma ⭐ no repositório!</sub>
</p>
