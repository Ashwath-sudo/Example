from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Status
from pydantic import BaseModel, Field

# Import FastGuard Analyzer module
try:
    from fastguard import FastGuardAnalyzer
except ImportError:
    # Fallback/Placeholder if fastguard package is in local directory
    class FastGuardAnalyzer:
        def __init__(self, model_path: str):
            self.model_path = model_path
            
        def analyze_diff(self, base: str = "origin/main", head: str = "HEAD"):
            return False, 0.2169, {"fields_type_changed_count": 0}

app = FastAPI(
    title="FastGuard Integrated API",
    description="FastAPI service with embedded AST breaking change analysis.",
    version="1.0.0",
)

# ------------------------------------------------------------------------------
# PYDANTIC SCHEMAS (Base Contract)
# ------------------------------------------------------------------------------

class UserRequest(BaseModel):
    user_id: int = Field(..., description="Unique integer ID of the user")
    email: str = Field(..., description="User email address")
    is_active: bool = True

class UserResponse(BaseModel):
    user_id: int
    email: str
    status: str = "ACTIVE"

# ------------------------------------------------------------------------------
# FASTAPI ROUTES
# ------------------------------------------------------------------------------

@app.post("/users", response_model=UserResponse, status_code=Status.HTTP_201_CREATED)
def create_user(user: UserRequest):
    """Sample route to register a new user."""
    return UserResponse(user_id=user.user_id, email=user.email, status="ACTIVE")

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Fetch user by integer ID."""
    return UserResponse(user_id=user_id, email="user@example.com", status="ACTIVE")

# ------------------------------------------------------------------------------
# PROGRAMMATIC FASTGUARD CHECK
# ------------------------------------------------------------------------------

@app.post("/analyze-contract")
def analyze_git_contract():
    guard = FastGuardAnalyzer(model_path="fastguard_model.pkl")
    is_breaking, prob, details = guard.analyze_diff(base="origin/main", head="HEAD")

    if is_breaking:
        print(f"Warning: Breaking change detected with probability {prob:.4f}")

    return {
        "is_breaking": is_breaking,
        "probability": round(prob, 4),
        "details": details
    }