import json
from google import genai
from google.genai import types
import config

def get_budget_insights(summary_data: dict, recent_transactions: list) -> str:
    """Uses Gemini to provide actionable financial coaching based on spending patterns."""
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    prompt = f"""
    Analyze the following monthly budget context:
    - Monthly Income: ${summary_data['monthly_income']:.2f}
    - Total Spent: ${summary_data['total_expenses']:.2f}
    - Remaining Funds: ${summary_data['remaining_budget']:.2f}
    - Savings Rate: {summary_data['savings_rate']:.1f}%
    - Category Breakdown: {summary_data['category_breakdown']}
    - Recent Transactions: {recent_transactions[:10]}

    Provide:
    1. A 2-sentence executive summary of financial health.
    2. 3 concrete, high-impact spending reduction recommendations.
    3. An actionable optimization strategy aligned with the 50/30/20 budget framework.
    Keep the tone encouraging, concise, and realistic.
    """

    response = client.models.generate_content(
        model=config.MODEL_NAME,
        contents=prompt
    )
    return response.text

def get_smart_purchase_advice(item_name: str, item_cost: float, summary_data: dict) -> dict:
    """Evaluates whether a planned purchase fits within the user's budget."""
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    system_instruction = """
    You are PocketSmart AI, a prudent financial advisor. Analyze a purchase decision given a user's budget.
    Return JSON strictly adhering to this schema:
    {
      "recommendation": "BUY", "WAIT", or "PASS",
      "impact_analysis": "Explanation of how this purchase affects monthly savings and cash flow",
      "alternative_suggestion": "A cost-saving alternative or waiting strategy"
    }
    """

    prompt = f"""
    Purchase Item: '{item_name}'
    Item Cost: ${item_cost:.2f}
    Monthly Income: ${summary_data['monthly_income']:.2f}
    Remaining Monthly Budget: ${summary_data['remaining_budget']:.2f}
    """

    response = client.models.generate_content(
        model=config.MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            temperature=0.3
        )
    )
    return json.loads(response.text)