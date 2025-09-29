"""
Script de teste para o endpoint de remoção de fundo
"""
import requests
import os

def test_background_removal():
    """Testa o endpoint de remoção de fundo"""
    
    # URL do endpoint
    url = "http://localhost:8000/api/v1/remove-background/"
    
    # Caminho da imagem de teste
    image_path = r"C:\Users\L77ga\OneDrive\Área de Trabalho\life_changing\temp_uploads\input.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Imagem de teste não encontrada: {image_path}")
        return
    
    print(f"📤 Enviando imagem: {image_path}")
    
    # Fazendo o upload
    try:
        with open(image_path, 'rb') as f:
            files = {'file': ('input.jpg', f, 'image/jpeg')}
            
            print("🔄 Processando... (pode levar alguns segundos)")
            response = requests.post(url, files=files)
        
        if response.status_code == 200:
            print("✅ Sucesso!")
            
            # Salvando o resultado
            output_path = r"C:\Users\L77ga\OneDrive\Área de Trabalho\life_changing\resultado_teste.jpg"
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"💾 Imagem processada salva em: {output_path}")
            
            # Verificando se o arquivo foi criado
            if os.path.exists(output_path):
                size = os.path.getsize(output_path)
                print(f"📊 Tamanho do arquivo: {size} bytes")
            else:
                print("❌ Arquivo não foi criado")
                
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")

if __name__ == "__main__":
    test_background_removal()