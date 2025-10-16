"""
Script de teste para a API de remoção de fundo
Testa os endpoints sem salvar arquivos localmente
"""
import requests
import base64
from pathlib import Path

API_URL = "http://127.0.0.1:8000"

def test_root():
    """Testa o endpoint raiz"""
    print("🧪 Testando endpoint raiz...")
    response = requests.get(f"{API_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}\n")
    return response.status_code == 200

def test_remover_fundo_download(image_path: str):
    """Testa remoção de fundo com download"""
    print("🧪 Testando /remover-fundo/ (download)...")
    
    with open(image_path, "rb") as f:
        files = {"file": f}
        params = {"visualizar": False}
        response = requests.post(f"{API_URL}/remover-fundo/", files=files, params=params)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        output_path = "teste_resultado_download.png"
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Imagem salva em: {output_path}")
        print(f"Tamanho: {len(response.content)} bytes\n")
        return True
    else:
        print(f"❌ Erro: {response.text}\n")
        return False

def test_remover_fundo_visualizar(image_path: str):
    """Testa remoção de fundo com visualização inline"""
    print("🧪 Testando /remover-fundo/ (visualização inline)...")
    
    with open(image_path, "rb") as f:
        files = {"file": f}
        params = {"visualizar": True}
        response = requests.post(f"{API_URL}/remover-fundo/", files=files, params=params)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        output_path = "teste_resultado_inline.png"
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Imagem salva em: {output_path}")
        print(f"Tamanho: {len(response.content)} bytes\n")
        return True
    else:
        print(f"❌ Erro: {response.text}\n")
        return False

def test_processar_imagem_json(image_path: str):
    """Testa remoção de fundo com resposta JSON"""
    print("🧪 Testando /processar-imagem/ (JSON com base64)...")
    
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{API_URL}/processar-imagem/", files=files)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {data['status']}")
        print(f"Mensagem: {data['mensagem']}")
        print(f"Tamanho original: {data['imagem_original']['tamanho_bytes']} bytes")
        print(f"Tamanho processado: {data['imagem_processada']['tamanho_bytes']} bytes")
        print(f"Algoritmo: {data['info']['algoritmo']}")
        print(f"Info: {data['info']['economia_armazenamento']}\n")
        
        # Salva a imagem processada a partir do base64
        img_data = data['imagem_processada']['data'].split(',')[1]
        img_bytes = base64.b64decode(img_data)
        
        output_path = "teste_resultado_json.png"
        with open(output_path, "wb") as f:
            f.write(img_bytes)
        print(f"✅ Imagem extraída do JSON salva em: {output_path}\n")
        return True
    else:
        print(f"❌ Erro: {response.text}\n")
        return False

def test_performance(image_path: str, num_requests: int = 5):
    """Testa performance com múltiplas requisições"""
    print(f"🧪 Testando performance ({num_requests} requisições)...")
    
    import time
    
    times = []
    
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    
    for i in range(num_requests):
        files = {"file": ("test.jpg", image_bytes)}
        params = {"visualizar": False}
        
        start = time.time()
        response = requests.post(f"{API_URL}/remover-fundo/", files=files, params=params)
        end = time.time()
        
        elapsed = end - start
        times.append(elapsed)
        
        status = "✅" if response.status_code == 200 else "❌"
        print(f"  Requisição {i+1}: {status} {elapsed:.2f}s")
    
    avg_time = sum(times) / len(times)
    print(f"\n📊 Tempo médio: {avg_time:.2f}s")
    print(f"📊 Primeira requisição: {times[0]:.2f}s (com carregamento do modelo)")
    if len(times) > 1:
        avg_subsequent = sum(times[1:]) / len(times[1:])
        print(f"📊 Requisições subsequentes: {avg_subsequent:.2f}s (apenas inferência)\n")
    
    return True

def main():
    """Executa todos os testes"""
    # Verifica se há uma imagem de teste
    image_path = "backend/temp_uploads/input.jpg"
    
    if not Path(image_path).exists():
        print(f"❌ Imagem de teste não encontrada: {image_path}")
        print("Por favor, coloque uma imagem em backend/temp_uploads/input.jpg")
        return
    
    print("=" * 60)
    print("🚀 TESTE DA API DE REMOÇÃO DE FUNDO (V2.0)")
    print("=" * 60)
    print()
    
    tests = [
        ("Root Endpoint", lambda: test_root()),
        ("Download", lambda: test_remover_fundo_download(image_path)),
        ("Visualização Inline", lambda: test_remover_fundo_visualizar(image_path)),
        ("JSON com Base64", lambda: test_processar_imagem_json(image_path)),
        ("Performance", lambda: test_performance(image_path, 3))
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"❌ Erro no teste '{name}': {e}\n")
            results.append((name, False))
    
    print("=" * 60)
    print("📋 RESUMO DOS TESTES")
    print("=" * 60)
    
    for name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{status} - {name}")
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    print(f"\n🎯 {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram com sucesso!")
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.")

if __name__ == "__main__":
    main()
