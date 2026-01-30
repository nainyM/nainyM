"""
Data models for RecipeBox CLI application.
"""
from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4


@dataclass
class Ingredient:
    """Represents a single ingredient with its quantity."""
    name: str
    quantity: str

    def __str__(self) -> str:
        """String representation of ingredient."""
        return f"{self.name}: {self.quantity}"


@dataclass
class Recipe:
    """Represents a recipe with all its details."""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    ingredients: list[Ingredient] = field(default_factory=list)
    steps: str = ""
    favorite: bool = False
    category: Optional[str] = None

    def __str__(self) -> str:
        """String representation of recipe."""
        favorite_marker = "⭐" if self.favorite else ""
        category_str = f" [{self.category}]" if self.category else ""
        return f"{favorite_marker} {self.name}{category_str}"

    def to_dict(self) -> dict:
        """Convert Recipe to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": [
                {"name": ing.name, "quantity": ing.quantity}
                for ing in self.ingredients
            ],
            "steps": self.steps,
            "favorite": self.favorite,
            "category": self.category
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Recipe":
        """Create Recipe instance from dictionary (JSON deserialization)."""
        ingredients = [
            Ingredient(name=ing["name"], quantity=ing["quantity"])
            for ing in data.get("ingredients", [])
        ]
        return cls(
            id=data.get("id", str(uuid4())),
            name=data.get("name", ""),
            ingredients=ingredients,
            steps=data.get("steps", ""),
            favorite=data.get("favorite", False),
            category=data.get("category")
        )
