import asyncio
import json
import os
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Ultron Neural Bridge")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# AUTO-DETECT EXISTING BRAIN FUNCTION
# ------------------------------------------------------------------------------
existing_brain_func = None

for mod_name in ['brain', 'main', 'agent', 'core', 'ultron_brain', 'llm']:
    try:
        mod = __import__(mod_name)
        for fn_name in ['ask_ultron', 'chat', 'generate_response', 'process_query', 'get_response', 'run_agent']:
            if hasattr(mod, fn_name):
                existing_brain_func = getattr(mod, fn_name)
                print(f"[ULTRON LINK] Existing Brain Hook Detected: {mod_name}.{fn_name}()")
                break
        if existing_brain_func:
            break
    except ImportError:
        pass

async def query_existing_brain(prompt: str):
    """Calls your existing brain or streams tactical reply"""
    if existing_brain_func:
        try:
            if asyncio.iscoroutinefunction(existing_brain_func):
                res = await existing_brain_func(prompt)
            else:
                res = await asyncio.to_thread(existing_brain_func, prompt)
            
            # If generator or string
            if hasattr(res, '__iter__') and not isinstance(res, (str, bytes, dict)):
                for chunk in res:
                    yield str(chunk)
            else:
                yield str(res)
            return
        except Exception as e:
            yield f"[BRAIN ERROR: {str(e)} - Falling back to core diagnostics]"

    # Fallback to local response if brain module wasn't directly imported
    tactical_stream = [
        f"Directive received: '{prompt}'. ",
        "Neural telemetry synchronized. ",
        "Executing tactical response matrix. Systems nominal."
    ]
    for seg in tactical_stream:
        yield seg
        await asyncio.sleep(0.06)

# ------------------------------------------------------------------------------
# WEBSOCKET STREAMING GATEWAY
# ------------------------------------------------------------------------------
@app.websocket("/ws/ultron")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(">>> [ULTRON LINK] 3D Mainframe UI Connected.")
    
    await websocket.send_json({
        "type": "status",
        "state": "BRAIN_CONNECTED",
        "message": "LISTENING // BRAIN CONNECTED"
    })

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            msg_type = data.get("type")

            if msg_type == "text_query":
                query_text = data.get("text", "").strip()
                if not query_text:
                    continue

                await websocket.send_json({"type": "stream_start"})
                full_reply = ""
                async for chunk in query_existing_brain(query_text):
                    full_reply += chunk
                    await websocket.send_json({"type": "stream_chunk", "token": chunk})
                
                await websocket.send_json({"type": "stream_end", "full_text": full_reply})

            elif msg_type == "audio_amplitude":
                amp = data.get("amplitude", 0.15)
                await websocket.send_json({"type": "harmonics_echo", "amplitude": amp})

    except WebSocketDisconnect:
        print(">>> [ULTRON LINK] 3D Mainframe Disconnected.")

def start_server():
    uvicorn.run("ultron_bridge:app", host="127.0.0.1", port=8000, log_level="warning")

if __name__ == "__main__":
    start_server()
