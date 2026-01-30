"""
Main entry point for RecipeBox CLI application.
Starts the command-line interface.
"""
import sys
from cli import RecipeBoxCLI


def main():
    """
    Main entry point for RecipeBox CLI.
    Initializes and starts the interactive command-line interface.
    """
    try:
        # Create and start the CLI
        cli = RecipeBoxCLI()
        cli.cmdloop()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nInterrupted. Exiting...\n")
        sys.exit(0)
    except Exception as e:
        # Handle unexpected errors
        print(f"\nError: An unexpected error occurred: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
