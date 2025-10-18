#!/usr/bin/env python3
"""
Command-line interface for the Audio Archive Bot.
"""

import sys
import os
import logging
from pathlib import Path

def main():
    """Main entry point for the audio archive bot CLI."""
    try:
        # Add the project root to the path so we can import the root-level hybrid_bot.py
        # This allows the package to work with the existing code structure
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))

        # Load environment variables first
        from dotenv import load_dotenv
        load_dotenv()

        # Validate required configuration
        DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
        if not DISCORD_TOKEN:
            print("Error: Missing required environment variable: DISCORD_TOKEN")
            print("Please configure your .env file with Discord credentials")
            print("\nExample .env file:")
            print("  DISCORD_TOKEN=your_bot_token_here")
            print("  TARGET_USER_ID=user_id_to_monitor")
            sys.exit(1)

        TARGET_USER_ID = os.getenv('TARGET_USER_ID')
        if not TARGET_USER_ID:
            print("Error: Missing required environment variable: TARGET_USER_ID")
            print("Please configure your .env file with the user ID to monitor")
            sys.exit(1)

        # Import and run the existing hybrid_bot
        # The hybrid_bot module will initialize itself when imported
        import hybrid_bot

        print("Starting Audio Archive Bot...")
        print(f"Monitoring user ID: {TARGET_USER_ID}")

        # Run the bot - the logger is already configured in hybrid_bot.py
        hybrid_bot.bot.run(DISCORD_TOKEN)

    except KeyboardInterrupt:
        print("\nBot stopped by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        print(f"\nFatal error: {e}")
        print("Check hybrid_bot.log for details")
        sys.exit(1)

if __name__ == "__main__":
    main()
