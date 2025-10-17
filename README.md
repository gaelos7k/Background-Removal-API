# 🎨 Bemasnap Background Removal API

> API REST para remoção automática de fundo de imagens usando inteligência artificial

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 💡 O que é?

Uma API gratuita e open source que remove automaticamente o fundo de qualquer imagem usando deep learning.

### ✨ Principais Vantagens

- ✅ **100% Gratuito** - Sem limites de uso
- ✅ **Privacidade Total** - Suas imagens não são armazenadas
- ✅ **Rápido** - Processa em menos de 1 segundo
- ✅ **Fácil de Usar** - Interface interativa em `/docs`
- ✅ **Alta Qualidade** - Usa modelo U²-Net de última geração

---

## 🚀 Instalação Rápida

### Pré-requisitos

- **Python 3.8 ou superior**
- **Git** com **Git LFS** instalado ([Download Git LFS](https://git-lfs.github.com/))
- **4GB+ de RAM**

> ⚠️ **IMPORTANTE**: Você precisa ter o Git LFS instalado ANTES de clonar o repositório, pois o modelo de IA é um arquivo grande.

### Passo a Passo

#### 1️⃣ Instale o Git LFS

**Windows:**
```powershell
# Baixe e instale: https://git-lfs.github.com/
git lfs install
```

**Linux:**
```bash
sudo apt-get install git-lfs
git lfs install
```

**Mac:**
```bash
brew install git-lfs
git lfs install
```

#### 2️⃣ Clone o Repositório

```bash
git clone https://github.com/G2J-Labs/bemasnap-backend-api.git
cd bemasnap-backend-api
```

#### 3️⃣ Configure o Ambiente

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4️⃣ Inicie o Servidor

```bash
cd backend
python main.py
```

Você verá algo assim:
```
Modelo U2Net carregado com sucesso!
INFO: Uvicorn running on http://127.0.0.1:8000
```

✅ **Pronto!** A API está rodando!

---

## 🎮 Como Usar

### Método Mais Fácil: Interface Interativa

1. **Abra seu navegador** em: http://127.0.0.1:8000/docs

2. **Escolha um endpoint:**
   - `/remover-fundo/` - Retorna a imagem processada em PNG
   - `/processar-imagem/` - Retorna JSON com a imagem em base64

3. **Clique em "Try it out"**

4. **Faça upload da sua imagem**

5. **Clique em "Execute"**

6. **Baixe o resultado!** 🎉

---

## 📡 Endpoints Disponíveis

### `POST /remover-fundo/`
Remove o fundo e retorna a imagem PNG pronta para download

**Parâmetros:**
- `file`: Sua imagem (JPEG, PNG, WebP, etc.)
- `visualizar`: `true` para visualizar no navegador, `false` para baixar (padrão: `false`)

**Retorno:** Imagem PNG com fundo transparente

---

### `POST /processar-imagem/`
Remove o fundo e retorna JSON com a imagem original e processada em base64

**Parâmetros:**
- `file`: Sua imagem

**Retorno:**
```json
{
  "status": "sucesso",
  "mensagem": "Fundo removido com sucesso!",
  "imagem_processada": {
    "data": "data:image/png;base64,iVBORw0KG...",
    "tamanho_bytes": 234567,
    "formato": "PNG"
  }
}
```

---

## 📁 Estrutura do Projeto

```
bemasnap-backend-api/
├── backend/                    # Código da API
│   ├── main.py                # 🚀 Inicia o servidor
│   └── app/
│       ├── presentation/      # Endpoints REST
│       ├── application/       # Lógica de negócio
│       └── infrastructure/    # Integração com IA
│
├── U-2-Net/                   # Modelo de IA
│   ├── model/
│   └── saved_models/
│       └── u2net/
│           └── u2net.pth     # Modelo (173MB)
│
└── requirements.txt           # Dependências
```

---

## ⚡ Performance

| Métrica | Valor |
|---------|-------|
| Primeira requisição | ~2-3s (carrega o modelo) |
| Requisições seguintes | ~0.5-1s |
| Uso de memória | ~800MB |
| Uso de disco | 0 bytes (tudo em memória) |

---

## 🔧 Problemas Comuns

### ❌ "Modelo não encontrado"
**Solução:** Certifique-se de ter instalado o Git LFS antes de clonar. Se já clonou sem LFS:
```bash
git lfs pull
```

### ❌ "Porta 8000 já está em uso"
**Solução (Windows):**
```powershell
# Encontre o processo
netstat -ano | findstr :8000
# Mate o processo (substitua <PID>)
taskkill /PID <PID> /F
```

**Solução (Linux/Mac):**
```bash
lsof -ti:8000 | xargs kill -9
```

### ❌ Erro de memória
**Solução:** O modelo usa CPU automaticamente se não houver GPU suficiente.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga estes passos:

1. Faça um fork do projeto
2. Crie uma branch: `git checkout -b minha-feature`
3. Commit suas mudanças: `git commit -m 'Adiciona nova feature'`
4. Push para a branch: `git push origin minha-feature`
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT - veja [LICENSE](LICENSE) para detalhes.

---

---

<p align="center">
  Feito com ❤️ por <a href="https://github.com/G2J-Labs">Gabriel</a>
</p>

<p align="center">
  <sub>Se este projeto te ajudou, considere dar uma ⭐!</sub>
</p>