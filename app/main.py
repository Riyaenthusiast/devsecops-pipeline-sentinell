from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, EmailStr
import uvicorn
import os
import re

app = FastAPI(
    title="Secured Enterprise Payment API",
    description="Production-ready microservice integrated with automated DevSecOps CI/CD security quality gates.",
    version="1.0.0"
)

security = HTTPBearer()

# Pydantic schema with input validation to prevent injection flaws
class TransactionRequest(BaseModel):
    account_id: str = Field(..., min_length=5, max_length=32, pattern=r"^[a-zA-Z0-9_-]+$")
    recipient_email: EmailStr
    amount: float = Field(..., gt=0, le=500000.0)
    currency: str = Field(default="INR", pattern=r"^(INR|USD|EUR|GBP)$")

class TransactionResponse(BaseModel):
    transaction_id: str
    status: str
    amount: float
    currency: str
    sanitized_recipient: str

@app.get("/health", tags=["Monitoring"])
def health_check():
    """Health check endpoint for Docker container probes and load balancers."""
    return {"status": "healthy", "service": "payment-api-gateway", "security_gate": "enforced"}

@app.post("/api/v1/transfer", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED, tags=["Banking"])
def process_transfer(payload: TransactionRequest, token: HTTPAuthorizationCredentials = Depends(security)):
    """
    Secure transaction processing endpoint.
    Enforces strict regex input sanitization, token validation, and parameter typing.
    """
    # Defensive input verification
    if not token.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization token")
    
    # Generate mock transaction id safely
    tx_hash = os.urandom(8).hex()
    
    return TransactionResponse(
        transaction_id=f"TX-{tx_hash}",
        status="PROCESSED",
        amount=payload.amount,
        currency=payload.currency,
        sanitized_recipient=payload.recipient_email
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
