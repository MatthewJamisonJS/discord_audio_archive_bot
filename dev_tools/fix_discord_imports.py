#!/usr/bin/env python3
"""
Discord Import Fix Script
========================

Automatically detects and fixes common Discord module installation issues.
This script resolves conflicts between py-cord and pycord packages.

Usage: python fix_discord_imports.py
"""

import subprocess
import sys
import importlib.util

def run_command(command):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_package_installed(package_name):
    """Check if a Python package is installed."""
    try:
        spec = importlib.util.find_spec(package_name)
        return spec is not None
    except ImportError:
        return False

def get_installed_packages():
    """Get list of installed packages."""
    success, stdout, _ = run_command("pip list")
    if success:
        packages = []
        for line in stdout.split('\n')[2:]:  # Skip header lines
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    packages.append((parts[0].lower(), parts[1]))
        return packages
    return []

def main():
    print("🔧 Discord Import Fix Script")
    print("=" * 40)
    print()

    # Check current state
    print("📋 Checking current Discord installation...")

    installed_packages = get_installed_packages()
    has_pycord = any(pkg[0] == 'pycord' for pkg in installed_packages)
    has_py_cord = any(pkg[0] == 'py-cord' for pkg in installed_packages)

    print(f"   py-cord installed: {'✅ Yes' if has_py_cord else '❌ No'}")
    print(f"   pycord installed: {'⚠️ Yes (CONFLICT!)' if has_pycord else '✅ No'}")

    # Test Discord import
    print("\n🧪 Testing Discord import...")
    discord_works = check_package_installed('discord')
    print(f"   Discord module accessible: {'✅ Yes' if discord_works else '❌ No'}")

    if discord_works:
        try:
            import discord
            print(f"   Discord version: {discord.__version__}")
        except:
            print("   Discord version: Unknown")

    print()

    # Determine what needs to be fixed
    needs_fix = False

    if has_pycord and has_py_cord:
        print("🚨 ISSUE: Both 'pycord' and 'py-cord' are installed!")
        print("   This causes import conflicts. Need to remove 'pycord'.")
        needs_fix = True
    elif has_pycord and not has_py_cord:
        print("🚨 ISSUE: Only 'pycord' is installed!")
        print("   Need to install 'py-cord' for this project.")
        needs_fix = True
    elif not has_py_cord and not has_pycord:
        print("🚨 ISSUE: No Discord library installed!")
        print("   Need to install 'py-cord'.")
        needs_fix = True
    elif has_py_cord and not discord_works:
        print("🚨 ISSUE: py-cord installed but Discord import fails!")
        print("   There may be a Python path issue.")
        needs_fix = True

    if not needs_fix and discord_works:
        print("✅ SUCCESS: Discord installation is working correctly!")
        print("   No fixes needed.")
        return

    print("\n🔧 Applying fixes...")

    # Fix 1: Remove conflicting pycord package
    if has_pycord:
        print("   Removing conflicting 'pycord' package...")
        success, stdout, stderr = run_command("pip uninstall pycord -y")
        if success:
            print("   ✅ Successfully removed 'pycord'")
        else:
            print(f"   ❌ Failed to remove 'pycord': {stderr}")
            return

    # Fix 2: Install py-cord if not present
    if not has_py_cord:
        print("   Installing 'py-cord' package...")
        success, stdout, stderr = run_command("pip install py-cord==2.4.1")
        if success:
            print("   ✅ Successfully installed 'py-cord'")
        else:
            print(f"   ❌ Failed to install 'py-cord': {stderr}")
            return

    # Fix 3: Test the fix
    print("\n🧪 Testing fix...")
    try:
        # Force reimport
        if 'discord' in sys.modules:
            del sys.modules['discord']

        import discord
        from discord.ext import commands

        # Test bot creation
        intents = discord.Intents.default()
        bot = commands.Bot(command_prefix='!', intents=intents)

        print("   ✅ Discord import test: PASSED")
        print(f"   ✅ Discord version: {discord.__version__}")
        print("   ✅ Bot creation test: PASSED")

    except Exception as e:
        print(f"   ❌ Discord import test: FAILED ({e})")
        print("\n🔍 Additional troubleshooting needed:")
        print("   1. Check if you're in the correct virtual environment")
        print("   2. Try: pip install --force-reinstall py-cord==2.4.1")
        print("   3. Restart your terminal/IDE")
        return

    print("\n🎉 SUCCESS: Discord imports are now working!")
    print("\n📋 Next steps:")
    print("   1. Run: python troubleshoot.py")
    print("   2. Run: python test_integration.py")
    print("   3. Configure your .env file")
    print("   4. Run: python bot.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Fix script interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue with the error details above.")
