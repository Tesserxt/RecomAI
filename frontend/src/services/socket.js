const WS_URL = "ws://localhost:8000/ws";

export function connectSocket({ onMessage, onOpen, onClose }) {
    const ws = new WebSocket(WS_URL);

    ws.onopen = () => {
        console.log("WebSocket connected");
        onOpen?.();
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        onMessage?.(data);
    };

    ws.onclose = () => {
        console.log("WebSocket disconnected");
        onClose?.();
    };

    ws.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    return ws;
}

export function sendMessage(ws, message) {
    if (ws?.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(message));
    }
}