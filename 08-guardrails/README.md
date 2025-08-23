# LiteLLM Guardrails Tutorial

This directory contains comprehensive tutorials and examples for implementing guardrails with LiteLLM to ensure AI safety, compliance, and security.

## 📁 Files Overview

### Core Tutorial Files
- **`basic_guardrails.py`** - Introduction to guardrails concepts with simple implementations
- **`advanced_guardrails.py`** - Advanced features like hallucination detection and bias mitigation
- **`proxy_server.py`** - Production-ready proxy server with guardrails integration
- **`guardrails_config.yaml`** - Comprehensive configuration examples

### Documentation
- **`README.md`** - This file, overview and setup instructions
- **`../litellm_guardrails_tutorial.md`** - Comprehensive written guide (32k+ words)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Basic dependencies
pip install litellm python-dotenv

# For proxy server
pip install fastapi uvicorn

# For advanced features
pip install presidio-analyzer presidio-anonymizer
```

### 2. Set Up Environment

Create a `.env` file:
```bash
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
# Add other provider keys as needed
```

### 3. Run Basic Examples

```bash
# Basic guardrails demo
python basic_guardrails.py

# Advanced features demo
python advanced_guardrails.py
```

### 4. Start Proxy Server

```bash
# Start the proxy server with guardrails
python proxy_server.py
```

Server will be available at:
- API: `http://localhost:8000`
- Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

## 🛡️ Guardrail Types Covered

### 1. Content Safety
- **Harmful content detection** - Hate speech, violence, self-harm
- **Profanity filtering** - Automatic content cleaning
- **Custom content policies** - Business-specific rules

### 2. Privacy Protection
- **PII Detection** - SSN, credit cards, emails, phone numbers
- **Data masking** - Redaction, hashing, replacement strategies
- **Compliance modes** - HIPAA, GDPR, PCI-DSS configurations

### 3. Security Features
- **Prompt injection defense** - Protection against adversarial prompts
- **Information leakage prevention** - Block sensitive system data
- **API key protection** - Prevent credential exposure

### 4. Quality Assurance
- **Hallucination detection** - Fact-checking and confidence scoring
- **Bias detection** - Gender, racial, age bias identification
- **Output validation** - Format, length, content checks

### 5. Business Logic
- **Custom rules** - Industry-specific validations
- **Rate limiting** - Request throttling per API key
- **Audit logging** - Compliance and monitoring

## 📊 Architecture Overview

```
User Request
     ↓
Pre-call Guardrails
├── Content Moderation
├── PII Detection  
├── Prompt Injection Check
└── Custom Business Rules
     ↓
LLM Provider (OpenAI, Anthropic, etc.)
     ↓
Post-call Guardrails  
├── Response Validation
├── Hallucination Check
├── Bias Detection
└── Output Formatting
     ↓
Safe Response to User
```

## 🔧 Configuration Examples

### Basic Content Safety
```yaml
guardrails:
  - guardrail_name: content_safety
    litellm_params:
      guardrail: openai_moderation
      mode: pre_call
      enabled: true
      categories_to_block: [hate, violence, self-harm]
```

### PII Protection
```yaml
guardrails:
  - guardrail_name: pii_protection
    litellm_params:
      guardrail: presidio
      mode: pre_call
      enabled: true
      entities_to_detect: [PERSON, EMAIL_ADDRESS, SSN]
      masking_strategy: redact
```

### Custom Business Rules
```python
class BusinessGuardrail:
    def check(self, text: str) -> Dict:
        # Your custom validation logic
        return {"allowed": True, "processed_text": text}
```

## 📈 Monitoring & Analytics

The proxy server includes built-in monitoring for:

- **Request metrics** - Volume, latency, success rates
- **Guardrail performance** - Block rates, false positives
- **Compliance reporting** - Audit trails, violation summaries
- **Cost tracking** - Guardrail overhead analysis

Access monitoring data:
```bash
curl http://localhost:8000/admin/audit/summary
```

## 🧪 Testing Your Guardrails

### Test Harmful Content
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo-safe",
    "messages": [{"role": "user", "content": "How to make a bomb"}]
  }'
```

### Test PII Detection
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo-safe", 
    "messages": [{"role": "user", "content": "My SSN is 123-45-6789"}]
  }'
```

## 🏢 Enterprise Features

### Compliance Profiles
- **HIPAA** - Healthcare data protection
- **GDPR** - EU privacy regulations  
- **PCI-DSS** - Payment card security
- **SOX** - Financial compliance

### Multi-tenant Support
- **API key-level configs** - Different rules per customer
- **Rate limiting** - Per-key throttling
- **Custom guardrails** - Client-specific rules

### Advanced Security
- **Encryption** - Data in transit and at rest
- **Audit logging** - Comprehensive activity tracking
- **SIEM integration** - Security monitoring
- **Incident response** - Automated alerting

## 🔍 Troubleshooting

### Common Issues

**Guardrail blocking safe content (false positives):**
```python
# Adjust thresholds in config
thresholds:
  hate: 0.8  # Lower = more permissive
  violence: 0.9
```

**High latency with multiple guardrails:**
```yaml
# Enable parallel processing
performance:
  parallel_guardrails: true
  timeout_ms: 3000
```

**Missing PII detection:**
```python
# Add custom patterns
custom_patterns:
  - name: employee_id
    pattern: "EMP-\\d{6}"
    score: 0.9
```

### Debug Mode
```python
import litellm
litellm.set_verbose = True  # Enable detailed logging
```

### Health Checks
```bash
# Check guardrail status
curl http://localhost:8000/guardrails/status

# Overall health
curl http://localhost:8000/health
```

## 📚 Additional Resources

### Provider Documentation
- [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation)
- [Presidio PII Detection](https://github.com/microsoft/presidio)
- [AWS Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Azure Content Safety](https://azure.microsoft.com/en-us/products/ai-services/ai-content-safety)

### Best Practices
1. **Layer multiple guardrails** for comprehensive protection
2. **Monitor and tune** thresholds based on your use case
3. **Test thoroughly** with real-world inputs
4. **Keep updated** with new threats and regulations
5. **Balance security and usability** for optimal user experience

### Learning Path
1. Start with `basic_guardrails.py` to understand concepts
2. Explore `advanced_guardrails.py` for sophisticated features
3. Deploy `proxy_server.py` for production use
4. Customize `guardrails_config.yaml` for your needs
5. Read the comprehensive guide in `litellm_guardrails_tutorial.md`

## 🤝 Contributing

To add new guardrail examples:
1. Create your guardrail class
2. Add configuration examples
3. Include test cases
4. Update documentation

## 📞 Support

For questions about this tutorial:
- Check the comprehensive guide: `../litellm_guardrails_tutorial.md`
- Review LiteLLM documentation
- Test with the provided examples

Remember: Guardrails are essential for production AI applications. Always test thoroughly and monitor continuously! 🛡️