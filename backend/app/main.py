"""
FastAPI para remoção de fundo com U²-Net
Versão original funcional restaurada
"""
import os
import sys
import uuid
import shutil
import base64
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F
from torchvision import transforms

# Adicionar U-2-Net ao path
sys.path.append(str(Path(__file__).parent.parent.parent / "U-2-Net"))

try:
    from model import U2NET
except ImportError:
    print("Aviso: Modelo U2NET não encontrado. Usando versão mock.")
    U2NET = None

# Configurações
BASE_DIR = Path(__file__).parent.parent.parent
UPLOAD_DIR = BASE_DIR / "temp_uploads"
RESULT_DIR = BASE_DIR / "temp_results"
MODEL_PATH = BASE_DIR / "saved_models" / "u2net" / "u2net.pth"

# Criar diretórios
UPLOAD_DIR.mkdir(exist_ok=True)
RESULT_DIR.mkdir(exist_ok=True)

# Inicializar FastAPI
app = FastAPI(
    title="Background Removal API",
    description="API para remoção de fundo usando U²-Net",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo global
model = None
device = torch.device("cpu")


def load_model():
    """Carrega o modelo U²-Net"""
    global model

    if U2NET is None:
        print("Modelo U2NET não disponível")
        return False

    try:
        model = U2NET(3, 1)

        if MODEL_PATH.exists():
            model.load_state_dict(torch.load(
                str(MODEL_PATH), map_location=device))
            print(f"Modelo carregado de: {MODEL_PATH}")
        else:
            print("Arquivo do modelo não encontrado, usando pesos aleatórios")

        model.to(device)
        model.eval()
        return True

    except Exception as e:
        print(f"Erro ao carregar modelo: {e}")
        model = None
        return False


def preprocess_image(image_path):
    """Preprocessa a imagem para o modelo"""
    transform = transforms.Compose([
        transforms.Resize((320, 320)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    image = Image.open(image_path).convert('RGB')
    image_tensor = transform(image).unsqueeze(0)
    return image_tensor.to(device), image.size


def postprocess_mask(pred, original_size):
    """Pós-processa a máscara"""
    pred = F.sigmoid(pred)
    pred = pred.squeeze().cpu().data.numpy()

    # Normalizar para 0-255
    pred = (pred - pred.min()) / (pred.max() - pred.min())
    pred = (pred * 255).astype(np.uint8)

    # Converter para PIL e redimensionar
    mask = Image.fromarray(pred, mode='L')
    mask = mask.resize(original_size, Image.LANCZOS)

    return mask


def remove_background_simple(input_path, output_path):
    """Remove fundo da imagem (versão simples)"""
    try:
        # Se não temos modelo, usar versão mock
        if model is None:
            image = Image.open(input_path)
            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            # Salvar como PNG com transparência
            image.save(output_path, 'PNG')
            return True

        # Processar com modelo real
        with torch.no_grad():
            input_tensor, original_size = preprocess_image(input_path)

            # Inferência
            d1, d2, d3, d4, d5, d6, d7 = model(input_tensor)
            pred = d1[:, 0, :, :]

            # Pós-processar
            mask = postprocess_mask(pred, original_size)

            # Aplicar máscara
            original = Image.open(input_path).convert('RGBA')
            mask_array = np.array(mask) / 255.0

            original_array = np.array(original)
            original_array[:, :, 3] = (mask_array * 255).astype(np.uint8)

            # Salvar resultado
            result = Image.fromarray(original_array, 'RGBA')
            result.save(output_path, 'PNG')

            return True

    except Exception as e:
        print(f"Erro na remoção: {e}")
        return False


@app.on_event("startup")
async def startup_event():
    """Inicialização da aplicação"""
    print("Inicializando aplicação...")
    success = load_model()
    if success:
        print("✅ Modelo U²-Net carregado com sucesso")
    else:
        print("⚠️  Usando modo mock (sem modelo)")


@app.get("/")
def read_root():
    """Endpoint raiz"""
    return {"message": "API de remoção de fundo funcionando!"}


@app.get("/health")
def health_check():
    """Verificação de saúde"""
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "device": str(device)
    }


@app.post("/api/v1/remove-background/")
async def remove_background(file: UploadFile = File(...)):
    """
    Remove o fundo de uma imagem
    """
    # Validar arquivo
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Arquivo deve ser uma imagem")

    # Gerar nome único
    file_id = str(uuid.uuid4())
    input_filename = f"{file_id}_{file.filename}"
    output_filename = f"{file_id}_no_bg.png"

    input_path = UPLOAD_DIR / input_filename
    output_path = RESULT_DIR / output_filename

    try:
        # Salvar arquivo de entrada
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Processar imagem
        success = remove_background_simple(input_path, output_path)

        if not success:
            raise HTTPException(
                status_code=500, detail="Erro ao processar imagem")

        # Retornar arquivo processado
        return FileResponse(
            path=str(output_path),
            media_type="image/png",
            filename=f"sem_fundo_{file.filename.split('.')[0]}.png"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

    finally:
        # Limpeza
        if input_path.exists():
            try:
                input_path.unlink()
            except:
                pass


@app.get("/api/v1/results/{filename}")
def get_result(filename: str):
    """Recupera resultado processado"""
    file_path = RESULT_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    return FileResponse(path=str(file_path), media_type="image/png")


@app.post("/api/v1/processar-imagem/")
async def processar_imagem(file: UploadFile = File(...)):
    """
    Remove o fundo de uma imagem e retorna dados em JSON com imagens em base64
    
    - **file**: Arquivo de imagem (JPEG, PNG, etc.)
    
    Retorna JSON com imagem original e processada em base64 para visualização direta
    """
    # Validar arquivo
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Arquivo deve ser uma imagem")

    # Gerar nome único
    file_id = str(uuid.uuid4())
    input_filename = f"{file_id}_{file.filename}"
    output_filename = f"{file_id}_processed.png"

    input_path = UPLOAD_DIR / input_filename
    output_path = RESULT_DIR / output_filename

    try:
        # Salvar arquivo de entrada
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Processar imagem
        success = remove_background_simple(input_path, output_path)

        if not success:
            raise HTTPException(
                status_code=500, detail="Erro ao processar imagem")

        # Converter imagens para base64
        with open(input_path, "rb") as img_file:
            original_b64 = base64.b64encode(img_file.read()).decode()
        
        with open(output_path, "rb") as img_file:
            processed_b64 = base64.b64encode(img_file.read()).decode()
        
        # Obter informações das imagens
        original_size = input_path.stat().st_size
        processed_size = output_path.stat().st_size
        
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
                "file_id": file_id,
                "download_url": f"/api/v1/results/{output_filename}"
            }
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

    finally:
        # Limpeza do arquivo de entrada
        if input_path.exists():
            try:
                input_path.unlink()
            except:
                pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
