"""
category_detector.py

Detects product category from a query using keyword matching.
"""

def detect_category(query: str) -> str:
    """
    Detect category based on keywords.

    Args:
        query (str): User input text

    Returns:
        str: 'cement', 'steel', 'aggregates', or 'unknown'
    """

    if not query:
        return "unknown"

    query_lower = query.lower()

    # Keyword groups
    cement_keywords = [
        "cement", "concrete", "portland", "mortar", "mix"
    ]

    steel_keywords = [
        "steel", "iron", "rebar", "bar", "tensile", "metal"
    ]

    aggregates_keywords = [
        "aggregate", "sand", "stone", "gravel", "crushed", "rock"
    ]

    # Match priority (important)
    for keyword in cement_keywords:
        if keyword in query_lower:
            return "cement"

    for keyword in steel_keywords:
        if keyword in query_lower:
            return "steel"

    for keyword in aggregates_keywords:
        if keyword in query_lower:
            return "aggregates"

    return "unknown"