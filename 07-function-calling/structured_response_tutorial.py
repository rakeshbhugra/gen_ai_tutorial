"""
Structured Response Tutorial - Day 4: From RAG to Smart Query Processing
===================================================================

This tutorial covers:
1. Query Interpretation for better RAG
2. Structured Outputs with Pydantic
3. Business Classification
4. Integration with existing RAG pipeline
"""

from pydantic import BaseModel, Field
from typing import List, Literal
import json
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def get_llm_response(messages, model="gemini/gemini-1.5-flash"):
    """
    Helper function for LLM completion using Gemini models
    """
    response = completion(
        model=model,
        messages=messages,
    )
    return response['choices'][0]['message']['content']

# =============================================================================
# PART 1: QUERY INTERPRETATION FOR RAG
# =============================================================================

def basic_query_interpreter(user_input: str) -> str:
    """
    Convert natural conversation to searchable queries for vector database
    
    Problem: Users say "Hello", "I'm having issues" but our vector DB needs
    specific search terms like "refund policy", "return process"
    """
    
    prompt = f"""
    Extract searchable terms from this user message for a knowledge base search.
    
    User message: "{user_input}"
    
    Examples:
    - "My order hasn't arrived and I'm frustrated" → "order tracking delivery status"
    - "I want to return my shoes" → "return policy product return process" 
    - "How do I contact support?" → "customer support contact information"
    
    Return only the search query, nothing else:
    """
    
    messages = [{"role": "user", "content": prompt}]
    response = get_llm_response(messages, model="gemini/gemini-1.5-flash")
    
    return response.strip()


# =============================================================================
# PART 2: STRUCTURED OUTPUTS WITH PYDANTIC
# =============================================================================

class SearchQuery(BaseModel):
    """Simple structured output for search queries"""
    original_message: str = Field(description="The user's original message")
    search_terms: str = Field(description="Extracted search terms for vector DB")
    intent_confidence: float = Field(description="Confidence in intent detection (0-1)")


def structured_query_interpreter(user_input: str) -> SearchQuery:
    """
    Same query interpretation but with structured output
    """
    
    prompt = f"""
    Analyze this user message and extract search information.
    
    User message: "{user_input}"
    
    You must respond with ONLY valid JSON in this exact format:
    {{
        "original_message": "exact user input here",
        "search_terms": "searchable keywords for knowledge base",
        "intent_confidence": 0.9
    }}
    
    Examples:
    {{"original_message": "My order is late", "search_terms": "order tracking delivery status", "intent_confidence": 0.9}}
    {{"original_message": "Hello", "search_terms": "general greeting help", "intent_confidence": 0.3}}
    
    Return only the JSON, no other text:
    """
    
    # Note: Gemini doesn't need explicit JSON mode, it responds well to JSON requests
    messages = [{"role": "user", "content": prompt}]
    response = get_llm_response(messages, model="gemini/gemini-1.5-flash")
    
    try:
        # Clean the response in case there are extra characters
        cleaned_response = response.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response.replace('```json', '').replace('```', '').strip()
        
        result = json.loads(cleaned_response)
        return SearchQuery(**result)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed. Response was: '{response}'")
        print(f"Error: {e}")
        raise


# =============================================================================
# PART 3: BUSINESS CLASSIFICATION
# =============================================================================

class BusinessRouting(BaseModel):
    """
    Business-focused classification for routing and decisions
    """
    category: Literal["sales", "support", "general"] = Field(
        description="Primary business category"
    )
    search_query: str = Field(
        description="Optimized search query for knowledge base"
    )
    priority: Literal["low", "medium", "high"] = Field(
        description="Urgency level for business routing"
    )
    suggested_actions: List[str] = Field(
        description="Recommended next steps for this request"
    )
    requires_human: bool = Field(
        description="Whether this needs human intervention"
    )


def business_classifier(user_input: str) -> BusinessRouting:
    """
    Classify user input for business routing and action planning
    """
    
    prompt = f"""
    Analyze this customer message for business routing and action planning.
    
    Customer message: "{user_input}"
    
    Categories:
    - sales: Product inquiries, pricing, purchasing, features
    - support: Issues, problems, complaints, returns, refunds  
    - general: Greetings, basic info, company questions
    
    Priority levels:
    - high: Angry customers, urgent issues, high-value sales
    - medium: Standard requests, normal inquiries
    - low: General questions, simple info requests
    
    You must respond with ONLY valid JSON in this exact format:
    {{
        "category": "sales|support|general",
        "search_query": "search terms for knowledge base",
        "priority": "low|medium|high", 
        "suggested_actions": ["action1", "action2"],
        "requires_human": true/false
    }}
    
    Return only the JSON, no other text:
    """
    
    # Note: Gemini doesn't need explicit JSON mode, it responds well to JSON requests
    messages = [{"role": "user", "content": prompt}]
    response = get_llm_response(messages, model="gemini/gemini-1.5-flash")
    
    try:
        # Clean the response in case there are extra characters
        cleaned_response = response.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response.replace('```json', '').replace('```', '').strip()
        
        result = json.loads(cleaned_response)
        return BusinessRouting(**result)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed. Response was: '{response}'")
        print(f"Error: {e}")
        raise


# =============================================================================
# PART 4: ADVANCED CLASSIFICATION
# =============================================================================

class CustomerSentiment(BaseModel):
    """Sentiment analysis for customer service"""
    sentiment: Literal["positive", "neutral", "negative", "frustrated", "angry"]
    confidence: float = Field(ge=0.0, le=1.0)
    emotional_indicators: List[str] = Field(description="Words/phrases indicating emotion")


class ProductMention(BaseModel):
    """Extract product mentions from customer messages"""
    product_name: str
    product_category: str
    action_mentioned: Literal["buy", "return", "complaint", "question", "none"]


class ComprehensiveAnalysis(BaseModel):
    """Complete customer message analysis"""
    routing: BusinessRouting
    sentiment: CustomerSentiment
    products_mentioned: List[ProductMention]
    estimated_response_time: str = Field(description="Suggested response timeframe")
    escalation_needed: bool


def comprehensive_classifier(user_input: str) -> ComprehensiveAnalysis:
    """
    Complete analysis combining all classification aspects
    """
    
    prompt = f"""
    Perform comprehensive analysis of this customer message:
    
    "{user_input}"
    
    Analyze for:
    1. Business routing (category, priority, actions needed)
    2. Customer sentiment and emotional state
    3. Any products mentioned and related actions
    4. Response timing and escalation needs
    
    Return complete JSON analysis:
    """
    
    # Note: Using gemini-1.5-pro for comprehensive analysis requiring complex reasoning
    messages = [{"role": "user", "content": prompt}]
    response = get_llm_response(messages, model="gemini/gemini-1.5-pro")
    
    result = json.loads(response)
    return ComprehensiveAnalysis(**result)


# =============================================================================
# PART 5: INTEGRATION WITH RAG PIPELINE
# =============================================================================

def enhanced_rag_pipeline(user_input: str):
    """
    Complete pipeline: Query Interpretation → RAG → Structured Response
    """
    
    # Step 1: Classify the request
    analysis = business_classifier(user_input)
    
    print(f"🔍 Analysis: {analysis.category} request, {analysis.priority} priority")
    print(f"📝 Search Query: {analysis.search_query}")
    
    # Step 2: Search knowledge base (placeholder - integrate with your RAG)
    # from your_rag_module import search_knowledge_base
    # rag_results = search_knowledge_base(analysis.search_query)
    
    # Step 3: Generate response with business context
    response_prompt = f"""
    Generate a response for this {analysis.category} request with {analysis.priority} priority.
    
    Original customer message: "{user_input}"
    Search query used: "{analysis.search_query}"
    Suggested actions: {analysis.suggested_actions}
    
    Guidelines:
    - {analysis.category} tone and approach
    - {analysis.priority} priority response
    - Include relevant information from knowledge base
    - {"Escalate to human if needed" if analysis.requires_human else "Handle automatically"}
    
    Response:
    """
    
    messages = [{"role": "user", "content": response_prompt}]
    response = get_llm_response(messages, model="gemini/gemini-1.5-flash")
    
    return {
        "classification": analysis,
        "response": response,
        "metadata": {
            "search_query": analysis.search_query,
            "requires_human": analysis.requires_human,
            "priority": analysis.priority
        }
    }


# =============================================================================
# PART 6: PRACTICAL EXAMPLES & TESTING
# =============================================================================

def run_examples():
    """
    Test the structured response system with various inputs
    """
    
    test_messages = [
        "My order hasn't arrived and I'm really frustrated!",
        "I want to return my shoes because they don't fit",
        "What's your refund policy?", 
        "Hello, I'm interested in your premium plan pricing",
        "I need help with setting up my account",
        "This product is terrible and I want my money back NOW!"
    ]
    
    print("=" * 60)
    print("STRUCTURED RESPONSE EXAMPLES")
    print("=" * 60)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🗣️  Example {i}: '{message}'")
        print("-" * 50)
        
        # Basic query interpretation
        search_query = basic_query_interpreter(message)
        print(f"🔍 Search Query: {search_query}")
        
        # Business classification
        classification = business_classifier(message)
        print(f"📊 Category: {classification.category}")
        print(f"⚡ Priority: {classification.priority}")
        print(f"🎯 Actions: {classification.suggested_actions}")
        print(f"👨‍💼 Needs Human: {classification.requires_human}")


def workshop_exercise():
    """
    Interactive exercise for workshop students
    """
    
    print("\n" + "=" * 60)
    print("WORKSHOP EXERCISE: Build Your Classifier")
    print("=" * 60)
    
    print("""
    Your turn! Try these tasks:
    
    1. Test the classifiers with your own customer messages
    2. Modify the BusinessRouting model to add your own categories
    3. Integrate with the RAG system from previous sessions
    4. Add custom business logic based on classification results
    
    Example integration:
    - Sales requests → Search product documentation  
    - Support requests → Search troubleshooting guides
    - General questions → Search FAQ database
    """)
    
    # Interactive testing
    while True:
        user_input = input("\n💬 Enter a test message (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
            
        try:
            result = enhanced_rag_pipeline(user_input)
            print(f"\n📋 Classification: {result['classification']}")
            print(f"💬 Response: {result['response']}")
            print(f"📊 Metadata: {result['metadata']}")
        except Exception as e:
            print(f"❌ Error: {e}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("🚀 Starting Structured Response Tutorial")
    
    # Run examples
    run_examples()
    
    # Show workshop instructions (interactive part commented out for demo)
    print("\n" + "=" * 60)
    print("WORKSHOP EXERCISE: Build Your Classifier")
    print("=" * 60)
    
    print("""
    Your turn! Try these tasks:
    
    1. Test the classifiers with your own customer messages
    2. Modify the BusinessRouting model to add your own categories
    3. Integrate with the RAG system from previous sessions
    4. Add custom business logic based on classification results
    
    Example integration:
    - Sales requests → Search product documentation  
    - Support requests → Search troubleshooting guides
    - General questions → Search FAQ database
    
    To test interactively, uncomment the workshop_exercise() call below
    """)
    
    # Uncomment this for interactive testing:
    # workshop_exercise()
    
    print("\n✅ Tutorial complete! You now have:")
    print("   - Query interpretation for better RAG")
    print("   - Structured business classification") 
    print("   - Integration patterns for real applications")
    print("   - Foundation for building intelligent agents")