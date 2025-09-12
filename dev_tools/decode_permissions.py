#!/usr/bin/env python3
"""
Discord Permissions Decoder
===========================

Decode Discord bot permission integers to human-readable format.
Helps verify bot permissions are correctly configured.

Usage: python decode_permissions.py [permission_integer]
"""

import sys

# Discord Permission Bit Values
PERMISSIONS = {
    'CREATE_INSTANT_INVITE': 1 << 0,
    'KICK_MEMBERS': 1 << 1,
    'BAN_MEMBERS': 1 << 2,
    'ADMINISTRATOR': 1 << 3,
    'MANAGE_CHANNELS': 1 << 4,
    'MANAGE_GUILD': 1 << 5,
    'ADD_REACTIONS': 1 << 6,
    'VIEW_AUDIT_LOG': 1 << 7,
    'PRIORITY_SPEAKER': 1 << 8,
    'STREAM': 1 << 9,
    'VIEW_CHANNEL': 1 << 10,
    'SEND_MESSAGES': 1 << 11,
    'SEND_TTS_MESSAGES': 1 << 12,
    'MANAGE_MESSAGES': 1 << 13,
    'EMBED_LINKS': 1 << 14,
    'ATTACH_FILES': 1 << 15,
    'READ_MESSAGE_HISTORY': 1 << 16,
    'MENTION_EVERYONE': 1 << 17,
    'USE_EXTERNAL_EMOJIS': 1 << 18,
    'VIEW_GUILD_INSIGHTS': 1 << 19,
    'CONNECT': 1 << 20,
    'SPEAK': 1 << 21,
    'MUTE_MEMBERS': 1 << 22,
    'DEAFEN_MEMBERS': 1 << 23,
    'MOVE_MEMBERS': 1 << 24,
    'USE_VAD': 1 << 25,
    'CHANGE_NICKNAME': 1 << 26,
    'MANAGE_NICKNAMES': 1 << 27,
    'MANAGE_ROLES': 1 << 28,
    'MANAGE_WEBHOOKS': 1 << 29,
    'MANAGE_EMOJIS_AND_STICKERS': 1 << 30,
    'USE_APPLICATION_COMMANDS': 1 << 31,
    'REQUEST_TO_SPEAK': 1 << 32,
    'MANAGE_EVENTS': 1 << 33,
    'MANAGE_THREADS': 1 << 34,
    'CREATE_PUBLIC_THREADS': 1 << 35,
    'CREATE_PRIVATE_THREADS': 1 << 36,
    'USE_EXTERNAL_STICKERS': 1 << 37,
    'SEND_MESSAGES_IN_THREADS': 1 << 38,
    'USE_EMBEDDED_ACTIVITIES': 1 << 39,
    'MODERATE_MEMBERS': 1 << 40,
    'VIEW_CREATOR_MONETIZATION_ANALYTICS': 1 << 41,
    'USE_SOUNDBOARD': 1 << 42,
    'CREATE_EXPRESSIONS': 1 << 43,
    'CREATE_EVENTS': 1 << 44,
    'USE_EXTERNAL_SOUNDS': 1 << 45,
    'SEND_VOICE_MESSAGES': 1 << 46,
    'SEND_POLLS': 1 << 47,
    'USE_EXTERNAL_APPS': 1 << 48,
}

# Required permissions for audio recording bot
REQUIRED_PERMISSIONS = [
    'VIEW_CHANNEL',
    'CONNECT',
    'SPEAK',
    'USE_VAD',
    'READ_MESSAGE_HISTORY'
]

# Dangerous permissions that should be avoided
DANGEROUS_PERMISSIONS = [
    'ADMINISTRATOR',
    'MANAGE_GUILD',
    'BAN_MEMBERS',
    'KICK_MEMBERS',
    'MANAGE_ROLES',
    'MANAGE_CHANNELS'
]

def decode_permissions(permission_int):
    """
    Decode a Discord permission integer into individual permissions.

    Args:
        permission_int (int): Discord permission integer

    Returns:
        dict: Dictionary with permission analysis
    """
    permission_int = int(permission_int)

    granted_permissions = []
    missing_required = []
    dangerous_granted = []

    # Check each permission
    for name, value in PERMISSIONS.items():
        if permission_int & value:
            granted_permissions.append(name)
            if name in DANGEROUS_PERMISSIONS:
                dangerous_granted.append(name)

    # Check required permissions
    for required in REQUIRED_PERMISSIONS:
        if required not in granted_permissions:
            missing_required.append(required)

    return {
        'total_permissions': len(granted_permissions),
        'granted_permissions': sorted(granted_permissions),
        'required_permissions': REQUIRED_PERMISSIONS,
        'missing_required': missing_required,
        'dangerous_granted': dangerous_granted,
        'permission_int': permission_int,
        'permission_hex': hex(permission_int),
        'is_admin': 'ADMINISTRATOR' in granted_permissions
    }

def format_analysis(analysis):
    """
    Format permission analysis for display.

    Args:
        analysis (dict): Permission analysis from decode_permissions

    Returns:
        str: Formatted analysis string
    """
    output = []
    output.append("=" * 60)
    output.append("DISCORD BOT PERMISSION ANALYSIS")
    output.append("=" * 60)
    output.append("")

    # Basic info
    output.append(f"Permission Integer: {analysis['permission_int']}")
    output.append(f"Permission Hex: {analysis['permission_hex']}")
    output.append(f"Total Permissions: {analysis['total_permissions']}")
    output.append(f"Administrator: {'YES - DANGEROUS!' if analysis['is_admin'] else 'No'}")
    output.append("")

    # Required permissions check
    output.append("REQUIRED PERMISSIONS FOR AUDIO BOT:")
    output.append("-" * 40)
    for perm in analysis['required_permissions']:
        status = "✅ GRANTED" if perm not in analysis['missing_required'] else "❌ MISSING"
        output.append(f"{perm:<25} {status}")
    output.append("")

    # Missing required permissions
    if analysis['missing_required']:
        output.append("⚠️  MISSING REQUIRED PERMISSIONS:")
        for perm in analysis['missing_required']:
            output.append(f"  - {perm}")
        output.append("")

    # Dangerous permissions
    if analysis['dangerous_granted']:
        output.append("🚨 DANGEROUS PERMISSIONS GRANTED:")
        output.append("Consider removing these for security:")
        for perm in analysis['dangerous_granted']:
            output.append(f"  - {perm}")
        output.append("")

    # All granted permissions
    output.append("ALL GRANTED PERMISSIONS:")
    output.append("-" * 40)
    for i, perm in enumerate(analysis['granted_permissions'], 1):
        marker = "🚨" if perm in DANGEROUS_PERMISSIONS else "✅" if perm in REQUIRED_PERMISSIONS else "  "
        output.append(f"{i:2d}. {marker} {perm}")

    output.append("")
    output.append("LEGEND:")
    output.append("✅ = Required for audio bot functionality")
    output.append("🚨 = Potentially dangerous permission")
    output.append("   = Optional/unnecessary permission")

    return "\n".join(output)

def get_minimal_permissions():
    """
    Calculate the minimal permission integer needed for the audio bot.

    Returns:
        int: Minimal permission integer
    """
    minimal = 0
    for perm_name in REQUIRED_PERMISSIONS:
        if perm_name in PERMISSIONS:
            minimal |= PERMISSIONS[perm_name]
    return minimal

def main():
    """Main execution function."""
    if len(sys.argv) != 2:
        print("Discord Permissions Decoder")
        print("=" * 30)
        print("Usage: python decode_permissions.py <permission_integer>")
        print("")
        print("Example:")
        print(f"  python decode_permissions.py 1125899941448832")
        print("")

        # Show minimal permissions needed
        minimal = get_minimal_permissions()
        print(f"Minimal permissions needed for audio bot: {minimal}")
        print(f"Minimal permissions hex: {hex(minimal)}")
        return

    try:
        permission_int = sys.argv[1]

        # Handle different input formats
        if permission_int.startswith('0x'):
            permission_int = int(permission_int, 16)
        else:
            permission_int = int(permission_int)

        # Decode and analyze
        analysis = decode_permissions(permission_int)

        # Display results
        print(format_analysis(analysis))

        # Security recommendations
        print("\n" + "=" * 60)
        print("SECURITY RECOMMENDATIONS:")
        print("=" * 60)

        if analysis['is_admin']:
            print("🚨 CRITICAL: Remove Administrator permission!")
            print("   This grants ALL permissions and is a security risk.")

        if analysis['dangerous_granted']:
            print("⚠️  WARNING: Remove dangerous permissions listed above.")
            print("   Grant only the minimum permissions needed.")

        if not analysis['missing_required']:
            print("✅ All required permissions are granted.")
        else:
            print("❌ Missing required permissions - bot may not function properly.")

        print(f"\n🔒 Recommended minimal permissions: {get_minimal_permissions()}")

    except ValueError as e:
        print(f"Error: Invalid permission integer '{sys.argv[1]}'")
        print("Please provide a valid integer or hex value (e.g., 0x1234)")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
