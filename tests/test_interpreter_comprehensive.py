import unittest
from unittest.mock import MagicMock
import os
import shutil
from zai.core.parser import get_parser
from zai.core.interpreter import Interpreter

class TestInterpreterComprehensive(unittest.TestCase):
    def setUp(self):
        self.parser = get_parser()
        self.mock_ai = MagicMock()
        self.mock_exec = MagicMock()
        
        # Default mock behavior
        self.mock_ai.handle.return_value = {}
        self.mock_exec.handle.return_value = {}
        
        if os.path.exists(".zai_ipc"):
            shutil.rmtree(".zai_ipc")

    def run_code(self, code):
        tree = self.parser.parse(code, start='start')
        interpreter = Interpreter(tree, ai_bridge=self.mock_ai, exec_bridge=self.mock_exec)
        return interpreter.run(), interpreter.env

    def test_control_flow(self):
        # IF/ELSE
        res, env = self.run_code("""
        agent A
        context C { y: "", z: "" }
        skill Main() {
            var x = 10
            if x > 5 { context.y = "GT" } else { context.y = "LT" }
            if x < 5 { context.z = "LT" } else { context.z = "GT" }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("y"), "GT")
        self.assertEqual(env.get_context("z"), "GT")
        
        # WHILE
        res, env = self.run_code("""
        agent A
        context C { cnt: 0 }
        skill Main() {
            while context.cnt < 3 { context.cnt = context.cnt + 1 }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("cnt"), 3)

    def test_variable_scope(self):
        # Shadowing
        res, env = self.run_code("""
        agent A
        context C { x: "Global", check_local: "", check_ctx: "" }
        skill Main() {
            var x = "Local"
            context.check_local = x
            context.check_ctx = context.x
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("check_local"), "Local")
        self.assertEqual(env.get_context("check_ctx"), "Global")

    def test_ai_process(self):
        self.mock_ai.handle.return_value = {"summary": "Done"}
        res, env = self.run_code("""
        agent A
        context C { summary: "" }
        persona P { base_instruction { "Act helpful" } }
        skill Main() {
            process "Summarize" { extract: ["summary"] }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("summary"), "Done")
        call_args = self.mock_ai.handle.call_args
        self.assertIn("Act helpful", call_args[0][2]) # check system prompt

    def test_nested_invoke(self):
        res, env = self.run_code("""
        agent A
        skill Helper() {
             var res = 100
             success 0 "OK"
        }
        skill Main() {
             invoke Helper()
             success 0 "OK"
        }
        """)
        self.assertEqual(res["status"], "success")

    def test_wait_timeout(self):
        # Test timeout branch of wait
        tree = self.parser.parse("""
        agent A
        context C { c: 0, m: "" }
        skill Main() {
             [c, m] = wait NonExistent
             context.c = c
             context.m = m
             success 0 "OK"
        }
        """, start='start')
        interpreter = Interpreter(tree, wait_timeout=0.1)
        res = interpreter.run()
        
        self.assertEqual(interpreter.env.get_context("c"), -1)
        self.assertEqual(interpreter.env.get_context("m"), "TIMEOUT") 

    def test_expressions(self):
        res, env = self.run_code("""
        agent A
        context C { a: 0, b: 0, c: 0.0, d: 0, e: false, f: false, g: true, h: false }
        skill Main() {
             context.a = 1 + 2
             context.b = 3 * 4
             context.c = 10 / 2
             context.d = 5 - 1
             context.e = 1 == 1
             context.f = 1 != 2
             context.g = true && false
             context.h = true || false
             success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("a"), 3)
        self.assertEqual(env.get_context("b"), 12)
        self.assertEqual(env.get_context("c"), 5.0)
        self.assertEqual(env.get_context("d"), 4)
        self.assertTrue(env.get_context("e"))
        self.assertTrue(env.get_context("f"))
        self.assertFalse(env.get_context("g"))
        self.assertTrue(env.get_context("h"))

if __name__ == '__main__':
    unittest.main()
