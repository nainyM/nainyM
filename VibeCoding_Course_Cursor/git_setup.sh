#!/bin/bash
# Git setup script for RecipeBox CLI project

# Initialize git repository
git init

# Add all files (respecting .gitignore)
git add .

# Commit with specified message
git commit -m "Initial commit – VIBECODING_COURSE_CURSR"

# Add remote repository (adjust URL if needed)
# Assuming the repository is: https://github.com/nainyM/VIBECODING_COURSE_CURSR
git remote add origin https://github.com/nainyM/VIBECODING_COURSE_CURSR.git

# Rename branch to main if needed
git branch -M main

# Push to main branch
git push -u origin main
