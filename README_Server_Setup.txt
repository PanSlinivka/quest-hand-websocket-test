🦾 WebSocket Server + Cloudflare Tunnel Setup (for Oculus Quest)

Tento stručný návod popisuje, jak spustit WebSocket server pro připojení z Oculus Questu a jak nastavit Cloudflare Tunnel, aby bylo možné se připojit k serveru přes internet.

──────────────────────────────
1️⃣ Spuštění WebSocket serveru
──────────────────────────────

1. Otevři terminál.
2. Zadej příkazy:

cd ~/g1_pickplace_project
source .venv/bin/activate
mjpython ws_server/server.py

✅ Pokud vše proběhne správně, uvidíš:
[WS] Server running on ws://0.0.0.0:8765

──────────────────────────────
2️⃣ Spuštění Cloudflare Tunnel
──────────────────────────────

1. Otevři nové terminálové okno (neukončuj server!).
2. Zadej příkaz:

cloudflared tunnel --url http://localhost:8765

3. Po chvíli se zobrazí adresa, např.:
https://refuse-yields-javascript-adelaide.trycloudflare.com

4. Přidej prefix wss:// a použij ji v prohlížeči Oculus Questu:
wss://refuse-yields-javascript-adelaide.trycloudflare.com

──────────────────────────────
3️⃣ Připojení z Oculus Questu
──────────────────────────────

1. Otevři Meta Browser v headsetu.
2. Načti stránku:
https://panslinivka.github.io/quest-hand-websocket-test/?v=1.6.2

3. Do pole „WebSocket Address“ vlož svou Cloudflare adresu.
4. Klikni na „Connect“ a pak na „Enter VR“.

✅ Pokud se vše načte správně, uvidíš šedou podlahu, světlo a koule reagující na pohyb rukou.
