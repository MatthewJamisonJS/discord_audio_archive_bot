"""
Discord Audio Archive Bot

A hybrid Python/Node.js bot that automatically records Discord voice conversations
with professional-quality MP3 output.

This package provides a modern, well-structured interface to the bot's functionality
while maintaining backward compatibility with the existing codebase.
"""

__version__ = "0.1.0"
__author__ = "Audio Archive Bot Contributors"
__license__ = "MIT"

# Import main components from the package
try:
    from .voice_manager_hybrid import HybridVoiceManager
except ImportError:
    # Fallback: try importing from root-level module
    import sys
    from pathlib import Path

    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    from voice_manager_hybrid import HybridVoiceManager

__all__ = [
    "HybridVoiceManager",
    "__version__",
]
