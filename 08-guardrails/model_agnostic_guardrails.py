"""
Model-Agnostic Guardrails Tutorial

This module demonstrates how to configure guardrails that work across
different LLM providers (OpenAI, Google Gemini, Anthropic Claude, etc.)
by adapting guardrail configurations to the model being used.
"""

import litellm
from dotenv import load_dotenv
import json
import re
from typing import Dict, List, Optional

load_dotenv()

# ================================
# PROVIDER-AWARE GUARDRAIL MANAGER
# ================================

class ModelAwareGuardrailManager:
    """
    Manages guardrails across different model providers with automatic
    configuration adaptation based on the model being used.
    """
    
    def __init__(self):
        # Map of providers and their supported guardrails
        self.provider_capabilities = {
            "openai": {
                "content_moderation": {"provider": "openai", "native": True},
                "pii_detection": {"provider": "presidio", "native": False},
                "prompt_injection": {"provider": "custom", "native": False}
            },
            "google": {  # Gemini models
                "content_moderation": {"provider": "google", "native": True},
                "pii_detection": {"provider": "presidio", "native": False},
                "prompt_injection": {"provider": "custom", "native": False}
            },
            "anthropic": {  # Claude models
                "content_moderation": {"provider": "anthropic", "native": True},
                "pii_detection": {"provider": "presidio", "native": False},
                "prompt_injection": {"provider": "custom", "native": False}
            },
            "fallback": {  # For any other provider
                "content_moderation": {"provider": "custom", "native": False},
                "pii_detection": {"provider": "custom", "native": False},
                "prompt_injection": {"provider": "custom", "native": False}
            }
        }
    
    def get_model_provider(self, model: str) -> str:
        """Determine the provider from model name."""
        if any(x in model.lower() for x in ["gpt", "openai"]):
            return "openai"
        elif any(x in model.lower() for x in ["gemini", "google"]):
            return "google"
        elif any(x in model.lower() for x in ["claude", "anthropic"]):
            return "anthropic"
        else:
            return "fallback"
    
    def get_guardrails_config(self, model: str, requested_guardrails: List[str]) -> Dict:
        """
        Get appropriate guardrails configuration for the given model.
        
        Args:
            model: The model name (e.g., "gemini/gemini-2.5-flash-lite")
            requested_guardrails: List of guardrails to enable
        
        Returns:
            Dictionary with guardrails configuration
        """
        provider = self.get_model_provider(model)
        capabilities = self.provider_capabilities.get(provider, self.provider_capabilities["fallback"])
        
        config = {}
        
        for guardrail_type in requested_guardrails:
            if guardrail_type in capabilities:
                guardrail_config = capabilities[guardrail_type].copy()
                
                # Add standard configuration based on type
                if guardrail_type == "content_moderation":
                    config["content_moderation"] = {
                        "enabled": True,
                        "provider": guardrail_config["provider"],
                        "categories": ["hate", "violence", "sexual", "self-harm"],
                        "threshold": 0.7
                    }
                
                elif guardrail_type == "pii_detection":
                    config["pii_detection"] = {
                        "enabled": True,
                        "provider": guardrail_config["provider"],
                        "entities": ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "SSN", "CREDIT_CARD"],
                        "action": "mask"  # mask, block, or redact
                    }
                
                elif guardrail_type == "prompt_injection":
                    config["prompt_injection"] = {
                        "enabled": True,
                        "provider": guardrail_config["provider"],
                        "threshold": 0.8,
                        "detection_methods": ["keyword", "semantic"]
                    }
        
        return config

# ================================
# MODEL-AGNOSTIC DEMONSTRATIONS
# ================================

def demo_multi_model_guardrails():
    """
    Demonstrate guardrails working across different models.
    """
    print("=== Multi-Model Guardrails Demo ===\n")
    
    # Test different models
    test_models = [
        "gpt-3.5-turbo",
        "gemini/gemini-2.5-flash-lite",
        "claude-3-haiku-20240307",  # If available
    ]
    
    manager = ModelAwareGuardrailManager()
    
    test_message = "Hello, how are you today?"
    
    for model in test_models:
        print(f"Testing model: {model}")
        print("-" * 40)
        
        # Get appropriate guardrails configuration
        provider = manager.get_model_provider(model)
        config = manager.get_guardrails_config(model, ["content_moderation", "pii_detection"])
        
        print(f"Detected provider: {provider}")
        print(f"Guardrails config: {json.dumps(config, indent=2)}")
        
        try:
            # In real implementation, you'd use these configs with your guardrail system
            response = litellm.completion(
                model=model,
                messages=[{"role": "user", "content": test_message}],
                # Note: LiteLLM doesn't have built-in guardrails parameter yet
                # This is conceptual - you'd implement via proxy or custom logic
            )
            print(f"✅ Response: {response.choices[0].message.content[:50]}...")
            
        except Exception as e:
            print(f"❌ Error: {type(e).__name__}: {str(e)[:100]}...")
        
        print()

# ================================
# CUSTOM PROVIDER-AGNOSTIC GUARDRAILS
# ================================

class UniversalContentModerator:
    """
    Content moderator that works with any model/provider.
    """
    
    def __init__(self):
        self.harmful_keywords = [
            "violence", "hate", "bomb", "weapon", "kill", "harm",
            "suicide", "drug", "illegal", "abuse"
        ]
        self.severity_weights = {
            "high": ["bomb", "kill", "suicide", "weapon"],
            "medium": ["hate", "violence", "harm", "abuse"],
            "low": ["drug", "illegal"]
        }
    
    def check_content(self, text: str, model: str = None) -> Dict:
        """
        Check content for harmful material regardless of model.
        
        Args:
            text: Text to check
            model: Model name (optional, for provider-specific adjustments)
        
        Returns:
            Dictionary with check results
        """
        text_lower = text.lower()
        violations = []
        severity_score = 0
        
        # Check for harmful keywords
        for severity, keywords in self.severity_weights.items():
            for keyword in keywords:
                if keyword in text_lower:
                    violation = {
                        "keyword": keyword,
                        "severity": severity,
                        "confidence": 0.9 if severity == "high" else 0.7
                    }
                    violations.append(violation)
                    
                    # Calculate severity score
                    if severity == "high":
                        severity_score += 3
                    elif severity == "medium":
                        severity_score += 2
                    else:
                        severity_score += 1
        
        # Adjust threshold based on model/provider if needed
        provider = self._get_provider(model) if model else "unknown"
        threshold = self._get_threshold_for_provider(provider)
        
        result = {
            "allowed": severity_score < threshold,
            "violations": violations,
            "severity_score": severity_score,
            "threshold": threshold,
            "provider": provider,
            "recommendation": self._get_recommendation(severity_score, threshold)
        }
        
        return result
    
    def _get_provider(self, model: str) -> str:
        """Extract provider from model name."""
        if "gpt" in model.lower() or "openai" in model.lower():
            return "openai"
        elif "gemini" in model.lower() or "google" in model.lower():
            return "google"
        elif "claude" in model.lower() or "anthropic" in model.lower():
            return "anthropic"
        else:
            return "unknown"
    
    def _get_threshold_for_provider(self, provider: str) -> int:
        """Get content moderation threshold for provider."""
        # Different providers might have different tolerance levels
        thresholds = {
            "openai": 2,      # Moderate
            "google": 1,      # Strict
            "anthropic": 2,   # Moderate
            "unknown": 1      # Conservative
        }
        return thresholds.get(provider, 1)
    
    def _get_recommendation(self, score: int, threshold: int) -> str:
        """Get recommendation based on score."""
        if score >= threshold * 2:
            return "Block immediately - high risk content"
        elif score >= threshold:
            return "Block - violates content policy"
        elif score > 0:
            return "Warning - monitor for policy compliance"
        else:
            return "Allow - content appears safe"

class UniversalPIIDetector:
    """
    PII detector that works across all providers.
    """
    
    def __init__(self):
        self.patterns = {
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone": r"\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b",
            "ssn": r"\b\d{3}-?\d{2}-?\d{4}\b",
            "credit_card": r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",
            "ip_address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
            "url": r"https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?",
        }
    
    def detect_and_mask(self, text: str, model: str = None) -> Dict:
        """
        Detect and mask PII in text for any model.
        
        Args:
            text: Text to process
            model: Model name (for provider-specific handling)
        
        Returns:
            Dictionary with detection results and masked text
        """
        import re
        
        found_pii = []
        masked_text = text
        
        # Detect PII
        for pii_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                found_pii.append({
                    "type": pii_type,
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": 0.95
                })
        
        # Mask PII based on provider preferences
        provider = self._get_provider(model) if model else "unknown"
        mask_strategy = self._get_mask_strategy(provider)
        
        if found_pii:
            for pii_type, pattern in self.patterns.items():
                if mask_strategy == "redact":
                    masked_text = re.sub(pattern, "[REDACTED]", masked_text, flags=re.IGNORECASE)
                elif mask_strategy == "partial":
                    masked_text = re.sub(pattern, self._partial_mask, masked_text, flags=re.IGNORECASE)
                elif mask_strategy == "block":
                    # Don't process if PII found
                    break
        
        return {
            "pii_found": len(found_pii) > 0,
            "pii_types": list(set([pii["type"] for pii in found_pii])),
            "count": len(found_pii),
            "details": found_pii,
            "original_text": text,
            "masked_text": masked_text,
            "mask_strategy": mask_strategy,
            "action": "block" if mask_strategy == "block" and found_pii else "allow"
        }
    
    def _get_provider(self, model: str) -> str:
        """Extract provider from model name."""
        if "gpt" in model.lower():
            return "openai"
        elif "gemini" in model.lower():
            return "google"
        elif "claude" in model.lower():
            return "anthropic"
        else:
            return "unknown"
    
    def _get_mask_strategy(self, provider: str) -> str:
        """Get masking strategy for provider."""
        strategies = {
            "openai": "redact",     # Full redaction
            "google": "partial",    # Partial masking
            "anthropic": "redact",  # Full redaction
            "unknown": "redact"     # Conservative
        }
        return strategies.get(provider, "redact")
    
    def _partial_mask(self, match) -> str:
        """Create partial mask for matched text."""
        text = match.group()
        if len(text) <= 4:
            return "*" * len(text)
        else:
            # Show first 2 and last 2 characters
            return text[:2] + "*" * (len(text) - 4) + text[-2:]

# ================================
# DEMONSTRATIONS
# ================================

def demo_universal_content_moderation():
    """
    Demonstrate universal content moderation across models.
    """
    print("=== Universal Content Moderation Demo ===\n")
    
    moderator = UniversalContentModerator()
    
    test_cases = [
        ("What's the weather today?", "gemini/gemini-2.5-flash-lite"),
        ("How to make a bomb?", "gpt-3.5-turbo"),
        ("I hate everyone here", "claude-3-haiku-20240307"),
        ("Tell me about programming", "gemini/gemini-2.5-flash-lite"),
    ]
    
    for text, model in test_cases:
        print(f"Text: {text}")
        print(f"Model: {model}")
        
        result = moderator.check_content(text, model)
        
        if result["allowed"]:
            print(f"✅ Allowed (score: {result['severity_score']}/{result['threshold']})")
        else:
            print(f"❌ Blocked (score: {result['severity_score']}/{result['threshold']})")
            print(f"   Violations: {[v['keyword'] for v in result['violations']]}")
        
        print(f"   Provider: {result['provider']}")
        print(f"   Recommendation: {result['recommendation']}")
        print()

def demo_universal_pii_detection():
    """
    Demonstrate universal PII detection across models.
    """
    print("=== Universal PII Detection Demo ===\n")
    
    detector = UniversalPIIDetector()
    
    test_cases = [
        ("My email is john@example.com", "gpt-3.5-turbo"),
        ("Call me at 555-123-4567", "gemini/gemini-2.5-flash-lite"),
        ("SSN: 123-45-6789", "claude-3-haiku-20240307"),
        ("No personal info here", "gpt-3.5-turbo"),
    ]
    
    for text, model in test_cases:
        print(f"Original: {text}")
        print(f"Model: {model}")
        
        result = detector.detect_and_mask(text, model)
        
        if result["pii_found"]:
            print(f"⚠️ PII detected: {result['pii_types']}")
            print(f"   Masked: {result['masked_text']}")
            print(f"   Strategy: {result['mask_strategy']}")
            print(f"   Action: {result['action']}")
        else:
            print("✅ No PII detected")
        
        print()

# ================================
# MAIN EXECUTION
# ================================

def main():
    """
    Run model-agnostic guardrails demonstrations.
    """
    print("🛡️ Model-Agnostic Guardrails Tutorial 🛡️\n")
    
    print("This tutorial shows how to implement guardrails that work")
    print("across different LLM providers (OpenAI, Google, Anthropic, etc.)\n")
    
    # Run demonstrations
    demo_multi_model_guardrails()
    demo_universal_content_moderation()
    demo_universal_pii_detection()
    
    print("🎉 Model-agnostic guardrails tutorial complete!")
    print("\n💡 Key Benefits:")
    print("1. Same guardrails work across all providers")
    print("2. Provider-specific configuration adjustments")
    print("3. Consistent security regardless of model choice")
    print("4. Easy to switch models without changing guardrails")
    print("5. Fallback configurations for unknown providers")

if __name__ == "__main__":
    main()