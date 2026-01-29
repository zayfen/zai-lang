import sys
import argparse
from zai.core.parser import get_parser
from zai.core.interpreter import Interpreter

def main():
    parser = argparse.ArgumentParser(description="zai: AI Orchestration Language")
    parser.add_argument("file", help="The .zai file to execute")
    parser.add_argument("--skill", default="Main", help="Entry skill (default: Main)")
    
    args = parser.parse_args()
    
    try:
        with open(args.file, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)
        
    lang_parser = get_parser()
    try:
        tree = lang_parser.parse(code, start='agent')
    except Exception as e:
        print(f"Parse Error: {e}")
        sys.exit(1)
        
    import os
    base_path = os.path.dirname(os.path.abspath(args.file))
    interpreter = Interpreter(tree, base_path=base_path)
    result = interpreter.run(entry_skill=args.skill)
    
    if result.get("status") == "fail":
        print(f"Execution Failed: {result.get('message')} (Code: {result.get('code')})")
        sys.exit(1)

if __name__ == "__main__":
    main()
