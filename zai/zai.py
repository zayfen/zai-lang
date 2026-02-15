import sys
import os
import argparse
from zai.core.parser import get_parser
from zai.core.interpreter import Interpreter
from zai.config import get_config, get_str


def print_env_status():
    """Print detected ZAI_ environment variables status."""
    # Ensure config is initialized
    get_config()

    # Required and optional ZAI_ variables
    required_vars = ["ZAI_API_KEY"]
    optional_vars = ["ZAI_BASE_URL", "ZAI_MODEL", "ZAI_TEMPERATURE"]

    print("=" * 60)
    print("zai Environment Configuration")
    print("=" * 60)

    # Check required variables
    print("\n[Required Variables]")
    all_required_set = True
    for var in required_vars:
        value = get_str(var, "")
        status = "✓ SET" if value else "✗ NOT SET"
        masked_value = "***" if value and "KEY" in var else value
        if not value:
            all_required_set = False
        print(f"  {var}: {status}")
        if value:
            print(f"    Value: {masked_value}")

    # Check optional variables
    print("\n[Optional Variables]")
    for var in optional_vars:
        value = get_str(var, "")
        status = "✓ SET" if value else "- not set (using default)"
        print(f"  {var}: {status}")
        if value:
            print(f"    Value: {value}")

    # Show all detected ZAI_ variables from environment
    print("\n[All ZAI_ Variables from Shell Environment]")
    env_vars_found = False
    for key, value in os.environ.items():
        if key.startswith("ZAI_"):
            env_vars_found = True
            masked_value = "***" if "KEY" in key else value
            print(f"  {key}={masked_value}")
    if not env_vars_found:
        print("  (none detected in shell environment)")

    # Show config file locations
    print("\n[Config File Search Paths]")
    print(f"  1. Shell environment (highest priority)")
    cwd = os.getcwd()
    print(f"  2. {cwd}/.zai/config.json")
    home = os.path.expanduser("~")
    print(f"  3. {home}/.config/zai/config.json (lowest priority)")

    print("\n" + "=" * 60)

    return all_required_set


def main():
    parser = argparse.ArgumentParser(description="zai: AI Orchestration Language")
    parser.add_argument("file", help="The .zai file to execute")
    parser.add_argument("--agent", default=None, help="Agent to run (default: first found)")
    parser.add_argument("--skill", default="Main", help="Entry skill (default: Main)")
    parser.add_argument("--check-env", action="store_true", help="Check environment variables and exit")
    parser.add_argument("--no-env-check", action="store_true", help="Skip environment variable check")

    args = parser.parse_args()

    # Initialize config with current directory for local config loading
    get_config(cwd=os.getcwd())

    # Check environment only flag
    if args.check_env:
        print_env_status()
        sys.exit(0)

    # Check environment variables unless disabled
    if not args.no_env_check:
        all_required_set = print_env_status()
        if not all_required_set:
            print("\n⚠️  WARNING: Required ZAI_ environment variables are not set!")
            print("\nTo configure zai, you can:")
            print("  1. Set shell environment variables:")
            print("     export ZAI_API_KEY='your-api-key'")
            print("     export ZAI_BASE_URL='https://api.example.com/v1'")
            print("  2. Create .zai/config.json in your project directory")
            print("  3. Create ~/.config/zai/config.json for global settings")
            print("\nUse --no-env-check to skip this check.")
            print("Use --check-env to see current configuration.\n")
            sys.exit(1)
        print()  # Empty line before execution

    try:
        with open(args.file, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)
        
    lang_parser = get_parser()
    try:
        tree = lang_parser.parse(code, start='start')
    except Exception as e:
        print(f"Parse Error: {e}")
        sys.exit(1)

    base_path = os.path.dirname(os.path.abspath(args.file))
    interpreter = Interpreter(tree, base_path=base_path, source_file=os.path.abspath(args.file))
    result = interpreter.run(agent_name=args.agent, entry_skill=args.skill)
    
    if result.get("status") == "fail":
        print(f"Execution Failed: {result.get('message')} (Code: {result.get('code')})")
        sys.exit(1)

if __name__ == "__main__":
    main()
