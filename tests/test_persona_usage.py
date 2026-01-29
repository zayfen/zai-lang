import unittest
import sys
import os
from io import StringIO
from unittest.mock import MagicMock, patch
from zai.core.parser import get_parser
from zai.core.interpreter import Interpreter

class TestPersonaUsage(unittest.TestCase):
    def setUp(self):
        # We'll use the content directly to ensure no file path issues, 
        # or read from disk if we trust the path.
        # Let's read from disk to be faithful to the user request "against this example file"
        self.example_path = os.path.join(os.path.dirname(__file__), "../examples/persona_usage.zai")
        with open(self.example_path, "r") as f:
            self.code = f.read()
            
        self.parser = get_parser()
        self.mock_ai = MagicMock()
        self.mock_ai.handle.return_value = {"summary": "Mocked Response"}

    def test_persona_adaptation(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            print("Capture Test") # Verify capture works
            
            # Parse
            tree = self.parser.parse(self.code, start='start')
            
            # Run
            interpreter = Interpreter(tree, ai_bridge=self.mock_ai, base_path=os.path.dirname(self.example_path))
            result = interpreter.run()
            
            # Verify
            output = fake_out.getvalue()
            
        # Assertions
        self.assertEqual(result.get("status"), "success")
        self.assertIn("--- Context: Formal ---", output)
        self.assertIn("Style: Formal (Business)", output)
        
        self.assertIn("--- Context: Casual ---", output)
        self.assertIn("Style: Casual (Friendly)", output)

if __name__ == '__main__':
    unittest.main()
