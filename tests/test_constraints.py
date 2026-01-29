import unittest
from zai.core.interpreter import Interpreter
from zai.core.parser import get_parser

class TestConstraints(unittest.TestCase):
    def test_multiple_contexts_fail(self):
        code = """
        agent BadAgent
        context C1 { a: 1 }
        context C2 { b: 2 }
        skill Main() { success 0 "OK" }
        """
        parser = get_parser()
        tree = parser.parse(code, start='agent')
        interpreter = Interpreter(tree)
        
        with self.assertRaises(RuntimeError) as cm:
            interpreter.run()
        self.assertIn("Multiple context definitions found", str(cm.exception))

    def test_import_context_fail(self):
        # Create temp header
        with open("bad_import.zaih", "w") as f: f.write('context Imported { x: 1 }')
        
        code = """
        agent BadImportAgent
        import "bad_import.zaih"
        context Local { y: 2 }
        skill Main() { success 0 "OK" }
        """
        parser = get_parser()
        tree = parser.parse(code, start='agent')
        interpreter = Interpreter(tree)
        
        try:
            with self.assertRaises(RuntimeError) as cm:
                interpreter.run()
            self.assertIn("Multiple context definitions found", str(cm.exception))
        finally:
            import os
            if os.path.exists("bad_import.zaih"): os.remove("bad_import.zaih")

    def test_multiple_personas_ok(self):
        code = """
        agent GoodAgent
        context C1 { a: 1 }
        persona P1 { base_instruction { "I am P1" } }
        persona P2 { base_instruction { "I am P2" } }
        skill Main() { success 0 "OK" }
        """
        parser = get_parser()
        tree = parser.parse(code, start='agent')
        interpreter = Interpreter(tree)
        # Should not raise exception
        interpreter.run()

if __name__ == "__main__":
    unittest.main()
