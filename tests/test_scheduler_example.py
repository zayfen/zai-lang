import unittest
from zai.core.interpreter import Interpreter
from zai.core.parser import get_parser
import os
import sys
from io import StringIO

class TestSchedulerExample(unittest.TestCase):
    def setUp(self):
        self.parser = get_parser()
        self.captured_output = StringIO()
        
    def test_scheduler_example(self):
        # Path to the example
        # Assuming we run this from the project root
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        example_path = os.path.join(base_path, "examples", "lifestyle", "scheduler.zai")
        
        with open(example_path, "r") as f:
            code = f.read()

        # Mock AI Bridge
        class MockAIBridge:
            def handle(self, prompt, keys, system, context):
                # Simulate LifeCoach response
                if "Suggest a 1-hour activity" in prompt:
                    return {"schedule_plan": "Go for a light jog"}
                return {}

        # Mock Exec Bridge
        class MockExecBridge:
            def handle(self, command, keys):
                if command.startswith("date"):
                    # The interpreter expects the bridge to filter/map the output to keys
                    # In this example, the code is: exec "date" { filter: ["raw_date"] }
                    output = "Thu Jan 1 10:00:00 UTC 2026"
                    if keys and "raw_date" in keys:
                        return {"raw_date": output}
                    return {}
                return {}

        # Mock Input (Standard Input)
        # The script asks: "How are you feeling today? (energetic/tired/neutral) {user_mood=}"
        # We provide "energetic"
        sys.stdin = StringIO("energetic\n")

        # Capture Stdout
        original_stdout = sys.stdout
        sys.stdout = self.captured_output

        try:
            # Change directory to example location so import "config.zaih" works
            # Alternatively, the interpreter could handle relative imports, 
            # but for now, chdir is safer for the test environment.
            cwd = os.getcwd()
            os.chdir(os.path.dirname(example_path))
            
            tree = self.parser.parse(code, start='agent')
            interpreter = Interpreter(tree, ai_bridge=MockAIBridge(), exec_bridge=MockExecBridge())
            interpreter.run()
            
        finally:
            sys.stdout = original_stdout
            # Restore stdin
            sys.stdin = sys.__stdin__
            # Restore CWD
            os.chdir(cwd)

        output = self.captured_output.getvalue()
        
        # Verification
        self.assertIn("--- Personal Schedule Manager ---", output)
        self.assertIn("Analyzing your context...", output)
        self.assertIn("Mood: energetic", output)
        # The mock execution of `date` assumes success but currently the interpreter might print debug info or nothing specific for exec unless we say it.
        # But we do check the final plan.
        self.assertIn("Sugested Plan: Go for a light jog", output)

if __name__ == "__main__":
    unittest.main()
