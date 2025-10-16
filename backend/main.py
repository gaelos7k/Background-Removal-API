import os
from app.presentation.api import app

if __name__ == "__main__":
    import uvicorn
    
    # Pega a porta do ambiente (Render usa PORT)
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "app.presentation.api:app",
        host="0.0.0.0",  # ← CRUCIAL PARA O RENDER
        port=port,
        reload=False,    # ← Desabilita reload em produção
        workers=1
    )