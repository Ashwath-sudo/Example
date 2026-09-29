from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from fastguard import FastGuardAnalyzer  # Imports clean installed package

app = FastAPI(title="FastGuard Integrated API")

class UserRequest(BaseModel):
    user_id: str = Field(..., description="ID as string")

@app.post("/analyze-contract")
def analyze_git_contract():
    guard = FastGuardAnalyzer()
    is_breaking, prob, details = guard.analyze_diff(base="origin/main", head="HEAD")

    return {
        "is_breaking": is_breaking,
        "probability": round(prob, 4),
        "details": details
    }

if __name__ == "__main__":
    print("🔍 Executing FastGuard AST Inspection...\n")
    guard = FastGuardAnalyzer()
    is_breaking, prob, details = guard.analyze_diff(base="main", head="HEAD")
    
    status_label = "❌ BLOCK" if is_breaking else "✅ PASS"
    print(f"Result: {status_label} | Breaking Probability: {prob:.4f}\n")

    # --------------------------------------------------------------------------
    # DETAILED BREAKAGE REPORT DISPLAY
    # --------------------------------------------------------------------------
    print("=" * 60)
    print("📋 FASTGUARD AST BREAKING CHANGE DETAILED REPORT")
    print("=" * 60)

    if isinstance(details, dict):
        # Extract raw CLI standard output if available
        raw_out = details.get("raw_output", "").strip()
        if raw_out:
            print(raw_out)
        else:
            # Print structured key-value feature details
            for key, value in details.items():
                if key != "exit_code":
                    print(f" • {key.replace('_', ' ').title()}: {value}")
    else:
        print(details)

    print("=" * 60)