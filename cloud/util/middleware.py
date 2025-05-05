from functools import wraps
import json
from fastapi import HTTPException
from mycrypto.mycrypto import decrypt_and_verify, load_private_key
from util.models import ItemCreatePlain #ItemCreate

def decrypt_request_data(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request_data = kwargs.get('item')
        if not request_data or not hasattr(request_data, 'encrypted_data'):
            raise HTTPException(
                status_code=400,
                detail="Verschlüsselte Daten fehlen"
            )
            
        try:
            receiver_key = load_private_key("IHR_PASSWORT")
            sender_key = None
            
            decrypted_data = decrypt_and_verify(
                receiver_key,
                sender_key,
                request_data.encrypted_data.dict()
            )
            
            decoded_data = json.loads(decrypted_data.decode())
            kwargs['item'] = ItemCreate(**decoded_data)
            
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Entschlüsselungsfehler: {str(e)}"
            )
            
        return await func(*args, **kwargs)
    return wrapper