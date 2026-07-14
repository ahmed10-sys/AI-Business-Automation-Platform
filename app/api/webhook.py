import logging
from fastapi import APIRouter, Query, HTTPException, Response, status
from app.config import settings
from app.schemas.webhook import WhatsAppWebhookPayload

logger = logging.getLogger("whatsapp_engine")

router = APIRouter(prefix="/webhook", tags=["Webhook"])

@router.get("")
async def verify_webhook(
    mode: str = Query(None, alias="hub.mode"),
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge"),
):
    """
    Webhook verification endpoint for WhatsApp Cloud API.
    """
    logger.info(f"Received webhook verification request. Mode: {mode}, Token: {token}")

    if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
        logger.info("Webhook successfully verified!")
        # Return the challenge as plain text
        return Response(content=challenge, media_type="text/plain")
    
    logger.warning("Webhook verification failed: Invalid verify token or mode.")
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Verification token mismatch or invalid mode"
    )

@router.post("")
async def receive_webhook(payload: WhatsAppWebhookPayload):
    """
    Endpoint to receive incoming WhatsApp messages and notifications.
    """
    logger.info("Received WhatsApp webhook event payload.")
    
    try:
        # Loop through entries and changes to log details of incoming messages
        for entry in payload.entry:
            for change in entry.changes:
                value = change.value
                
                # Check for incoming messages
                if value.messages:
                    for message in value.messages:
                        sender = message.from_
                        msg_id = message.id
                        msg_type = message.type
                        
                        if msg_type == "text" and message.text:
                            body = message.text.body
                            logger.info(f"Incoming Text Message from {sender} (ID: {msg_id}): '{body}'")
                        else:
                            logger.info(f"Incoming Message from {sender} of type: {msg_type} (ID: {msg_id})")
                            
                # Check for status updates (sent, delivered, read receipts)
                if value.statuses:
                    for status_update in value.statuses:
                        recipient = status_update.recipient_id
                        msg_status = status_update.status
                        logger.info(f"Message Status Update for {recipient}: {msg_status} (ID: {status_update.id})")
                        
    except Exception as e:
        logger.error(f"Error processing WhatsApp webhook event: {e}", exc_info=True)
        # We still return HTTP 200/202 to prevent WhatsApp from retrying and blocking our webhook.
        return {"status": "error", "message": "Failed to process, but webhook accepted"}

    return {"status": "ok"}
