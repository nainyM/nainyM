"""
Storage layer for RecipeBox CLI application.
Handles persistence of recipes using JSON (with upgrade path to SQLite).
"""
import json
import os
import shutil
from pathlib import Path
from typing import List
from abc import ABC, abstractmethod

from models import Recipe


class StorageInterface(ABC):
    """Abstract base class for storage implementations."""
    
    @abstractmethod
    def load_recipes(self) -> List[Recipe]:
        """Load all recipes from storage."""
        pass
    
    @abstractmethod
    def save_recipes(self, recipes: List[Recipe]) -> None:
        """Save all recipes to storage."""
        pass


class JSONStorage(StorageInterface):
    """JSON-based storage implementation for recipes."""
    
    def __init__(self, file_path: str = "recipes.json"):
        """
        Initialize JSON storage.
        
        Args:
            file_path: Path to the JSON file for storing recipes
        """
        self.file_path = Path(file_path)
        self.temp_file_path = Path(f"{file_path}.tmp")
    
    def load_recipes(self) -> List[Recipe]:
        """
        Load recipes from JSON file.
        
        Returns:
            List of Recipe objects. Returns empty list if file doesn't exist
            or is corrupted.
        
        Raises:
            IOError: If file exists but cannot be read
        """
        # If file doesn't exist, return empty list
        if not self.file_path.exists():
            return []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both array format and wrapped format for flexibility
            if isinstance(data, dict) and "recipes" in data:
                recipes_data = data["recipes"]
            elif isinstance(data, list):
                recipes_data = data
            else:
                # Invalid format, return empty list
                return []
            
            # Convert dictionaries to Recipe objects
            recipes = []
            for recipe_dict in recipes_data:
                try:
                    recipe = Recipe.from_dict(recipe_dict)
                    recipes.append(recipe)
                except (KeyError, TypeError) as e:
                    # Skip corrupted recipe entries
                    print(f"Warning: Skipping invalid recipe entry: {e}")
                    continue
            
            return recipes
        
        except json.JSONDecodeError as e:
            # Corrupted JSON - try to restore from backup if available
            backup_path = Path(f"{self.file_path}.backup")
            if backup_path.exists():
                print(f"Warning: recipes.json is corrupted. Attempting to restore from backup...")
                try:
                    shutil.copy(backup_path, self.file_path)
                    return self.load_recipes()  # Retry loading
                except Exception:
                    print("Error: Could not restore from backup. Starting with empty recipe list.")
                    return []
            else:
                print(f"Warning: recipes.json is corrupted and no backup found. Starting with empty recipe list.")
                return []
        
        except IOError as e:
            raise IOError(f"Error reading recipes file: {e}")
    
    def save_recipes(self, recipes: List[Recipe]) -> None:
        """
        Save recipes to JSON file using atomic write.
        
        Uses atomic write pattern: write to temp file, then rename.
        Also creates a backup before overwriting.
        
        Args:
            recipes: List of Recipe objects to save
        
        Raises:
            IOError: If file cannot be written
        """
        try:
            # Create backup of existing file if it exists
            if self.file_path.exists():
                backup_path = Path(f"{self.file_path}.backup")
                try:
                    shutil.copy(self.file_path, backup_path)
                except Exception as e:
                    # Backup failure is not critical, continue anyway
                    print(f"Warning: Could not create backup: {e}")
            
            # Convert recipes to dictionaries
            recipes_data = [recipe.to_dict() for recipe in recipes]
            
            # Write to temporary file first (atomic write)
            with open(self.temp_file_path, 'w', encoding='utf-8') as f:
                json.dump(recipes_data, f, indent=2, ensure_ascii=False)
            
            # Atomic rename: temp file becomes the actual file
            self.temp_file_path.replace(self.file_path)
            
        except IOError as e:
            raise IOError(f"Error writing recipes file: {e}")
        except Exception as e:
            # If something goes wrong, try to restore from backup
            if self.file_path.exists() and Path(f"{self.file_path}.backup").exists():
                try:
                    shutil.copy(Path(f"{self.file_path}.backup"), self.file_path)
                    print("Error during save. Restored from backup.")
                except Exception:
                    pass
            raise


# Factory function for easy storage creation
def create_storage(storage_type: str = "json", file_path: str = "recipes.json") -> StorageInterface:
    """
    Factory function to create storage instance.
    
    Args:
        storage_type: Type of storage ("json" for now, "sqlite" for future)
        file_path: Path to storage file
    
    Returns:
        StorageInterface instance
    """
    if storage_type.lower() == "json":
        return JSONStorage(file_path)
    else:
        raise ValueError(f"Unsupported storage type: {storage_type}")
