import sys
import os
from typing import Optional, Union
from io import BytesIO
import numpy as np
from PIL import Image
import torch
from torchvision import transforms

class U2NetService:
    """
    Serviço de infraestrutura responsável por executar o modelo U²-Net para remoção de fundo.
    Processa imagens em memória sem salvar arquivos localmente.
    """
    def __init__(self, u2net_dir: Optional[str] = None):
        # Caminho para o diretório do U²-Net
        self.u2net_dir = u2net_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../U-2-Net'))
        self.model = None
        self.model_loaded = False
        self._carregar_modelo()

        self.model = None
        self.model_loaded = False
        self._carregar_modelo()

    def _carregar_modelo(self):
        """Carrega o modelo U2Net em memória uma única vez."""
        try:
            # Adiciona o diretório U2Net ao path para importar os módulos
            sys.path.insert(0, self.u2net_dir)
            from model import U2NET
            
            model_path = os.path.join(self.u2net_dir, 'saved_models', 'u2net', 'u2net.pth')
            
            if not os.path.exists(model_path):
                print(f"ERRO: Modelo não encontrado em {model_path}")
                return
            
            print(f"Carregando modelo U2Net de {model_path}...")
            self.model = U2NET(3, 1)
            
            if torch.cuda.is_available():
                self.model.load_state_dict(torch.load(model_path))
                self.model.cuda()
                print("Modelo carregado na GPU")
            else:
                self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
                print("Modelo carregado na CPU")
            
            self.model.eval()
            self.model_loaded = True
            print("Modelo U2Net carregado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao carregar modelo U2Net: {e}")
            self.model_loaded = False

    def remover_fundo(self, imagem_bytes: Union[bytes, BytesIO], formato_saida: str = "PNG") -> Optional[BytesIO]:
        """
        Remove o fundo de uma imagem processando em memória.
        
        Args:
            imagem_bytes: Bytes da imagem de entrada ou objeto BytesIO
            formato_saida: Formato da imagem de saída (PNG, JPEG, etc.)
        
        Returns:
            BytesIO contendo a imagem processada com fundo removido, ou None se houver erro
        """
        if not self.model_loaded:
            print("ERRO: Modelo não foi carregado corretamente")
            return None
        
        try:
            # Converte bytes para PIL Image
            if isinstance(imagem_bytes, bytes):
                imagem_bytes = BytesIO(imagem_bytes)
            
            imagem_original = Image.open(imagem_bytes).convert("RGB")
            tamanho_original = imagem_original.size
            
            print(f"Processando imagem {tamanho_original[0]}x{tamanho_original[1]}...")
            
            # Prepara a imagem para o modelo
            imagem_tensor = self._preparar_imagem(imagem_original)
            
            # Executa a inferência
            with torch.no_grad():
                if torch.cuda.is_available():
                    imagem_tensor = imagem_tensor.cuda()
                
                d1, d2, d3, d4, d5, d6, d7 = self.model(imagem_tensor)
                
                # Normaliza a predição
                pred = d1[:, 0, :, :]
                pred = self._normalizar_pred(pred)
                
                # Converte para numpy
                mascara = pred.squeeze().cpu().data.numpy()
            
            # Cria a máscara em PIL Image
            mascara_img = Image.fromarray((mascara * 255).astype(np.uint8)).convert('L')
            mascara_img = mascara_img.resize(tamanho_original, Image.LANCZOS)
            
            # Aplica a máscara na imagem original
            imagem_resultado = self._aplicar_mascara(imagem_original, mascara_img)
            
            # Converte para BytesIO
            output_buffer = BytesIO()
            imagem_resultado.save(output_buffer, format=formato_saida)
            output_buffer.seek(0)
            
            print(f"Processamento concluído! Tamanho do resultado: {len(output_buffer.getvalue())} bytes")
            
            return output_buffer
            
        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _preparar_imagem(self, imagem: Image.Image) -> torch.Tensor:
        """Prepara a imagem para inferência no modelo."""
        transform = transforms.Compose([
            transforms.Resize((320, 320)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        tensor = transform(imagem).unsqueeze(0)
        return tensor

    def _normalizar_pred(self, pred: torch.Tensor) -> torch.Tensor:
        """Normaliza a predição do modelo."""
        ma = torch.max(pred)
        mi = torch.min(pred)
        return (pred - mi) / (ma - mi + 1e-8)

    def _aplicar_mascara(self, imagem_original: Image.Image, mascara: Image.Image) -> Image.Image:
        """
        Aplica a máscara na imagem original para remover o fundo.
        
        Args:
            imagem_original: Imagem original em RGB
            mascara: Máscara em escala de cinza (L)
        
        Returns:
            Imagem com fundo removido (RGBA)
        """
        # Converte para RGBA se necessário
        if imagem_original.mode != 'RGBA':
            imagem_original = imagem_original.convert('RGBA')
        
        # Converte para arrays numpy
        img_array = np.array(imagem_original)
        mascara_array = np.array(mascara)
        
        # Aplica a máscara no canal alfa
        img_array[:, :, 3] = mascara_array
        
        # Cria a imagem final
        imagem_resultado = Image.fromarray(img_array, 'RGBA')
        
        return imagem_resultado

__all__ = ["U2NetService"]