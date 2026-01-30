"""
Shopping List Generator for RecipeBox CLI application.
Combines ingredients from multiple recipes and aggregates quantities.
"""
from typing import List, Dict
from collections import defaultdict

from models import Recipe, Ingredient


class ShoppingListGenerator:
    """Generates combined shopping lists from multiple recipes."""
    
    def __init__(self):
        """Initialize the shopping list generator."""
        pass
    
    def generate(self, recipes: List[Recipe]) -> Dict[str, List[str]]:
        """
        Generate a shopping list from multiple recipes.
        Aggregates quantities for duplicate ingredients.
        
        Args:
            recipes: List of Recipe objects to include in shopping list
        
        Returns:
            Dictionary mapping normalized ingredient names to lists of quantities.
            Format: {"ingredient_name": ["quantity1", "quantity2", ...]}
        
        Example:
            {
                "tomato": ["2", "200g"],
                "onion": ["1", "1"],
                "olive oil": ["100 ml"]
            }
        """
        shopping_list: Dict[str, List[str]] = defaultdict(list)
        
        for recipe in recipes:
            for ingredient in recipe.ingredients:
                # Normalize ingredient name (lowercase, strip whitespace)
                normalized_name = self._normalize_ingredient_name(ingredient.name)
                shopping_list[normalized_name].append(ingredient.quantity)
        
        return dict(shopping_list)
    
    def _normalize_ingredient_name(self, name: str) -> str:
        """
        Normalize ingredient name for aggregation.
        Case-insensitive matching, strips whitespace.
        
        Args:
            name: Ingredient name to normalize
        
        Returns:
            Normalized ingredient name (lowercase, stripped)
        """
        return name.lower().strip()
    
    def format(self, shopping_list: Dict[str, List[str]], 
               preserve_case: bool = False) -> str:
        """
        Format shopping list as a readable string.
        
        Args:
            shopping_list: Dictionary from generate() method
            preserve_case: If True, uses original case from first occurrence.
                          If False, capitalizes first letter of each word.
        
        Returns:
            Formatted string representation of shopping list
        
        Example output:
            Shopping List:
            - Tomatoes: 2, 200g
            - Onions: 1, 1
            - Olive Oil: 100 ml
        """
        if not shopping_list:
            return "Shopping List:\n(empty)"
        
        lines = ["Shopping List:"]
        
        # Sort ingredients alphabetically for consistent output
        for normalized_name, quantities in sorted(shopping_list.items()):
            # Format ingredient name
            if preserve_case:
                # Use original case (would need to track this separately)
                display_name = normalized_name.title()
            else:
                # Capitalize first letter of each word
                display_name = normalized_name.title()
            
            # Combine quantities (MVP: simple concatenation)
            quantities_str = ", ".join(quantities)
            lines.append(f"- {display_name}: {quantities_str}")
        
        return "\n".join(lines)
    
    def aggregate_quantities(self, shopping_list: Dict[str, List[str]]) -> Dict[str, str]:
        """
        Aggregate quantities for each ingredient (MVP version).
        For MVP, this simply combines quantities as strings.
        
        Future: Could parse and convert units (e.g., "2" + "200g" = "2 + 200g")
        
        Args:
            shopping_list: Dictionary from generate() method
        
        Returns:
            Dictionary mapping ingredient names to aggregated quantity strings
        
        Example:
            {
                "tomato": "2, 200g",
                "onion": "1, 1",
                "olive oil": "100 ml"
            }
        """
        aggregated = {}
        for ingredient_name, quantities in shopping_list.items():
            # MVP: Simple concatenation
            aggregated[ingredient_name] = ", ".join(quantities)
        
        return aggregated
    
    def get_ingredient_count(self, shopping_list: Dict[str, List[str]]) -> int:
        """
        Get total number of unique ingredients in shopping list.
        
        Args:
            shopping_list: Dictionary from generate() method
        
        Returns:
            Number of unique ingredients
        """
        return len(shopping_list)
    
    def get_total_items(self, shopping_list: Dict[str, List[str]]) -> int:
        """
        Get total number of ingredient items (including duplicates from different recipes).
        
        Args:
            shopping_list: Dictionary from generate() method
        
        Returns:
            Total number of ingredient entries
        """
        return sum(len(quantities) for quantities in shopping_list.values())


def generate_shopping_list(recipes: List[Recipe]) -> str:
    """
    Convenience function to generate and format a shopping list from recipes.
    
    Args:
        recipes: List of Recipe objects
    
    Returns:
        Formatted shopping list string
    """
    generator = ShoppingListGenerator()
    shopping_list = generator.generate(recipes)
    return generator.format(shopping_list)


def generate_shopping_list_dict(recipes: List[Recipe]) -> Dict[str, List[str]]:
    """
    Convenience function to generate shopping list as dictionary.
    
    Args:
        recipes: List of Recipe objects
    
    Returns:
        Dictionary mapping ingredient names to quantity lists
    """
    generator = ShoppingListGenerator()
    return generator.generate(recipes)
