
RecipeBox CLI

1. 🎯 Objective

Build a Python-based terminal application that allows users to:

Save and manage recipes

Mark favorite recipes

Search recipes easily

Auto-generate a shopping list from selected recipes

This is a single-user, offline CLI app (perfect for local use and learning).

2. 👤 Target User

Home cooks

Developers learning Python

Anyone who prefers terminal tools over apps

3. 🧩 Core Features (MVP)
3.1 Recipe Management

User can:

Add a recipe

View all recipes

View a single recipe in detail

Delete a recipe

Recipe data model:

- Recipe ID
- Name
- Ingredients (list with quantity)
- Steps / Instructions
- Category (optional: breakfast, dinner, etc.)
- Is Favorite (true/false)

3.2 Favorite Recipes

User can:

Mark / unmark a recipe as favorite

View only favorite recipes

3.3 Search Recipes

Search by:

Recipe name (partial match)

Ingredient name

Example:

Search recipe by ingredient: "tomato"

3.4 Shopping List Generator

User can:

Select one or multiple recipes

Generate a combined shopping list

Quantities should be aggregated if same ingredient appears multiple times

Example output:

Shopping List:
- Tomatoes: 4
- Onions: 2
- Olive Oil: 100 ml

4. 🖥️ User Experience (CLI Flow)
Main Menu
1. Add Recipe
2. View All Recipes
3. Search Recipe
4. View Favorite Recipes
5. Generate Shopping List
6. Delete Recipe
7. Exit

Example Add Recipe Flow
Enter recipe name:
Enter ingredients (comma separated):
Enter quantities (comma separated):
Enter steps:
Mark as favorite? (y/n):

5. 🏗️ Technical Requirements
5.1 Tech Stack

Language: Python 3

Storage:

JSON file (v1 – simplest)

Upgrade path: SQLite later

5.2 Data Storage Format (v1)

recipes.json

[
  {
    "id": 1,
    "name": "Pasta",
    "ingredients": [
      {"name": "Pasta", "quantity": "200g"},
      {"name": "Tomato", "quantity": "2"}
    ],
    "steps": "Boil pasta. Add sauce.",
    "favorite": true
  }
]

6. ⚙️ Functional Requirements
Feature	Requirement
Add Recipe	Validate inputs, no empty names
Search	Case-insensitive
Favorites	Toggle without deleting recipe
Shopping List	Merge duplicate ingredients
Persistence	Data must persist after restart
7. 🚫 Out of Scope (for now)

User login

Cloud sync

Images

Nutritional data

GUI / Web UI

8. 📦 Milestones (Suggested Build Order)
Phase 1 – Foundation

Project structure

JSON read/write

Add & view recipes

Phase 2 – Usability

Search

Favorites

Delete recipe

Phase 3 – Power Feature

Shopping list aggregation

9. 📁 Suggested Project Structure
recipe_cli/
│
├── main.py
├── recipe_manager.py
├── storage.py
├── models.py
├── recipes.json
└── utils.py