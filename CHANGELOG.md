# Changelog - Bemasnap Backend API

## [2.0.0] - 2025-10-16

### 🎉 Mudanças Importantes

#### Processamento em Memória
- **Removido**: Salvamento de arquivos locais (temp_uploads/ e temp_results/)
- **Novo**: Processamento completo em memória usando BytesIO
- **Benefício**: Não cria arquivos temporários, economia de espaço em disco

#### Carregamento do Modelo U2Net
- **Otimizado**: Modelo é carregado uma única vez na inicialização
- **Antes**: Modelo era carregado via subprocess a cada requisição
- **Agora**: Inferência direta usando PyTorch em memória
- **Benefício**: ~10x mais rápido nas requisições subsequentes

### ✨ Novas Features

#### API Endpoints
- `GET /` - Informações da API
- `POST /remover-fundo/` - Remove fundo e retorna PNG (download ou visualização inline)
- `POST /processar-imagem/` - Remove fundo e retorna JSON com imagens em base64

### 🔧 Mudanças Técnicas

#### U2NetService
- Carrega modelo PyTorch diretamente (sem subprocess)
- Processa imagens em memória (PIL + NumPy + Torch)
- Retorna BytesIO ao invés de salvar arquivos
- Suporta GPU automático (se disponível)

#### RemocaoFundoService
- Interface simplificada: `remover_fundo(bytes) -> BytesIO`
- Remove dependência de caminhos de arquivo

#### API (presentation/api.py)
- Usa `StreamingResponse` para retornar imagens
- Remove dependência de FileResponse e arquivos temporários
- Suporte a visualização inline e download
- Endpoint JSON com base64 para integração web

### 📊 Performance

- **Primeira requisição**: ~2-3s (carregamento do modelo)
- **Requisições subsequentes**: ~0.5-1s (apenas inferência)
- **Memória**: ~800MB (modelo carregado)
- **Disco**: 0 bytes (sem arquivos temporários)

### 🚀 Como Usar

```bash
# Iniciar servidor
cd backend
python main.py

# Testar endpoint
curl -X POST "http://127.0.0.1:8000/remover-fundo/?visualizar=false" \
  -F "file=@imagem.jpg" \
  --output resultado.png

# Ver documentação
http://127.0.0.1:8000/docs
```

### 🐛 Bug Fixes

- Corrigido caminho do modelo U2Net (agora busca em U-2-Net/saved_models/)
- Adicionado parser de argumentos em u2net_test.py (mantido para compatibilidade)
- Removido código duplicado e dependências desnecessárias

### ⚠️ Breaking Changes

- **Entidade `Imagem`**: Não é mais usada nos serviços
- **Paths de arquivo**: Removidos dos métodos de serviço
- **Temp directories**: Não são mais criados automaticamente

### 🔜 Próximos Passos

- [ ] Cache de resultados (Redis)
- [ ] Suporte a batch processing
- [ ] Métricas e logging estruturado
- [ ] Docker containerization
- [ ] Health check endpoints
