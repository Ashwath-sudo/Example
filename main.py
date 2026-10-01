from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from fastguard import FastGuardAnalyzer

app = FastAPI(title="FastGuard API - Base Version")

# ------------------------------------------------------------------------------
# BASE SCHEMA & ROUTES
# ------------------------------------------------------------------------------
class UserRequest(BaseModel):
    user_id: int = Field(..., description="Unique user integer ID")
    email: str = Field(..., description="User email address")

class UserResponse(BaseModel):
    user_id: int
    email: str
    status: str = "ACTIVE"

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserRequest):
    return UserResponse(user_id=user.user_id, email=user.email, status="ACTIVE")

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return UserResponse(user_id=user_id, email="user@example.com", status="ACTIVE")

# ------------------------------------------------------------------------------
# LOCAL FASTGUARD INSPECTION
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("🔍 Executing FastGuard AST Inspection (Baseline)...")
    guard = FastGuardAnalyzer()
    is_breaking, prob, details = guard.analyze_diff(base="origin/main", head="HEAD")
    
    status_label = "❌ BLOCK" if is_breaking else "✅ PASS"
    print(f"Result: {status_label} | Breaking Probability: {prob:.4f}\n")
    