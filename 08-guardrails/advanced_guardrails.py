"""
Advanced LiteLLM Guardrails Implementation

This module demonstrates advanced guardrail concepts:
1. Hallucination detection and fact-checking
2. Bias detection and mitigation
3. Enterprise security features
4. Custom business logic guardrails
5. Async guardrail processing
"""

import litellm
from dotenv import load_dotenv
import asyncio
import json
import re
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

load_dotenv()

# ================================
# 1. HALLUCINATION DETECTION
# ================================

class HallucinationDetector:
    """
    Advanced hallucination detection using multiple strategies.
    """
    
    def __init__(self, knowledge_base: Dict[str, Any] = None):
        self.knowledge_base = knowledge_base or {}
        self.confidence_threshold = 0.7
        
    def detect_hallucinations(self, text: str, context: str = None) -> Dict:
        """
        Detect potential hallucinations in LLM output.
        """
        findings = []
        
        # 1. Check for specific facts against knowledge base
        factual_claims = self._extract_factual_claims(text)
        for claim in factual_claims:
            if not self._verify_claim(claim):
                findings.append({
                    "type": "unverified_fact",
                    "claim": claim,
                    "confidence": 0.8
                })
        
        # 2. Check for temporal inconsistencies
        temporal_issues = self._check_temporal_consistency(text)
        if temporal_issues:
            findings.extend(temporal_issues)
        
        # 3. Check for logical contradictions
        contradictions = self._find_contradictions(text)
        if contradictions:
            findings.extend(contradictions)
        
        # 4. Check confidence markers
        low_confidence = self._detect_uncertainty_markers(text)
        if low_confidence:
            findings.append({
                "type": "low_confidence",
                "markers": low_confidence,
                "confidence": 0.6
            })
        
        return {
            "has_hallucinations": len(findings) > 0,
            "findings": findings,
            "overall_confidence": self._calculate_confidence(findings)
        }
    
    def _extract_factual_claims(self, text: str) -> List[str]:
        """Extract statements that appear to be factual claims."""
        # Simplified implementation
        sentences = text.split('.')
        claims = []
        
        fact_patterns = [
            r"is \d+",  # Numerical facts
            r"was founded in",  # Historical facts
            r"located in",  # Geographic facts
            r"costs? \$",  # Price facts
        ]
        
        for sentence in sentences:
            for pattern in fact_patterns:
                if re.search(pattern, sentence, re.IGNORECASE):
                    claims.append(sentence.strip())
                    break
        
        return claims
    
    def _verify_claim(self, claim: str) -> bool:
        """Verify a claim against knowledge base."""
        # Check if claim matches known facts
        for key, value in self.knowledge_base.items():
            if key.lower() in claim.lower():
                # Simple verification - in production, use semantic similarity
                return True
        return False
    
    def _check_temporal_consistency(self, text: str) -> List[Dict]:
        """Check for temporal inconsistencies."""
        issues = []
        
        # Look for date/time contradictions
        dates = re.findall(r'\b(19|20)\d{2}\b', text)
        if dates and len(set(dates)) > 1:
            # Multiple different years mentioned - could be inconsistent
            issues.append({
                "type": "temporal_inconsistency",
                "details": f"Multiple years mentioned: {dates}",
                "confidence": 0.5
            })
        
        return issues
    
    def _find_contradictions(self, text: str) -> List[Dict]:
        """Find logical contradictions in text."""
        contradictions = []
        
        # Look for contradictory terms
        contradiction_pairs = [
            ("always", "never"),
            ("all", "none"),
            ("increase", "decrease"),
            ("positive", "negative")
        ]
        
        text_lower = text.lower()
        for word1, word2 in contradiction_pairs:
            if word1 in text_lower and word2 in text_lower:
                contradictions.append({
                    "type": "logical_contradiction",
                    "terms": [word1, word2],
                    "confidence": 0.7
                })
        
        return contradictions
    
    def _detect_uncertainty_markers(self, text: str) -> List[str]:
        """Detect uncertainty markers in text."""
        uncertainty_phrases = [
            "might be", "possibly", "perhaps", "maybe",
            "I think", "I believe", "it seems", "apparently",
            "roughly", "approximately", "around", "about"
        ]
        
        found_markers = []
        text_lower = text.lower()
        for phrase in uncertainty_phrases:
            if phrase in text_lower:
                found_markers.append(phrase)
        
        return found_markers
    
    def _calculate_confidence(self, findings: List[Dict]) -> float:
        """Calculate overall confidence score."""
        if not findings:
            return 1.0
        
        # Weight different finding types
        weights = {
            "unverified_fact": 0.3,
            "temporal_inconsistency": 0.2,
            "logical_contradiction": 0.3,
            "low_confidence": 0.2
        }
        
        total_weight = 0
        for finding in findings:
            finding_type = finding.get("type", "")
            confidence = finding.get("confidence", 0.5)
            weight = weights.get(finding_type, 0.1)
            total_weight += weight * (1 - confidence)
        
        return max(0, 1 - total_weight)

# ================================
# 2. BIAS DETECTION AND MITIGATION
# ================================

class BiasDetector:
    """
    Detect and mitigate various types of bias in AI outputs.
    """
    
    def __init__(self):
        self.bias_categories = {
            "gender": ["he", "she", "man", "woman", "male", "female"],
            "race": ["white", "black", "asian", "hispanic", "latino"],
            "age": ["young", "old", "elderly", "millennial", "boomer"],
            "religion": ["christian", "muslim", "jewish", "hindu", "buddhist"]
        }
        
        self.stereotypes = {
            "gender": [
                "women are emotional",
                "men are strong",
                "girls like pink",
                "boys don't cry"
            ],
            "occupation": [
                "nurses are women",
                "engineers are men",
                "secretaries are female"
            ]
        }
    
    def analyze_bias(self, text: str) -> Dict:
        """
        Analyze text for various types of bias.
        """
        analysis = {
            "has_bias": False,
            "bias_types": [],
            "severity": "none",
            "details": [],
            "mitigation_suggestions": []
        }
        
        # Check for demographic bias
        demographic_bias = self._check_demographic_bias(text)
        if demographic_bias:
            analysis["bias_types"].append("demographic")
            analysis["details"].extend(demographic_bias)
        
        # Check for stereotypes
        stereotype_bias = self._check_stereotypes(text)
        if stereotype_bias:
            analysis["bias_types"].append("stereotype")
            analysis["details"].extend(stereotype_bias)
        
        # Check for exclusionary language
        exclusion_bias = self._check_exclusionary_language(text)
        if exclusion_bias:
            analysis["bias_types"].append("exclusionary")
            analysis["details"].extend(exclusion_bias)
        
        # Determine overall bias presence and severity
        if analysis["details"]:
            analysis["has_bias"] = True
            analysis["severity"] = self._calculate_severity(analysis["details"])
            analysis["mitigation_suggestions"] = self._generate_mitigations(analysis["details"])
        
        return analysis
    
    def _check_demographic_bias(self, text: str) -> List[Dict]:
        """Check for demographic bias."""
        biases = []
        text_lower = text.lower()
        
        for category, terms in self.bias_categories.items():
            term_counts = {}
            for term in terms:
                count = text_lower.count(term)
                if count > 0:
                    term_counts[term] = count
            
            # Check for imbalanced representation
            if term_counts and len(term_counts) > 1:
                max_count = max(term_counts.values())
                min_count = min(term_counts.values())
                if max_count > min_count * 2:  # Significant imbalance
                    biases.append({
                        "type": f"{category}_imbalance",
                        "details": term_counts,
                        "severity": "medium"
                    })
        
        return biases
    
    def _check_stereotypes(self, text: str) -> List[Dict]:
        """Check for stereotypical statements."""
        found_stereotypes = []
        text_lower = text.lower()
        
        for category, stereotypes in self.stereotypes.items():
            for stereotype in stereotypes:
                if any(word in text_lower for word in stereotype.split()):
                    found_stereotypes.append({
                        "type": f"{category}_stereotype",
                        "pattern": stereotype,
                        "severity": "high"
                    })
        
        return found_stereotypes
    
    def _check_exclusionary_language(self, text: str) -> List[Dict]:
        """Check for exclusionary or non-inclusive language."""
        exclusions = []
        
        exclusionary_patterns = [
            (r'\bguys\b', "gender-specific term", "people/everyone"),
            (r'\bmanpower\b', "gendered term", "workforce/staff"),
            (r'\bchairman\b', "gendered title", "chairperson/chair"),
            (r'\bnormal people\b', "ableist language", "typical/most people")
        ]
        
        for pattern, issue, suggestion in exclusionary_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                exclusions.append({
                    "type": "exclusionary_language",
                    "issue": issue,
                    "suggestion": suggestion,
                    "severity": "low"
                })
        
        return exclusions
    
    def _calculate_severity(self, details: List[Dict]) -> str:
        """Calculate overall bias severity."""
        severities = [d.get("severity", "low") for d in details]
        
        if "high" in severities:
            return "high"
        elif "medium" in severities:
            return "medium"
        else:
            return "low"
    
    def _generate_mitigations(self, details: List[Dict]) -> List[str]:
        """Generate mitigation suggestions."""
        suggestions = []
        
        for detail in details:
            detail_type = detail.get("type", "")
            
            if "imbalance" in detail_type:
                suggestions.append("Ensure balanced representation of all groups")
            elif "stereotype" in detail_type:
                suggestions.append("Avoid stereotypical characterizations")
            elif "exclusionary" in detail_type:
                suggestion = detail.get("suggestion", "")
                if suggestion:
                    suggestions.append(f"Replace with: {suggestion}")
        
        return list(set(suggestions))  # Remove duplicates

# ================================
# 3. ENTERPRISE SECURITY GUARDRAIL
# ================================

class EnterpriseSecurityGuardrail:
    """
    Enterprise-grade security guardrail with compliance features.
    """
    
    def __init__(self, compliance_mode: str = "standard"):
        self.compliance_mode = compliance_mode  # standard, hipaa, pci, gdpr
        self.audit_log = []
        self.blocked_patterns = self._load_blocked_patterns()
        
    def _load_blocked_patterns(self) -> Dict:
        """Load patterns to block based on compliance mode."""
        patterns = {
            "standard": {
                "secrets": [
                    r"api[_-]?key[\s:=]+[\w\-]+",
                    r"password[\s:=]+[\w\-]+",
                    r"token[\s:=]+[\w\-]+"
                ],
                "pii": [
                    r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
                    r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b"  # Credit card
                ]
            },
            "hipaa": {
                "phi": [
                    r"patient\s+\w+",
                    r"diagnosis[:=]\s*\w+",
                    r"medical\s+record\s+#?\d+"
                ]
            },
            "pci": {
                "cardholder": [
                    r"cvv[\s:=]+\d{3,4}",
                    r"card\s+number[\s:=]+[\d\s\-]+"
                ]
            },
            "gdpr": {
                "personal": [
                    r"email[\s:=]+[\w\.\-]+@[\w\.\-]+",
                    r"phone[\s:=]+[\d\s\-\+\(\)]+"
                ]
            }
        }
        
        # Combine patterns based on compliance mode
        combined = patterns.get("standard", {}).copy()
        if self.compliance_mode != "standard":
            mode_patterns = patterns.get(self.compliance_mode, {})
            combined.update(mode_patterns)
        
        return combined
    
    async def check_request(self, request_data: Dict) -> Dict:
        """
        Comprehensive security check for incoming requests.
        """
        violations = []
        
        # Extract text to check
        text = self._extract_text(request_data)
        
        # Check for blocked patterns
        for category, patterns in self.blocked_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    violations.append({
                        "category": category,
                        "pattern": pattern,
                        "matches": len(matches),
                        "action": "block"
                    })
        
        # Log the check
        await self._audit_log_entry({
            "timestamp": datetime.now().isoformat(),
            "type": "request_check",
            "violations": violations,
            "blocked": len(violations) > 0
        })
        
        return {
            "allowed": len(violations) == 0,
            "violations": violations,
            "compliance_mode": self.compliance_mode
        }
    
    async def check_response(self, response_data: Dict) -> Dict:
        """
        Check LLM response for security violations.
        """
        violations = []
        
        # Extract response text
        text = self._extract_text(response_data)
        
        # Check for information leakage
        leakage = self._check_information_leakage(text)
        if leakage:
            violations.extend(leakage)
        
        # Check compliance-specific requirements
        compliance_issues = self._check_compliance_requirements(text)
        if compliance_issues:
            violations.extend(compliance_issues)
        
        # Log the check
        await self._audit_log_entry({
            "timestamp": datetime.now().isoformat(),
            "type": "response_check",
            "violations": violations,
            "requires_redaction": len(violations) > 0
        })
        
        return {
            "allowed": len(violations) == 0,
            "violations": violations,
            "redacted_response": self._redact_response(text, violations) if violations else text
        }
    
    def _extract_text(self, data: Dict) -> str:
        """Extract text from request/response data."""
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            # Handle different data structures
            if "messages" in data:
                return " ".join([msg.get("content", "") for msg in data["messages"]])
            elif "content" in data:
                return data["content"]
            elif "text" in data:
                return data["text"]
        return str(data)
    
    def _check_information_leakage(self, text: str) -> List[Dict]:
        """Check for potential information leakage."""
        leaks = []
        
        # Check for internal system information
        internal_patterns = [
            r"internal\s+api",
            r"database\s+schema",
            r"system\s+architecture",
            r"deployment\s+configuration"
        ]
        
        for pattern in internal_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                leaks.append({
                    "type": "information_leakage",
                    "pattern": pattern,
                    "severity": "high"
                })
        
        return leaks
    
    def _check_compliance_requirements(self, text: str) -> List[Dict]:
        """Check compliance-specific requirements."""
        issues = []
        
        if self.compliance_mode == "hipaa":
            # Check for unencrypted PHI
            if re.search(r"patient", text, re.IGNORECASE) and not re.search(r"encrypted|redacted", text, re.IGNORECASE):
                issues.append({
                    "type": "hipaa_violation",
                    "issue": "Potential unencrypted PHI",
                    "severity": "critical"
                })
        
        elif self.compliance_mode == "gdpr":
            # Check for consent mentions
            if re.search(r"personal data|user data", text, re.IGNORECASE) and not re.search(r"consent|permission", text, re.IGNORECASE):
                issues.append({
                    "type": "gdpr_violation",
                    "issue": "Personal data without consent mention",
                    "severity": "high"
                })
        
        return issues
    
    def _redact_response(self, text: str, violations: List[Dict]) -> str:
        """Redact sensitive information from response."""
        redacted = text
        
        for violation in violations:
            if "pattern" in violation:
                # Replace matched patterns with [REDACTED]
                pattern = violation["pattern"]
                redacted = re.sub(pattern, "[REDACTED]", redacted, flags=re.IGNORECASE)
        
        return redacted
    
    async def _audit_log_entry(self, entry: Dict):
        """Add entry to audit log."""
        self.audit_log.append(entry)
        
        # In production, also send to external logging system
        # await self._send_to_siem(entry)
    
    def get_audit_report(self) -> Dict:
        """Generate audit report."""
        total_checks = len(self.audit_log)
        blocked_requests = sum(1 for entry in self.audit_log if entry.get("blocked") or entry.get("requires_redaction"))
        
        return {
            "total_checks": total_checks,
            "blocked_requests": blocked_requests,
            "block_rate": blocked_requests / total_checks if total_checks > 0 else 0,
            "compliance_mode": self.compliance_mode,
            "recent_violations": self.audit_log[-10:]  # Last 10 entries
        }

# ================================
# 4. DEMO FUNCTIONS
# ================================

def demo_hallucination_detection():
    """Demonstrate hallucination detection."""
    print("=== Hallucination Detection Demo ===\n")
    
    # Initialize detector with knowledge base
    knowledge_base = {
        "company_founded": "2020",
        "headquarters": "San Francisco",
        "employees": "500",
        "product": "AI Assistant"
    }
    
    detector = HallucinationDetector(knowledge_base)
    
    test_outputs = [
        "Our company was founded in 2020 in San Francisco.",  # Correct
        "We have over 10,000 employees worldwide.",  # Hallucination
        "Our product costs $99 per month, or maybe $199, I think around that range.",  # Uncertainty
        "Sales increased while revenue decreased significantly.",  # Contradiction
    ]
    
    for output in test_outputs:
        print(f"Text: {output[:50]}...")
        result = detector.detect_hallucinations(output)
        
        if result["has_hallucinations"]:
            print(f"⚠️ Potential hallucinations detected!")
            print(f"   Confidence: {result['overall_confidence']:.2f}")
            for finding in result["findings"]:
                print(f"   - {finding['type']}: {finding.get('claim', finding.get('details', ''))[:50]}")
        else:
            print(f"✅ No hallucinations detected (confidence: {result['overall_confidence']:.2f})")
        
        print()

def demo_bias_detection():
    """Demonstrate bias detection and mitigation."""
    print("=== Bias Detection Demo ===\n")
    
    detector = BiasDetector()
    
    test_texts = [
        "The engineer fixed the problem. He was very skilled.",  # Gender bias
        "All nurses are caring. She helped the patient.",  # Stereotype
        "Hey guys, let's discuss the new feature.",  # Exclusionary
        "The team includes diverse professionals from various backgrounds.",  # Inclusive
    ]
    
    for text in test_texts:
        print(f"Text: {text[:50]}...")
        analysis = detector.analyze_bias(text)
        
        if analysis["has_bias"]:
            print(f"⚠️ Bias detected!")
            print(f"   Types: {', '.join(analysis['bias_types'])}")
            print(f"   Severity: {analysis['severity']}")
            print(f"   Suggestions:")
            for suggestion in analysis["mitigation_suggestions"]:
                print(f"   - {suggestion}")
        else:
            print("✅ No significant bias detected")
        
        print()

async def demo_enterprise_security():
    """Demonstrate enterprise security features."""
    print("=== Enterprise Security Demo ===\n")
    
    # Test different compliance modes
    for mode in ["standard", "hipaa", "gdpr"]:
        print(f"Testing {mode.upper()} compliance mode:")
        guardrail = EnterpriseSecurityGuardrail(compliance_mode=mode)
        
        # Test request
        test_request = {
            "messages": [{
                "role": "user",
                "content": "My API key is sk-1234567890 and SSN is 123-45-6789"
            }]
        }
        
        result = await guardrail.check_request(test_request)
        
        if result["allowed"]:
            print("  ✅ Request allowed")
        else:
            print("  ❌ Request blocked")
            print(f"     Violations: {len(result['violations'])}")
            for violation in result["violations"]:
                print(f"     - {violation['category']}: {violation['matches']} matches")
        
        print()

# ================================
# MAIN EXECUTION
# ================================

async def main():
    """Run all advanced guardrail demonstrations."""
    print("🛡️ Advanced LiteLLM Guardrails 🛡️\n")
    
    # Run demos
    demo_hallucination_detection()
    demo_bias_detection()
    await demo_enterprise_security()
    
    print("\n🎉 Advanced guardrails demonstration complete!")
    print("\n📚 Key capabilities demonstrated:")
    print("1. Multi-strategy hallucination detection")
    print("2. Comprehensive bias analysis")
    print("3. Enterprise security with compliance modes")
    print("4. Audit logging and reporting")
    print("5. Automated redaction and mitigation")

if __name__ == "__main__":
    asyncio.run(main())