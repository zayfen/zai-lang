import unittest
from zai.core.interpreter import Interpreter
from zai.core.parser import get_parser
import os

class TestCoreFeatures(unittest.TestCase):
    def test_persona_binding(self):
        code = """
        agent TestAgent
        persona P1 { base_instruction { "Instruction 1" } }
        persona P2 { base_instruction { "Instruction 2" } }
        skill Main() {
            process "Task" { extract: ["dummy"] }
            success 0 "OK"
        }
        """
        parser = get_parser()
        tree = parser.parse(code, start='agent')
        
        # Mock bridge
        class MockBridge:
            def handle(self, prompt, keys, system, context):
                self.last_system = system
                return {}
        
        bridge = MockBridge()
        interpreter = Interpreter(tree, ai_bridge=bridge)
        interpreter.run()
        
        assert "Instruction 1" in bridge.last_system
        assert "Instruction 2" in bridge.last_system
        assert "Persona: P1" in bridge.last_system
        assert "Persona: P2" in bridge.last_system

    def test_circular_import(self):
        # Create temporary files
        with open("a.zaih", "w") as f: f.write('import "b.zaih"')
        with open("b.zaih", "w") as f: f.write('import "a.zaih"')
        
        code = """
        agent TestImport
        import "a.zaih"
        skill Main() { success 0 "OK" }
        """
        parser = get_parser()
        tree = parser.parse(code, start='agent')
        interpreter = Interpreter(tree)
        
        # Should run without infinite recursion error
        try:
            interpreter.run()
        except RecursionError:
            self.fail("Recursion detected in imports")
        finally:
            if os.path.exists("a.zaih"): os.remove("a.zaih")
            if os.path.exists("b.zaih"): os.remove("b.zaih")

if __name__ == "__main__":
    unittest.main()
