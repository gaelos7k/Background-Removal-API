# 🎨 Background Removal API - U²-Net

Uma API REST profissional para remoção automática de fundo de imagens usando deep learning com arquitetura U²-Net, desenvolvida com FastAPI e seguindo os princípios de Clean Architecture.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Instalação](#-instalação)
- [Uso da API](#-uso-da-api)
- [Endpoints](#-endpoints)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Modelo U²-Net](#-modelo-u²-net)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

## 🎯 Visão Geral

Este sistema foi desenvolvido para auxiliar pequenos comerciantes e profissionais de marketing digital na criação de imagens mais atrativas, removendo automaticamente o fundo de fotografias de produtos usando inteligência artificial.

### Principais Benefícios

- ✅ **Processamento Automático**: Remoção de fundo sem intervenção manual
- ✅ **Alta Qualidade**: Utiliza o modelo U²-Net pré-treinado para resultados profissionais
- ✅ **API REST**: Integração fácil com aplicações web e mobile
- ✅ **Resposta Rápida**: Processamento otimizado para uso em produção
- ✅ **Múltiplos Formatos**: Suporte para diferentes tipos de resposta (download e base64)

## 🚀 Funcionalidades

### Core Features

- **Remoção de Fundo Inteligente**: Algoritmo U²-Net para segmentação precisa
- **Processamento Batch**: Suporte para múltiplas imagens
- **Preview em Tempo Real**: Visualização direta via base64
- **Download Direto**: Arquivo processado para download
- **API Documentada**: Interface Swagger/OpenAPI integrada
- **CORS Habilitado**: Suporte para aplicações web cross-origin

### Formatos Suportados

- **Entrada**: JPEG, PNG, WebP, BMP, TIFF
- **Saída**: PNG com transparência (RGBA)

## 🏗️ Arquitetura

O sistema segue os princípios de **Clean Architecture**, garantindo separação de responsabilidades e facilidade de manutenção:

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│                   (FastAPI Endpoints)                   │
├─────────────────────────────────────────────────────────┤
│                   Application Layer                     │
│              (Business Logic & Use Cases)               │
├─────────────────────────────────────────────────────────┤
│                   Infrastructure Layer                  │
│              (U²-Net Service & File I/O)               │
├─────────────────────────────────────────────────────────┤
│                     Domain Layer                        │
│                (Entities & Interfaces)                 │
└─────────────────────────────────────────────────────────┘
```

## 💻 Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e performático
- **Uvicorn** - Servidor ASGI de alta performance
- **PyTorch** - Framework de deep learning
- **Torchvision** - Processamento de imagens com PyTorch

### IA/ML
- **U²-Net** - Modelo de segmentação semântica
- **PIL (Pillow)** - Manipulação de imagens
- **NumPy** - Computação numérica
- **OpenCV** - Processamento avançado de imagens

### Utilitários
- **Python-multipart** - Upload de arquivos multipart
- **Base64** - Codificação de imagens para JSON
- **UUID** - Geração de identificadores únicos

## 📦 Instalação

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- 4GB+ RAM (recomendado para processamento de imagens)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone <repository-url>
cd life_changing
```

2. **Crie um ambiente virtual**
```bash
python -m venv .venv
```

3. **Ative o ambiente virtual**

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install fastapi uvicorn torch torchvision pillow numpy opencv-python python-multipart
```

5. **Execute o servidor**
```bash
cd backend
python main.py
```

O servidor estará disponível em: `http://127.0.0.1:8000`

## 🔌 Uso da API

### Interface Interativa

Acesse a documentação interativa da API em:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Autenticação

Esta API não requer autenticação (adequado para desenvolvimento e demonstrações).

## 📡 Endpoints

### 1. Health Check

```http
GET /health
```

**Resposta:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "device": "cpu"
}
```

### 2. Remoção de Fundo com Download

```http
POST /api/v1/remove-background/
Content-Type: multipart/form-data

file: <arquivo-imagem>
```

**Resposta:** Arquivo PNG com fundo removido para download direto.

### 3. Processamento com Preview JSON

```http
POST /api/v1/processar-imagem/
Content-Type: multipart/form-data

file: <arquivo-imagem>
```

**Resposta:**
```json
{
  "status": "sucesso",
  "mensagem": "Fundo removido com sucesso!",
  "imagem_original": {
    "data": "data:image/jpeg;base64,/9j/4AAQ...",
    "tamanho_bytes": 125840,
    "formato": "JPEG"
  },
  "imagem_processada": {
    "data": "data:image/png;base64,iVBORw0KGg...",
    "tamanho_bytes": 89632,
    "formato": "PNG",
    "transparencia": true
  },
  "info": {
    "algoritmo": "U²-Net",
    "processamento_concluido": true,
    "file_id": "123e4567-e89b-12d3-a456-426614174000",
    "download_url": "/api/v1/results/123e4567_processed.png"
  }
}
```

### 4. Recuperar Resultado

```http
GET /api/v1/results/{filename}
```

Retorna o arquivo processado pelo nome.

## 📁 Estrutura do Projeto

```
life_changing/
├── 📁 backend/
│   ├── 📄 main.py                 # Entry point do servidor
│   └── 📁 app/
│       ├── 📄 main.py            # Aplicação FastAPI principal
│       ├── 📁 domain/            # Entidades do domínio
│       │   └── 📄 entities.py
│       ├── 📁 application/       # Lógica de negócio
│       │   └── 📄 services.py
│       ├── 📁 infrastructure/    # Adaptadores externos
│       │   └── 📁 segmentation/
│       │       └── 📄 u2net_service.py
│       └── 📁 presentation/      # Camada de apresentação
│           └── 📄 api.py
├── 📁 U-2-Net/                   # Modelo U²-Net
│   ├── 📄 u2net_test.py         # Script de inferência
│   ├── 📁 model/                 # Arquitetura do modelo
│   └── 📄 data_loader.py        # Carregamento de dados
├── 📁 saved_models/              # Modelos pré-treinados
│   └── 📁 u2net/
│       └── 📄 u2net.pth         # Pesos do modelo (173.6MB)
├── 📁 temp_uploads/              # Arquivos temporários de entrada
├── 📁 temp_results/              # Resultados processados
└── 📄 README.md                  # Este arquivo
```

## 🧠 Modelo U²-Net

### Sobre o U²-Net

O **U²-Net (U Square Net)** é uma arquitetura de rede neural convolucional especializada em segmentação de imagens, desenvolvida especificamente para detecção de objetos salientes (salient object detection).

### Características Técnicas

- **Tamanho do Modelo**: 173.6 MB
- **Arquitetura**: Encoder-Decoder com conexões residuais
- **Resolução de Entrada**: 320x320 pixels
- **Normalização**: ImageNet (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- **Função de Ativação**: Sigmoid para saída de probabilidade

### Pipeline de Processamento

1. **Pré-processamento**: Redimensionamento e normalização
2. **Inferência**: Passagem pela rede U²-Net
3. **Pós-processamento**: Aplicação de sigmoid e redimensionamento
4. **Composição**: Aplicação da máscara à imagem original

## 💡 Exemplos de Uso

### Exemplo 1: Python Requests

```python
import requests

# Upload de imagem para processamento
url = "http://127.0.0.1:8000/api/v1/processar-imagem/"
files = {"file": open("produto.jpg", "rb")}

response = requests.post(url, files=files)
result = response.json()

print(f"Status: {result['status']}")
print(f"Tamanho original: {result['imagem_original']['tamanho_bytes']} bytes")
print(f"Tamanho processado: {result['imagem_processada']['tamanho_bytes']} bytes")
```

### Exemplo 2: cURL

```bash
# Download direto
curl -X POST "http://127.0.0.1:8000/api/v1/remove-background/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@produto.jpg" \
  --output produto_sem_fundo.png

# Processamento com JSON
curl -X POST "http://127.0.0.1:8000/api/v1/processar-imagem/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@produto.jpg"
```

### Exemplo 3: JavaScript (Frontend)

```javascript
// Upload com preview
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://127.0.0.1:8000/api/v1/processar-imagem/', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  // Exibir imagem original
  document.getElementById('original').src = data.imagem_original.data;
  
  // Exibir imagem processada
  document.getElementById('processed').src = data.imagem_processada.data;
});
```

## 🔧 Configurações Avançadas

### Variáveis de Ambiente

```bash
# Configurações do servidor
HOST=127.0.0.1
PORT=8000
WORKERS=1

# Configurações do modelo
MODEL_PATH=./saved_models/u2net/u2net.pth
DEVICE=cpu  # ou cuda para GPU

# Diretórios temporários
UPLOAD_DIR=./temp_uploads
RESULT_DIR=./temp_results
```

### Otimizações de Performance

1. **GPU**: Configure `DEVICE=cuda` se disponível
2. **Batch Processing**: Processe múltiplas imagens simultaneamente
3. **Caching**: Implemente cache para modelos frequentemente usados
4. **Compressão**: Use compressão de imagens para reduzir bandwidth

## 🚀 Deploy em Produção

### Docker (Recomendado)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "backend/main.py"]
```

### Considerações de Produção

- Use um servidor proxy reverso (Nginx)
- Configure monitoramento e logs
- Implemente rate limiting
- Use HTTPS em produção
- Configure backup para modelos

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Créditos

- **U²-Net Model**: Baseado no trabalho de Qin et al. ([Paper](https://arxiv.org/abs/2005.09007))
- **FastAPI**: Framework web moderno para Python
- **PyTorch**: Framework de deep learning

---

**Desenvolvido com ❤️ para auxiliar pequenos comerciantes no marketing digital**

Para dúvidas ou suporte, abra uma [issue](../../issues) no GitHub.