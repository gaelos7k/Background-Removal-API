from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
import base64

from app.domain.entities import Imagem
from app.application.services import RemocaoFundoService
from app.infrastructure.segmentation.u2net_service import U2NetService

app = FastAPI()

# Instancia o serviço de infraestrutura e o serviço de aplicação
u2net_service = U2NetService()
remocao_service = RemocaoFundoService(segmentador=u2net_service)

# Pasta temporária para uploads e resultados
UPLOAD_DIR = os.path.abspath("temp_uploads")
RESULT_DIR = os.path.abspath("temp_results")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

@app.post("/remover-fundo/")
async def remover_fundo(file: UploadFile = File(...), visualizar: bool = Query(False, description="Se True, exibe a imagem no navegador; se False, faz download")):
    """
    Remove o fundo de uma imagem
    
    - **file**: Arquivo de imagem (JPEG, PNG, etc.)
    - **visualizar**: Se True, a imagem será exibida diretamente no navegador; se False, será baixada
    
    Retorna a imagem processada com fundo transparente
    """
    """
    Endpoint para upload de imagem e remoção de fundo.
    Retorna a imagem processada.
    """
    # Limpa a pasta de uploads antes de salvar o novo arquivo
    for f in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    # Salva o arquivo enviado com nome simples
    upload_path = os.path.join(UPLOAD_DIR, "input.jpg")
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Cria entidade Imagem
    imagem = Imagem(caminho_arquivo=upload_path)

    # Define caminho de saída simples
    saida_path = os.path.join(RESULT_DIR, "sem_fundo.jpg")

    # Orquestra a remoção de fundo
    imagem_resultado = remocao_service.remover_fundo(imagem, saida_path)

    if imagem_resultado:
        # Retorna a imagem processada
        if visualizar:
            # Visualização inline no navegador
            return FileResponse(
                saida_path, 
                media_type="image/png",
                headers={"Content-Disposition": "inline; filename=imagem_sem_fundo.png"}
            )
        else:
            # Download da imagem
            return FileResponse(
                saida_path, 
                media_type="image/png",
                filename="imagem_sem_fundo.png"
            )
    else:
        return JSONResponse(status_code=500, content={"erro": "Falha ao remover fundo da imagem."})


@app.post("/visualizar-sem-fundo/")
async def visualizar_sem_fundo(file: UploadFile = File(...)):
    """
    Remove o fundo de uma imagem e exibe diretamente no navegador
    
    - **file**: Arquivo de imagem (JPEG, PNG, etc.)
    
    Retorna a imagem processada com fundo transparente para visualização inline
    """
    # Limpa a pasta de upload de arquivos antigos
    for f in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    # Salva o arquivo enviado com nome simples
    upload_path = os.path.join(UPLOAD_DIR, "input.jpg")
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Cria entidade Imagem
    imagem = Imagem(caminho_arquivo=upload_path)

    # Define caminho de saída simples
    saida_path = os.path.join(RESULT_DIR, "visualizar_sem_fundo.png")

    # Orquestra a remoção de fundo
    imagem_resultado = remocao_service.remover_fundo(imagem, saida_path)

    if imagem_resultado:
        # Sempre retorna para visualização inline no navegador
        return FileResponse(
            saida_path, 
            media_type="image/png",
            headers={
                "Content-Disposition": "inline; filename=resultado_sem_fundo.png",
                "Cache-Control": "no-cache"
            }
        )
    else:
        return JSONResponse(status_code=500, content={"erro": "Falha ao remover fundo da imagem."})


@app.post("/processar-imagem/")
async def processar_imagem(file: UploadFile = File(...)):
    """
    Remove o fundo de uma imagem e retorna dados da imagem em JSON com base64
    
    - **file**: Arquivo de imagem (JPEG, PNG, etc.)
    
    Retorna JSON com imagem original e processada em base64 para visualização
    """
    # Limpa a pasta de upload de arquivos antigos
    for f in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    # Salva o arquivo enviado com nome simples
    upload_path = os.path.join(UPLOAD_DIR, "input.jpg")
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Cria entidade Imagem
    imagem = Imagem(caminho_arquivo=upload_path)

    # Define caminho de saída simples
    saida_path = os.path.join(RESULT_DIR, "processar_imagem.png")

    # Orquestra a remoção de fundo
    imagem_resultado = remocao_service.remover_fundo(imagem, saida_path)

    if imagem_resultado:
        # Converte as imagens para base64
        with open(upload_path, "rb") as img_file:
            original_b64 = base64.b64encode(img_file.read()).decode()
        
        with open(saida_path, "rb") as img_file:
            processed_b64 = base64.b64encode(img_file.read()).decode()
        
        # Obter informações das imagens
        original_size = os.path.getsize(upload_path)
        processed_size = os.path.getsize(saida_path)
        
        return JSONResponse(content={
            "status": "sucesso",
            "mensagem": "Fundo removido com sucesso!",
            "imagem_original": {
                "data": f"data:image/jpeg;base64,{original_b64}",
                "tamanho_bytes": original_size,
                "formato": "JPEG"
            },
            "imagem_processada": {
                "data": f"data:image/png;base64,{processed_b64}",
                "tamanho_bytes": processed_size,
                "formato": "PNG",
                "transparencia": True
            },
            "info": {
                "algoritmo": "U²-Net",
                "processamento_concluido": True,
                "download_url": "/remover-fundo/",
                "visualizar_url": "/visualizar-sem-fundo/"
            }
        })
    else:
        return JSONResponse(status_code=500, content={
            "status": "erro",
            "mensagem": "Falha ao remover fundo da imagem.",
            "imagem_original": None,
            "imagem_processada": None
        })