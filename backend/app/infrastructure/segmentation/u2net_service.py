import sys
import os
import subprocess
import shutil
from typing import Optional
import numpy as np
from PIL import Image

class U2NetService:
    """
    Serviço de infraestrutura responsável por executar o modelo U²-Net para remoção de fundo.
    """
    def __init__(self, u2net_dir: Optional[str] = None):
        # Caminho para o diretório do U²-Net
        self.u2net_dir = u2net_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../U-2-Net'))

    def remover_fundo(self, caminho_entrada: str, caminho_saida: str) -> bool:
        """
        Executa o script do U²-Net para remover o fundo da imagem (segmentação de produtos).
        - caminho_entrada: caminho da imagem original
        - caminho_saida: caminho do arquivo de saída (imagem sem fundo, não é usado diretamente)
        Retorna True se o processamento foi bem-sucedido.
        """
        # Script do U²-Net para segmentação de objetos/produtos
        script_path = os.path.join(self.u2net_dir, 'u2net_test.py')
        # Caminho do modelo (no diretório do projeto, não do U²-Net)
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
        model_path = os.path.join(project_root, 'saved_models', 'u2net', 'u2net.pth')
        # Diretório de saída
        output_dir = os.path.dirname(caminho_saida)
        os.makedirs(output_dir, exist_ok=True)
        print(f"DEBUG: Output directory: {output_dir}")
        print(f"DEBUG: Input file exists: {os.path.exists(caminho_entrada)}")
        print(f"DEBUG: U2Net script exists: {os.path.exists(script_path)}")

        # Usa o diretório de uploads como parâmetro para o script
        upload_dir = os.path.dirname(caminho_entrada)

        # Monta o comando para rodar o script do U²-Net
        command = [
            sys.executable,
            script_path,
            '--image_path', upload_dir,
            '--output_dir', output_dir,
            '--model_path', model_path
        ]
        print(f"Executando: {' '.join(command)}")
        print(f"DEBUG: Working directory: {self.u2net_dir}")
        try:
            result = subprocess.run(command, capture_output=True, text=True, cwd=self.u2net_dir)
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            print("RETURN CODE:", result.returncode)
            # O script gera o arquivo removendo a extensão original (ex: input.jpg -> input.png)
            base_name = os.path.splitext(os.path.basename(caminho_entrada))[0]
            saida_gerada = os.path.join(output_dir, f"{base_name}.png")
            # Aplica a máscara na imagem original para remover o fundo
            if os.path.exists(saida_gerada):
                self._aplicar_mascara_remover_fundo(caminho_entrada, saida_gerada, caminho_saida)
                return True
            else:
                print(f"Arquivo de saída não encontrado: {saida_gerada}")
                return False
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar U²-Net: {e.stderr}")
            return False

    def _aplicar_mascara_remover_fundo(self, imagem_original: str, mascara_path: str, saida_path: str):
        """
        Aplica a máscara na imagem original para remover o fundo, gerando uma imagem com transparência.
        """
        try:
            # Carrega a imagem original
            img_original = Image.open(imagem_original).convert("RGBA")
            
            # Carrega a máscara (gerada pelo U²-Net)
            mascara = Image.open(mascara_path).convert("L")  # Converte para escala de cinza
            
            # Redimensiona a máscara para o tamanho da imagem original, se necessário
            if mascara.size != img_original.size:
                mascara = mascara.resize(img_original.size, Image.LANCZOS)
            
            # Converte máscara para array numpy para processamento
            mascara_array = np.array(mascara)
            
            # Normaliza a máscara (0-255 para 0-1)
            mascara_norm = mascara_array / 255.0
            
            # Aplica a máscara no canal alfa (transparência)
            img_array = np.array(img_original)
            img_array[:, :, 3] = (mascara_norm * 255).astype(np.uint8)
            
            # Cria a imagem final com fundo removido
            img_sem_fundo = Image.fromarray(img_array, "RGBA")
            
            # Salva a imagem final
            img_sem_fundo.save(saida_path, "PNG")
            print(f"Imagem sem fundo salva em: {saida_path}")
            
        except Exception as e:
            print(f"Erro ao aplicar máscara: {e}")
            # Fallback: copia a máscara se houver erro
            shutil.copy(mascara_path, saida_path)

__all__ = ["U2NetService"]