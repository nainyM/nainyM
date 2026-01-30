"""
RecipeManager class for RecipeBox CLI application.
Handles all CRUD operations and business logic for recipe management.
"""
from typing import List, Optional, Dict
from collections import Counter

from models import Recipe, Ingredient
from storage import StorageInterface, create_storage


class RecipeManager:
    """Manages recipes with full CRUD operations."""
    
    def __init__(self, storage: Optional[StorageInterface] = None):
        """
        Initialize RecipeManager.
        
        Args:
            storage: StorageInterface instance. If None, creates default JSON storage.
        """
        self.storage = storage or create_storage()
        self._recipes: List[Recipe] = []
        self._load_recipes()
    
    def _load_recipes(self) -> None:
        """Load recipes from storage into memory."""
        try:
            self._recipes = self.storage.load_recipes()
        except Exception as e:
            print(f"Error loading recipes: {e}")
            self._recipes = []
    
    def _save_recipes(self) -> None:
        """Save recipes to storage."""
        try:
            self.storage.save_recipes(self._recipes)
        except Exception as e:
            raise RuntimeError(f"Error saving recipes: {e}")
    
    # CREATE operations
    def add_recipe(
        self,
        name: str,
        ingredients: List[Ingredient],
        steps: str,
        favorite: bool = False,
        category: Optional[str] = None
    ) -> Recipe:
        """
        Add a new recipe.
        
        Args:
            name: Recipe name (must not be empty)
            ingredients: List of Ingredient objects
            steps: Cooking instructions
            favorite: Whether recipe is marked as favorite
            category: Optional category (e.g., "breakfast", "dinner")
        
        Returns:
            The created Recipe object
        
        Raises:
            ValueError: If name is empty
        """
        # Validate inputs - no empty names
        if not name or not name.strip():
            raise ValueError("Recipe name cannot be empty")
        
        # Create new recipe
        recipe = Recipe(
            name=name.strip(),
            ingredients=ingredients,
            steps=steps,
            favorite=favorite,
            category=category.strip() if category else None
        )
        
        self._recipes.append(recipe)
        self._save_recipes()
        
        return recipe
    
    # READ operations
    def get_all_recipes(self) -> List[Recipe]:
        """
        Get all recipes.
        
        Returns:
            List of all Recipe objects
        """
        return self._recipes.copy()
    
    def get_recipe_by_id(self, recipe_id: str) -> Optional[Recipe]:
        """
        Get a single recipe by ID.
        
        Args:
            recipe_id: Unique recipe identifier
        
        Returns:
            Recipe object if found, None otherwise
        """
        for recipe in self._recipes:
            if recipe.id == recipe_id:
                return recipe
        return None
    
    def get_favorite_recipes(self) -> List[Recipe]:
        """
        Get all favorite recipes.
        
        Returns:
            List of Recipe objects marked as favorite
        """
        return [recipe for recipe in self._recipes if recipe.favorite]
    
    def search_recipes(self, search_term: str) -> List[Recipe]:
        """
        Search recipes by name or ingredient (case-insensitive, partial match).
        
        Args:
            search_term: Search query (recipe name or ingredient name)
        
        Returns:
            List of Recipe objects matching the search term
        """
        if not search_term:
            return []
        
        search_term_lower = search_term.lower().strip()
        matching_recipes = []
        
        for recipe in self._recipes:
            # Search by recipe name (case-insensitive, partial match)
            if search_term_lower in recipe.name.lower():
                matching_recipes.append(recipe)
                continue
            
            # Search by ingredient name (case-insensitive, partial match)
            for ingredient in recipe.ingredients:
                if search_term_lower in ingredient.name.lower():
                    matching_recipes.append(recipe)
                    break  # Avoid duplicates if multiple ingredients match
        
        return matching_recipes
    
    # UPDATE operations
    def toggle_favorite(self, recipe_id: str) -> bool:
        """
        Toggle favorite status of a recipe.
        
        Args:
            recipe_id: Unique recipe identifier
        
        Returns:
            New favorite status (True if now favorite, False otherwise)
        
        Raises:
            ValueError: If recipe not found
        """
        recipe = self.get_recipe_by_id(recipe_id)
        if recipe is None:
            raise ValueError(f"Recipe with ID '{recipe_id}' not found")
        
        recipe.favorite = not recipe.favorite
        self._save_recipes()
        
        return recipe.favorite
    
    def update_recipe(
        self,
        recipe_id: str,
        name: Optional[str] = None,
        ingredients: Optional[List[Ingredient]] = None,
        steps: Optional[str] = None,
        favorite: Optional[bool] = None,
        category: Optional[str] = None
    ) -> Recipe:
        """
        Update a recipe's fields.
        
        Args:
            recipe_id: Unique recipe identifier
            name: New recipe name (if provided)
            ingredients: New ingredients list (if provided)
            steps: New cooking instructions (if provided)
            favorite: New favorite status (if provided)
            category: New category (if provided)
        
        Returns:
            Updated Recipe object
        
        Raises:
            ValueError: If recipe not found or name is empty
        """
        recipe = self.get_recipe_by_id(recipe_id)
        if recipe is None:
            raise ValueError(f"Recipe with ID '{recipe_id}' not found")
        
        if name is not None:
            if not name.strip():
                raise ValueError("Recipe name cannot be empty")
            recipe.name = name.strip()
        
        if ingredients is not None:
            recipe.ingredients = ingredients
        
        if steps is not None:
            recipe.steps = steps
        
        if favorite is not None:
            recipe.favorite = favorite
        
        if category is not None:
            recipe.category = category.strip() if category else None
        
        self._save_recipes()
        
        return recipe
    
    # DELETE operations
    def delete_recipe(self, recipe_id: str) -> bool:
        """
        Delete a recipe.
        
        Args:
            recipe_id: Unique recipe identifier
        
        Returns:
            True if recipe was deleted, False if not found
        """
        for i, recipe in enumerate(self._recipes):
            if recipe.id == recipe_id:
                del self._recipes[i]
                self._save_recipes()
                return True
        return False
    
    # Shopping List operations
    def generate_shopping_list(self, recipe_ids: List[str]) -> Dict[str, List[str]]:
        """
        Generate a combined shopping list from selected recipes.
        Aggregates quantities for duplicate ingredients.
        
        Args:
            recipe_ids: List of recipe IDs to include in shopping list
        
        Returns:
            Dictionary mapping ingredient names to lists of quantities.
            Format: {"ingredient_name": ["quantity1", "quantity2", ...]}
        
        Example:
            {
                "Tomato": ["2", "200g"],
                "Onion": ["1", "1"],
                "Olive Oil": ["100 ml"]
            }
        """
        shopping_list: Dict[str, List[str]] = {}
        
        for recipe_id in recipe_ids:
            recipe = self.get_recipe_by_id(recipe_id)
            if recipe is None:
                continue  # Skip invalid recipe IDs
            
            for ingredient in recipe.ingredients:
                ingredient_name = ingredient.name
                if ingredient_name not in shopping_list:
                    shopping_list[ingredient_name] = []
                shopping_list[ingredient_name].append(ingredient.quantity)
        
        return shopping_list
    
    def format_shopping_list(self, shopping_list: Dict[str, List[str]]) -> str:
        """
        Format shopping list as a readable string.
        
        Args:
            shopping_list: Dictionary from generate_shopping_list()
        
        Returns:
            Formatted string representation of shopping list
        """
        if not shopping_list:
            return "Shopping List:\n(empty)"
        
        lines = ["Shopping List:"]
        for ingredient_name, quantities in sorted(shopping_list.items()):
            # For MVP: simple concatenation of quantities
            # Future: could parse and aggregate units
            quantities_str = ", ".join(quantities)
            lines.append(f"- {ingredient_name}: {quantities_str}")
        
        return "\n".join(lines)
    
    # Utility methods
    def get_recipe_count(self) -> int:
        """Get total number of recipes."""
        return len(self._recipes)
    
    def get_favorite_count(self) -> int:
        """Get number of favorite recipes."""
        return len(self.get_favorite_recipes())
    
    def recipe_exists(self, recipe_id: str) -> bool:
        """Check if a recipe with given ID exists."""
        return self.get_recipe_by_id(recipe_id) is not None
