# backend/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import connectMqttBoth as Mqtt

app = FastAPI()

# CORS erlauben fürs Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

players = {}  # {"player1": websocket, "player2": websocket}
ball_positions = {"ball1": 50, "ball2": 50}  # 0–100 Sliderwerte

@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    await websocket.accept()
    players[player_id] = websocket
    print(f"{player_id} verbunden.")

    try:
        while True:
            data = await websocket.receive_json()
            # Spieler 1 steuert Ball 2 und umgekehrt
            if player_id == "player1":
                ball_positions["ball2"] = data["value"]
            elif player_id == "player2":
                ball_positions["ball1"] = data["value"]

            # Neue Positionen an beide Spieler senden
            for p_ws in players.values():
                await p_ws.send_json(ball_positions)

    except WebSocketDisconnect:
        print(f"{player_id} hat getrennt.")
        del players[player_id]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
