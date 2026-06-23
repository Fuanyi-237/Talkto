from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
import json

from app.core.deps import get_db, get_current_active_user
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse, MediaUploadResponse
from app.models.user import User
from app.models.chat import ChatMessage

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    from app.core.security import decode_token
    
    # Verify token
    payload = decode_token(token)
    if payload is None:
        await websocket.close(code=1008)
        return
    
    user_id = payload.get("sub")
    if user_id is None:
        await websocket.close(code=1008)
        return
    
    # Get user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        await websocket.close(code=1008)
        return
    
    await manager.connect(user_id, websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Handle different message types
            if message_data.get("type") == "message":
                # Save message to database
                receiver_id = message_data.get("receiver_id")
                content = message_data.get("content")
                media_url = message_data.get("media_url")
                appointment_id = message_data.get("appointment_id")
                
                if receiver_id and content:
                    chat_message = ChatMessage(
                        sender_id=user_id,
                        receiver_id=receiver_id,
                        content=content,
                        media_url=media_url,
                        appointment_id=appointment_id,
                    )
                    
                    db.add(chat_message)
                    await db.commit()
                    await db.refresh(chat_message)
                    
                    # Send to receiver if online
                    response = {
                        "type": "message",
                        "data": {
                            "id": str(chat_message.id),
                            "sender_id": str(chat_message.sender_id),
                            "receiver_id": str(chat_message.receiver_id),
                            "content": chat_message.content,
                            "media_url": chat_message.media_url,
                            "is_read": chat_message.is_read,
                            "created_at": chat_message.created_at.isoformat(),
                        }
                    }
                    
                    await manager.send_personal_message(json.dumps(response), receiver_id)
                    await manager.send_personal_message(json.dumps(response), user_id)
            
            elif message_data.get("type") == "typing":
                # Send typing indicator
                receiver_id = message_data.get("receiver_id")
                if receiver_id:
                    typing_data = {
                        "type": "typing",
                        "sender_id": user_id,
                        "is_typing": message_data.get("is_typing", False)
                    }
                    await manager.send_personal_message(json.dumps(typing_data), receiver_id)
            
            elif message_data.get("type") == "read_receipt":
                # Mark message as read
                message_id = message_data.get("message_id")
                if message_id:
                    result = await db.execute(
                        select(ChatMessage).where(
                            ChatMessage.id == message_id,
                            ChatMessage.receiver_id == user_id
                        )
                    )
                    message = result.scalar_one_or_none()
                    
                    if message:
                        message.is_read = True
                        await db.commit()
                        
                        # Notify sender
                        receipt_data = {
                            "type": "read_receipt",
                            "message_id": message_id,
                            "reader_id": user_id
                        }
                        await manager.send_personal_message(json.dumps(receipt_data), str(message.sender_id))
    
    except WebSocketDisconnect:
        manager.disconnect(user_id)


@router.get("/history/{counselor_id}", response_model=list[ChatMessageResponse])
async def get_chat_history(
    counselor_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Get messages between current user and counselor
    query = select(ChatMessage).where(
        (ChatMessage.sender_id == current_user.id) & (ChatMessage.receiver_id == counselor_id) |
        (ChatMessage.sender_id == counselor_id) & (ChatMessage.receiver_id == current_user.id)
    ).order_by(ChatMessage.created_at.asc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    messages = result.scalars().all()
    
    return messages


@router.post("/media", response_model=MediaUploadResponse)
async def upload_chat_media(
    current_user: User = Depends(get_current_active_user)
):
    # In production, this would upload to AWS S3
    # For now, return a placeholder URL
    return MediaUploadResponse(
        media_url="https://placeholder.com/media/file.jpg"
    )
