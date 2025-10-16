from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import StreamingResponse, JSONResponse
import base64
from io import BytesIO

from app.application.services import RemocaoFundoService
from app.infrastructure.segmentation.u2net_service import U2NetService

app = FastAPI(
    title="Bemasnap Background Removal API",
    description="API para remoção de fundo de imagens usando U²-Net",
    version="2.0.0"
)

# Instancia o serviço de infraestrutura e o serviço de aplicação
u2net_service = U2NetService()
remocao_service = RemocaoFundoService(segmentador=u2net_service)


@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "nome": "Bemasnap Background Removal API",
        "versao": "2.0.0",
        "descricao": "API para remoção de fundo de imagens usando U²-Net",
        "endpoints": {
            "/remover-fundo/": "Remove fundo e retorna imagem PNG",
            "/processar-imagem/": "Remove fundo e retorna JSON com base64",
            "/docs": "Documentação interativa da API"
        }
    }


@app.post("/remover-fundo/")
async def remover_fundo(
    file: UploadFile = File(...), 
    visualizar: bool = Query(False, description="Se True, exibe inline; se False, faz download")
):
    """
    Remove o fundo de uma imagem e retorna o resultado.
    
    **Não salva arquivos localmente - processa tudo em memória!**
    
    - **file**: Arquivo de imagem (JPEG, PNG, etc.)
    - **visualizar**: Se True, exibe inline no navegador; se False, faz download
    
    Returns:
        Imagem processada com fundo transparente (PNG)
    """
    try:
        # Lê os bytes da imagem enviada
        imagem_bytes = await file.read()
        
        # Processa a imagem em memória
        resultado = remocao_service.remover_fundo(imagem_bytes, formato_saida="PNG")
        
        if resultado is None:
            return JSONResponse(
                status_code=500, 
                content={"erro": "Falha ao processar a imagem"}
            )
        
        # Retorna a imagem processada
        media_type = "image/png"
        filename = "imagem_sem_fundo.png"
        
        if visualizar:
            # Visualização inline
            return StreamingResponse(
                resultado,
                media_type=media_type,
                headers={"Content-Disposition": f"inline; filename={filename}"}
            )
        else:
            # Download
            return StreamingResponse(
                resultado,
                media_type=media_type,
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"erro": f"Erro ao processar requisição: {str(e)}"}
        )


@app.post("/processar-imagem/")
async def processar_imagem(file: UploadFile = File(...)):
    """
    Remove o fundo e retorna JSON com imagens em base64.
    
    **Não salva arquivos localmente - processa tudo em memória!**
    
    - **file**: Arquivo de imagem (JPEG, PNG, etc.)
    
    Returns:
        JSON com imagem original e processada em base64
    """
    try:
        # Lê os bytes da imagem original
        imagem_bytes = await file.read()
        tamanho_original = len(imagem_bytes)
        
        # Processa a imagem em memória
        resultado = remocao_service.remover_fundo(imagem_bytes, formato_saida="PNG")
        
        if resultado is None:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "erro",
                    "mensagem": "Falha ao processar a imagem"
                }
            )
        
        # Converte para base64
        resultado_bytes = resultado.getvalue()
        tamanho_processado = len(resultado_bytes)
        
        original_b64 = base64.b64encode(imagem_bytes).decode()
        processado_b64 = base64.b64encode(resultado_bytes).decode()
        
        return JSONResponse(content={
            "status": "sucesso",
            "mensagem": "Fundo removido com sucesso!",
            "imagem_original": {
                "data": f"data:image/jpeg;base64,{original_b64}",
                "tamanho_bytes": tamanho_original,
                "formato": file.content_type or "image/jpeg"
            },
            "imagem_processada": {
                "data": f"data:image/png;base64,{processado_b64}",
                "tamanho_bytes": tamanho_processado,
                "formato": "PNG",
                "transparencia": True
            },
            "info": {
                "algoritmo": "U²-Net",
                "processamento_concluido": True,
                "economia_armazenamento": "Nenhum arquivo salvo localmente"
            }
        })
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "erro",
                "mensagem": f"Erro ao processar requisição: {str(e)}"
            }
        )