"""
Command-line interface for RecipeBox CLI application.
Uses Python's cmd module for interactive command processing.
"""
import cmd
import sys
from typing import List, Optional

from models import Recipe, Ingredient
from recipes import RecipeManager
from shopping_list import ShoppingListGenerator


class RecipeBoxCLI(cmd.Cmd):
    """Interactive command-line interface for RecipeBox."""
    
    intro = """
╔═══════════════════════════════════════════════════════════╗
║                  RecipeBox CLI v1.0                       ║
║         Your Personal Recipe Management System            ║
╚═══════════════════════════════════════════════════════════╝

Type 'help' or '?' to see available commands.
Type 'menu' to see the main menu.
"""
    prompt = '(RecipeBox) '
    
    def __init__(self):
        """Initialize the CLI with RecipeManager."""
        super().__init__()
        self.manager = RecipeManager()
        self.shopping_list_gen = ShoppingListGenerator()
    
    def do_menu(self, arg):
        """Display the main menu."""
        print("\n" + "="*60)
        print("Main Menu")
        print("="*60)
        print("1. add          - Add a new recipe")
        print("2. list         - View all recipes")
        print("3. search       - Search recipes by name or ingredient")
        print("4. favorites    - View favorite recipes")
        print("5. shopping     - Generate shopping list from recipes")
        print("6. delete       - Delete a recipe")
        print("7. view         - View a recipe in detail")
        print("8. toggle       - Toggle favorite status of a recipe")
        print("9. exit/quit    - Exit the application")
        print("="*60 + "\n")
    
    def help_menu(self):
        """Help for menu command."""
        print("Display the main menu with all available commands.")
    
    def do_add(self, arg):
        """Add a new recipe."""
        print("\n" + "-"*60)
        print("Add New Recipe")
        print("-"*60)
        
        try:
            # Get recipe name
            name = input("Enter recipe name: ").strip()
            if not name:
                print("Error: Recipe name cannot be empty.")
                return
            
            # Get ingredients
            ingredients_str = input("Enter ingredients (comma separated): ").strip()
            quantities_str = input("Enter quantities (comma separated): ").strip()
            
            if not ingredients_str or not quantities_str:
                print("Error: Ingredients and quantities are required.")
                return
            
            # Parse ingredients and quantities
            ingredient_names = [ing.strip() for ing in ingredients_str.split(",")]
            quantities = [qty.strip() for qty in quantities_str.split(",")]
            
            # Ensure same number of ingredients and quantities
            if len(ingredient_names) != len(quantities):
                print("Error: Number of ingredients must match number of quantities.")
                return
            
            # Create Ingredient objects
            ingredients = [
                Ingredient(name=name, quantity=qty)
                for name, qty in zip(ingredient_names, quantities)
            ]
            
            # Get steps
            print("Enter cooking steps (press Enter twice when done, or type 'done' on a new line):")
            steps_lines = []
            while True:
                line = input()
                if line.strip().lower() == 'done' and steps_lines:
                    break
                if not line.strip() and steps_lines:
                    # Empty line after content means done
                    break
                steps_lines.append(line)
            steps = "\n".join(steps_lines).strip()
            
            # Get favorite status
            favorite_input = input("Mark as favorite? (y/n): ").strip().lower()
            favorite = favorite_input in ['y', 'yes']
            
            # Get category (optional)
            category = input("Enter category (optional, press Enter to skip): ").strip()
            category = category if category else None
            
            # Add recipe
            recipe = self.manager.add_recipe(
                name=name,
                ingredients=ingredients,
                steps=steps,
                favorite=favorite,
                category=category
            )
            
            print(f"\n✓ Recipe '{recipe.name}' added successfully!")
            print(f"  Recipe ID: {recipe.id}\n")
        
        except ValueError as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.\n")
        except Exception as e:
            print(f"Error: {e}\n")
    
    def help_add(self):
        """Help for add command."""
        print("Add a new recipe to your collection.")
        print("You will be prompted for:")
        print("  - Recipe name (required)")
        print("  - Ingredients (comma separated)")
        print("  - Quantities (comma separated)")
        print("  - Cooking steps")
        print("  - Favorite status (y/n)")
        print("  - Category (optional)")
    
    def do_list(self, arg):
        """View all recipes."""
        recipes = self.manager.get_all_recipes()
        
        if not recipes:
            print("\nNo recipes found. Add some recipes to get started!\n")
            return
        
        print("\n" + "="*60)
        print(f"All Recipes ({len(recipes)} total)")
        print("="*60)
        
        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe}")
        
        print("="*60 + "\n")
    
    def help_list(self):
        """Help for list command."""
        print("Display all recipes in your collection.")
    
    def do_view(self, arg):
        """View a recipe in detail by ID or index."""
        if not arg:
            print("Error: Please provide a recipe ID or index.")
            print("Usage: view <recipe_id> or view <index>")
            return
        
        recipes = self.manager.get_all_recipes()
        
        if not recipes:
            print("\nNo recipes found.\n")
            return
        
        # Try to find by index first (if it's a number)
        try:
            index = int(arg) - 1
            if 0 <= index < len(recipes):
                recipe = recipes[index]
            else:
                print(f"Error: Invalid index. Please use 1-{len(recipes)}")
                return
        except ValueError:
            # Not a number, try as ID
            recipe = self.manager.get_recipe_by_id(arg)
            if not recipe:
                print(f"Error: Recipe with ID '{arg}' not found.")
                return
        
        # Display recipe details
        print("\n" + "="*60)
        print(f"Recipe: {recipe.name}")
        print("="*60)
        print(f"ID: {recipe.id}")
        if recipe.category:
            print(f"Category: {recipe.category}")
        print(f"Favorite: {'Yes ⭐' if recipe.favorite else 'No'}")
        print("\nIngredients:")
        for ingredient in recipe.ingredients:
            print(f"  - {ingredient}")
        print("\nSteps:")
        print(f"  {recipe.steps.replace(chr(10), chr(10) + '  ')}")
        print("="*60 + "\n")
    
    def help_view(self):
        """Help for view command."""
        print("View a recipe in detail.")
        print("Usage: view <recipe_id> or view <index>")
        print("Example: view 1  (views first recipe from list)")
        print("Example: view abc123  (views recipe with ID abc123)")
    
    def do_search(self, arg):
        """Search recipes by name or ingredient."""
        if not arg:
            search_term = input("Enter search term: ").strip()
        else:
            search_term = arg
        
        if not search_term:
            print("Error: Search term cannot be empty.")
            return
        
        results = self.manager.search_recipes(search_term)
        
        if not results:
            print(f"\nNo recipes found matching '{search_term}'.\n")
            return
        
        print("\n" + "="*60)
        print(f"Search Results for '{search_term}' ({len(results)} found)")
        print("="*60)
        
        for i, recipe in enumerate(results, 1):
            print(f"{i}. {recipe}")
        
        print("="*60 + "\n")
    
    def help_search(self):
        """Help for search command."""
        print("Search recipes by name or ingredient (case-insensitive).")
        print("Usage: search <term>")
        print("Example: search tomato")
        print("If no term is provided, you will be prompted.")
    
    def do_favorites(self, arg):
        """View favorite recipes."""
        favorites = self.manager.get_favorite_recipes()
        
        if not favorites:
            print("\nNo favorite recipes found.\n")
            return
        
        print("\n" + "="*60)
        print(f"Favorite Recipes ({len(favorites)} total)")
        print("="*60)
        
        for i, recipe in enumerate(favorites, 1):
            print(f"{i}. {recipe}")
        
        print("="*60 + "\n")
    
    def help_favorites(self):
        """Help for favorites command."""
        print("Display all recipes marked as favorites.")
    
    def do_toggle(self, arg):
        """Toggle favorite status of a recipe."""
        if not arg:
            print("Error: Please provide a recipe ID or index.")
            print("Usage: toggle <recipe_id> or toggle <index>")
            return
        
        recipes = self.manager.get_all_recipes()
        
        if not recipes:
            print("\nNo recipes found.\n")
            return
        
        # Try to find by index first
        try:
            index = int(arg) - 1
            if 0 <= index < len(recipes):
                recipe = recipes[index]
            else:
                print(f"Error: Invalid index. Please use 1-{len(recipes)}")
                return
        except ValueError:
            # Not a number, try as ID
            recipe = self.manager.get_recipe_by_id(arg)
            if not recipe:
                print(f"Error: Recipe with ID '{arg}' not found.")
                return
        
        new_status = self.manager.toggle_favorite(recipe.id)
        status_str = "marked as favorite ⭐" if new_status else "unmarked as favorite"
        print(f"\n✓ Recipe '{recipe.name}' {status_str}.\n")
    
    def help_toggle(self):
        """Help for toggle command."""
        print("Toggle the favorite status of a recipe.")
        print("Usage: toggle <recipe_id> or toggle <index>")
    
    def do_shopping(self, arg):
        """Generate shopping list from selected recipes."""
        recipes = self.manager.get_all_recipes()
        
        if not recipes:
            print("\nNo recipes found. Add some recipes first!\n")
            return
        
        print("\n" + "="*60)
        print("Available Recipes:")
        print("="*60)
        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe}")
        print("="*60)
        
        recipe_input = input("\nEnter recipe numbers (comma separated, e.g., 1,3,5): ").strip()
        
        if not recipe_input:
            print("Error: No recipes selected.\n")
            return
        
        try:
            # Parse selected recipe indices
            indices = [int(x.strip()) - 1 for x in recipe_input.split(",")]
            selected_recipes = []
            
            for idx in indices:
                if 0 <= idx < len(recipes):
                    selected_recipes.append(recipes[idx])
                else:
                    print(f"Warning: Index {idx + 1} is out of range. Skipping.")
            
            if not selected_recipes:
                print("Error: No valid recipes selected.\n")
                return
            
            # Generate shopping list
            shopping_list = self.shopping_list_gen.generate(selected_recipes)
            formatted_list = self.shopping_list_gen.format(shopping_list)
            
            print("\n" + formatted_list + "\n")
        
        except ValueError:
            print("Error: Invalid input. Please enter numbers separated by commas.\n")
        except Exception as e:
            print(f"Error: {e}\n")
    
    def help_shopping(self):
        """Help for shopping command."""
        print("Generate a combined shopping list from selected recipes.")
        print("You will be prompted to select recipes by their numbers.")
        print("Quantities for duplicate ingredients will be aggregated.")
    
    def do_delete(self, arg):
        """Delete a recipe."""
        if not arg:
            print("Error: Please provide a recipe ID or index.")
            print("Usage: delete <recipe_id> or delete <index>")
            return
        
        recipes = self.manager.get_all_recipes()
        
        if not recipes:
            print("\nNo recipes found.\n")
            return
        
        # Try to find by index first
        try:
            index = int(arg) - 1
            if 0 <= index < len(recipes):
                recipe = recipes[index]
            else:
                print(f"Error: Invalid index. Please use 1-{len(recipes)}")
                return
        except ValueError:
            # Not a number, try as ID
            recipe = self.manager.get_recipe_by_id(arg)
            if not recipe:
                print(f"Error: Recipe with ID '{arg}' not found.")
                return
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete '{recipe.name}'? (y/n): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            if self.manager.delete_recipe(recipe.id):
                print(f"\n✓ Recipe '{recipe.name}' deleted successfully.\n")
            else:
                print(f"\nError: Failed to delete recipe.\n")
        else:
            print("\nDeletion cancelled.\n")
    
    def help_delete(self):
        """Help for delete command."""
        print("Delete a recipe from your collection.")
        print("Usage: delete <recipe_id> or delete <index>")
        print("You will be asked to confirm before deletion.")
    
    def do_exit(self, arg):
        """Exit the application."""
        print("\nThank you for using RecipeBox CLI. Goodbye!\n")
        return True
    
    def help_exit(self):
        """Help for exit command."""
        print("Exit the RecipeBox CLI application.")
    
    def do_quit(self, arg):
        """Exit the application (alias for exit)."""
        return self.do_exit(arg)
    
    def help_quit(self):
        """Help for quit command."""
        print("Exit the RecipeBox CLI application (alias for 'exit').")
    
    def do_EOF(self, arg):
        """Handle EOF (Ctrl+D) to exit gracefully."""
        print()
        return self.do_exit(arg)
    
    def default(self, line):
        """Handle unknown commands."""
        print(f"Unknown command: {line}")
        print("Type 'help' or 'menu' to see available commands.")
    
    def emptyline(self):
        """Handle empty line input."""
        # Do nothing on empty line (don't repeat last command)
        pass


def main():
    """Main entry point for the CLI."""
    cli = RecipeBoxCLI()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Exiting...\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
