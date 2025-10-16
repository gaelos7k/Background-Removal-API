# 🚀 Guia de Migração - API V2.0

## O que mudou?

### ✅ Processamento em Memória
**Antes (V1.0)**:
- Imagens eram salvas em `temp_uploads/`
- Resultados eram salvos em `temp_results/`
- Necessário gerenciar limpeza de arquivos temporários

**Agora (V2.0)**:
- ✨ Tudo processado em memória
- ✨ Zero arquivos temporários
- ✨ Sem necessidade de gerenciar disco

### ✅ Performance Melhorada
**Antes (V1.0)**:
- Modelo carregado via subprocess a cada requisição
- ~5-10 segundos por requisição

**Agora (V2.0)**:
- ✨ Modelo carregado uma vez na inicialização
- ✨ Primeira requisição: ~2-3s
- ✨ Requisições subsequentes: ~0.5-1s

## Como testar?

### 1. Inicie o servidor
```powershell
cd backend
python main.py
```

Você verá:
```
Carregando modelo U2Net de C:\...\U-2-Net\saved_models\u2net\u2net.pth...
Modelo carregado na CPU
Modelo U2Net carregado com sucesso!
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 2. Teste com cURL (PowerShell)

**Download da imagem processada:**
```powershell
curl -X POST "http://127.0.0.1:8000/remover-fundo/?visualizar=false" `
  -F "file=@backend/temp_uploads/input.jpg" `
  --output resultado.png
```

**Visualização inline:**
```powershell
curl -X POST "http://127.0.0.1:8000/remover-fundo/?visualizar=true" `
  -F "file=@backend/temp_uploads/input.jpg" `
  --output resultado_inline.png
```

**JSON com base64:**
```powershell
curl -X POST "http://127.0.0.1:8000/processar-imagem/" `
  -F "file=@backend/temp_uploads/input.jpg" `
  -o resultado.json
```

### 3. Teste com Python
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
with open("resultado.png", "wb") as f:
    f.write(response.content)
```

### 4. Teste com o script de teste
```powershell
# Certifique-se de que há uma imagem em backend/temp_uploads/input.jpg
python test_api_v2.py
```

## Documentação da API

Acesse: http://127.0.0.1:8000/docs

### Endpoints Disponíveis

#### `GET /`
Retorna informações da API

#### `POST /remover-fundo/`
Remove fundo e retorna imagem PNG

**Parâmetros:**
- `file` (form-data): Arquivo de imagem
- `visualizar` (query, opcional): `true` para inline, `false` para download

**Retorna:** Imagem PNG com fundo removido

#### `POST /processar-imagem/`
Remove fundo e retorna JSON com base64

**Parâmetros:**
- `file` (form-data): Arquivo de imagem

**Retorna:** JSON com:
```json
{
  "status": "sucesso",
  "mensagem": "Fundo removido com sucesso!",
  "imagem_original": {
    "data": "data:image/jpeg;base64,...",
    "tamanho_bytes": 123456,
    "formato": "image/jpeg"
  },
  "imagem_processada": {
    "data": "data:image/png;base64,...",
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

## Vantagens da V2.0

### 🚀 Performance
- **10x mais rápido** nas requisições subsequentes
- Modelo carregado apenas uma vez
- Inferência direta com PyTorch

### 💾 Economia de Disco
- **0 bytes** de arquivos temporários
- Sem necessidade de limpeza periódica
- Sem risco de disco cheio

### 🔒 Segurança
- Não armazena dados dos usuários
- Processamento completamente efêmero
- Conformidade com LGPD/GDPR

### 🎯 Simplicidade
- API mais limpa e intuitiva
- Menos código para manter
- Menos pontos de falha

## Troubleshooting

### Modelo não carrega
```
ERRO: Modelo não encontrado em ...
```
**Solução:** Verifique se `U-2-Net/saved_models/u2net/u2net.pth` existe

### Erro de memória
```
RuntimeError: CUDA out of memory
```
**Solução:** O modelo está tentando usar GPU. Se não houver memória suficiente, ele automaticamente usa CPU.

### Porta ocupada
```
ERROR: Address already in use
```
**Solução:** 
```powershell
# Parar processos na porta 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## Próximos Passos

- [ ] Adicionar autenticação JWT
- [ ] Implementar cache de resultados
- [ ] Suporte a batch processing
- [ ] Métricas e monitoring
- [ ] Deploy com Docker

## Suporte

Em caso de problemas, abra uma issue no repositório ou entre em contato com a equipe de desenvolvimento.
