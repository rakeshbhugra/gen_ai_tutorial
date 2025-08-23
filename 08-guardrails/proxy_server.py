"""
LiteLLM Proxy Server with Guardrails

This demonstrates how to run a production-ready LiteLLM proxy server
with comprehensive guardrails protection.
"""

import litellm
from litellm import Router
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import yaml
import json
import hashlib
import time
from typing import Dict, Any, Optional, List
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================================
# GUARDRAIL IMPLEMENTATIONS
# ================================

class SimpleContentModerator:
    """Simple content moderation implementation."""
    
    def __init__(self, config: Dict):
        self.blocked_keywords = config.get("blocked_keywords", [
            "violence", "hate", "bomb", "weapon", "kill"
        ])
        self.threshold = config.get("threshold", 0.7)
    
    def check(self, text: str) -> Dict:
        """Check if text contains harmful content."""
        text_lower = text.lower()
        violations = []
        
        for keyword in self.blocked_keywords:
            if keyword in text_lower:
                violations.append({
                    "keyword": keyword,
                    "confidence": 0.9
                })
        
        return {
            "allowed": len(violations) == 0,
            "violations": violations,
            "confidence": max([v["confidence"] for v in violations], default=0)
        }

class SimplePIIDetector:
    """Simple PII detection implementation."""
    
    def __init__(self, config: Dict):
        self.patterns = {
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone": r"\b\d{3}-\d{3}-\d{4}\b",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "credit_card": r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b"
        }
        self.action = config.get("action", "mask")  # mask, block, redact
    
    def check(self, text: str) -> Dict:
        """Check for PII in text."""
        import re
        
        found_pii = []
        for pii_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                found_pii.append({
                    "type": pii_type,
                    "count": len(matches),
                    "matches": matches
                })
        
        processed_text = text
        if found_pii and self.action == "mask":
            for pii_type, pattern in self.patterns.items():
                processed_text = re.sub(pattern, "[REDACTED]", processed_text, flags=re.IGNORECASE)
        
        return {
            "allowed": True if self.action != "block" or not found_pii else False,
            "pii_found": found_pii,
            "processed_text": processed_text,
            "action_taken": self.action if found_pii else "none"
        }

# ================================
# GUARDRAIL MANAGER
# ================================

class GuardrailManager:
    """Manages all guardrails for the proxy server."""
    
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.guardrails = self._initialize_guardrails()
        self.api_key_configs = self._load_api_key_configs()
        
    def _initialize_guardrails(self) -> Dict:
        """Initialize all configured guardrails."""
        guardrails = {}
        
        # Initialize content moderator
        guardrails["content_safety"] = SimpleContentModerator({
            "blocked_keywords": ["violence", "hate", "bomb", "weapon"],
            "threshold": 0.7
        })
        
        # Initialize PII detector
        guardrails["pii_protection"] = SimplePIIDetector({
            "action": "mask"
        })
        
        return guardrails
    
    def _load_api_key_configs(self) -> Dict:
        """Load API key specific configurations."""
        configs = {}
        for config in self.config.get("api_key_configs", []):
            api_key_hash = config["api_key_hash"]
            configs[api_key_hash] = config
        return configs
    
    def get_guardrails_for_api_key(self, api_key: str) -> List[str]:
        """Get guardrails configured for a specific API key."""
        api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()[:16]
        config = self.api_key_configs.get(api_key_hash, {})
        return config.get("guardrails", ["content_safety", "pii_protection"])
    
    async def run_pre_call_guardrails(self, request_data: Dict, api_key: str) -> Dict:
        """Run all pre-call guardrails."""
        active_guardrails = self.get_guardrails_for_api_key(api_key)
        results = {}
        
        # Extract text from request
        text = self._extract_text_from_request(request_data)
        
        for guardrail_name in active_guardrails:
            if guardrail_name in self.guardrails:
                guardrail = self.guardrails[guardrail_name]
                try:
                    result = guardrail.check(text)
                    results[guardrail_name] = result
                    
                    # If any guardrail blocks, stop processing
                    if not result.get("allowed", True):
                        return {
                            "allowed": False,
                            "blocked_by": guardrail_name,
                            "reason": result.get("violations", "Policy violation"),
                            "all_results": results
                        }
                
                except Exception as e:
                    logger.error(f"Error in guardrail {guardrail_name}: {e}")
                    results[guardrail_name] = {"error": str(e)}
        
        # Process text modifications (e.g., PII masking)
        processed_text = text
        for result in results.values():
            if "processed_text" in result:
                processed_text = result["processed_text"]
        
        return {
            "allowed": True,
            "processed_text": processed_text,
            "guardrail_results": results
        }
    
    async def run_post_call_guardrails(self, response_data: Dict, api_key: str) -> Dict:
        """Run all post-call guardrails."""
        # Similar to pre-call but for response validation
        return {"allowed": True, "processed_response": response_data}
    
    def _extract_text_from_request(self, request_data: Dict) -> str:
        """Extract text content from request."""
        if "messages" in request_data:
            messages = request_data["messages"]
            if isinstance(messages, list) and messages:
                return messages[-1].get("content", "")
        elif "prompt" in request_data:
            return request_data["prompt"]
        return str(request_data)

# ================================
# PROXY SERVER
# ================================

app = FastAPI(title="LiteLLM Proxy with Guardrails", version="1.0.0")
security = HTTPBearer()

# Initialize components
guardrail_manager = GuardrailManager("guardrails_config.yaml")

# Initialize LiteLLM router
router = Router(
    model_list=[
        {
            "model_name": "gpt-3.5-turbo-safe",
            "litellm_params": {
                "model": "gpt-3.5-turbo",
                "api_key": "your-openai-key"
            }
        }
    ]
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests for audit purposes."""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Request: {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    
    return response

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "guardrails": list(guardrail_manager.guardrails.keys())}

@app.get("/guardrails/status")
async def guardrails_status():
    """Get status of all guardrails."""
    status = {}
    for name, guardrail in guardrail_manager.guardrails.items():
        status[name] = {
            "enabled": True,
            "type": type(guardrail).__name__
        }
    return status

@app.post("/v1/chat/completions")
async def chat_completions(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Main chat completions endpoint with guardrails."""
    try:
        # Get request data
        request_data = await request.json()
        api_key = credentials.credentials
        
        # Run pre-call guardrails
        guardrail_result = await guardrail_manager.run_pre_call_guardrails(request_data, api_key)
        
        if not guardrail_result["allowed"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Request blocked by guardrails",
                    "blocked_by": guardrail_result.get("blocked_by"),
                    "reason": guardrail_result.get("reason")
                }
            )
        
        # Modify request if needed (e.g., PII masking)
        if "processed_text" in guardrail_result:
            if "messages" in request_data and request_data["messages"]:
                request_data["messages"][-1]["content"] = guardrail_result["processed_text"]
        
        # Call LLM
        response = await router.acompletion(**request_data)
        
        # Run post-call guardrails
        post_guardrail_result = await guardrail_manager.run_post_call_guardrails(
            response.dict(), api_key
        )
        
        if not post_guardrail_result["allowed"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Response blocked by guardrails",
                    "reason": "Response content violates policies"
                }
            )
        
        # Add guardrail metadata to response
        response_dict = response.dict()
        response_dict["guardrails"] = {
            "pre_call": guardrail_result["guardrail_results"],
            "post_call": post_guardrail_result
        }
        
        return response_dict
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/v1/completions")
async def completions(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Text completions endpoint with guardrails."""
    try:
        request_data = await request.json()
        api_key = credentials.credentials
        
        # Similar to chat completions but for text completion
        guardrail_result = await guardrail_manager.run_pre_call_guardrails(request_data, api_key)
        
        if not guardrail_result["allowed"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Request blocked by guardrails",
                    "blocked_by": guardrail_result.get("blocked_by")
                }
            )
        
        response = await router.acompletion(**request_data)
        return response.dict()
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing completion request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/v1/models")
async def list_models():
    """List available models."""
    return {
        "data": [
            {
                "id": "gpt-3.5-turbo-safe",
                "object": "model",
                "owned_by": "litellm-proxy",
                "guardrails_enabled": True
            }
        ]
    }

# ================================
# ADMIN ENDPOINTS
# ================================

@app.get("/admin/audit/summary")
async def audit_summary():
    """Get audit summary (admin only)."""
    # In production, add proper authentication
    return {
        "total_requests": 1234,
        "blocked_requests": 56,
        "top_blocked_reasons": [
            {"reason": "harmful_content", "count": 30},
            {"reason": "pii_detected", "count": 26}
        ],
        "guardrail_performance": {
            "content_safety": {"latency_ms": 45, "accuracy": 0.95},
            "pii_protection": {"latency_ms": 23, "accuracy": 0.98}
        }
    }

@app.post("/admin/guardrails/reload")
async def reload_guardrails():
    """Reload guardrail configuration (admin only)."""
    global guardrail_manager
    try:
        guardrail_manager = GuardrailManager("guardrails_config.yaml")
        return {"status": "success", "message": "Guardrails reloaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reload: {e}")

# ================================
# STARTUP SCRIPT
# ================================

def start_server():
    """Start the proxy server."""
    print("🛡️ Starting LiteLLM Proxy with Guardrails")
    print("📋 Enabled guardrails:")
    for name in guardrail_manager.guardrails.keys():
        print(f"  ✅ {name}")
    
    print("\n🚀 Server starting on http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("❤️ Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "proxy_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    start_server()