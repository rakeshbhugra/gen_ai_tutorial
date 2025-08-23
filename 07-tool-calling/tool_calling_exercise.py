# LiteLLM Tool Calling Exercise - 3 New Functions and Test Queries

def calculate_tip(bill_amount: float, tip_percentage: float = 15.0) -> dict:
    """Calculate tip amount and total bill with tip
    
    Parameters
    ----------
    bill_amount : float
        The original bill amount
    tip_percentage : float
        The tip percentage (default 15.0)
    
    Returns
    -------
    dict
        Dictionary with tip_amount, total_amount, and tip_percentage
    """
    tip_amount = (bill_amount * tip_percentage) / 100
    total_amount = bill_amount + tip_amount
    
    return {
        "tip_amount": round(tip_amount, 2),
        "total_amount": round(total_amount, 2),
        "tip_percentage": tip_percentage
    }

def check_password_strength(password: str) -> dict:
    """Check the strength of a password and provide feedback
    
    Parameters
    ----------
    password : str
        The password to analyze
    
    Returns
    -------
    dict
        Dictionary with strength score, level, and suggestions
    """
    import re
    
    score = 0
    suggestions = []
    
    if len(password) >= 8:
        score += 2
    else:
        suggestions.append("Use at least 8 characters")
    
    if re.search(r'[a-z]', password):
        score += 1
    else:
        suggestions.append("Add lowercase letters")
    
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        suggestions.append("Add uppercase letters")
    
    if re.search(r'[0-9]', password):
        score += 1
    else:
        suggestions.append("Add numbers")
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 2
    else:
        suggestions.append("Add special characters")
    
    if score <= 2:
        level = "Weak"
    elif score <= 4:
        level = "Medium"
    else:
        level = "Strong"
    
    return {
        "score": score,
        "level": level,
        "suggestions": suggestions
    }

def calculate_bmi(weight: float, height: float, unit_system: str = "metric") -> dict:
    """Calculate Body Mass Index and provide health category
    
    Parameters
    ----------
    weight : float
        Weight (kg for metric, lbs for imperial)
    height : float
        Height (cm for metric, inches for imperial)
    unit_system : str {'metric', 'imperial'}
        Unit system to use (default 'metric')
    
    Returns
    -------
    dict
        Dictionary with BMI value, category, and unit system used
    """
    if unit_system == "imperial":
        # Convert to metric: lbs to kg, inches to meters
        weight_kg = weight * 0.453592
        height_m = (height * 2.54) / 100
    else:
        # Metric: kg and cm to meters
        weight_kg = weight
        height_m = height / 100
    
    bmi = weight_kg / (height_m ** 2)
    bmi = round(bmi, 1)
    
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    return {
        "bmi": bmi,
        "category": category,
        "unit_system": unit_system
    }

# Test Queries to Try:

"""
TIP CALCULATOR QUERIES:
- "Calculate the tip for a $85 bill with 20% tip"
- "What's the total for a $42.50 bill with standard tip?"
- "I have a $120 dinner bill, what should I tip 18%?"

PASSWORD STRENGTH QUERIES:
- "Check the strength of password 'hello123'"
- "How strong is the password 'MyP@ssw0rd2024'?"
- "Analyze password 'abc' and tell me how to improve it"

BMI CALCULATOR QUERIES:
- "Calculate BMI for 70kg weight and 175cm height"
- "What's my BMI if I weigh 150 lbs and I'm 5 feet 8 inches tall?"
- "Calculate BMI for 65kg and 160cm, what category am I in?"

COMPLEX QUERIES (multiple tools):
- "Check if 'MyTip20%' is a strong password, then calculate tip for $50 with 20%"
- "Calculate my BMI for 80kg and 180cm, then check password strength of 'Healthy123!'"
"""