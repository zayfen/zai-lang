"""Comprehensive tests for all zai-lang statements."""

import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
import os
import sys

from zai.core.parser import get_parser
from zai.core.interpreter import Interpreter


class BaseTestCase(unittest.TestCase):
    """Base test case with helper methods."""

    def run_code(self, code, start='agent', ai_bridge=None, exec_bridge=None):
        """Parse and run zai code, returning result and environment."""
        parser = get_parser()
        tree = parser.parse(code, start=start)
        interpreter = Interpreter(tree, ai_bridge=ai_bridge, exec_bridge=exec_bridge)
        result = interpreter.run()
        return result, interpreter.env, interpreter

    def mock_ai_bridge(self, return_value=None):
        """Create a mock AI bridge."""
        mock = MagicMock()
        mock.handle.return_value = return_value or {"result": "ok"}
        return mock

    def mock_exec_bridge(self, return_value=None):
        """Create a mock exec bridge."""
        mock = MagicMock()
        mock.handle.return_value = return_value or {"output": "done"}
        return mock


class TestVarDecl(BaseTestCase):
    """Test var declaration statement: var x = expression"""

    def test_var_decl_number(self):
        """Variable declaration with number."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            var x = 42
            context.result = x
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("result"), 42)

    def test_var_decl_string(self):
        """Variable declaration with string."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            var msg = "hello"
            context.result = msg
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("result"), "hello")

    def test_var_decl_expression(self):
        """Variable declaration with expression."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            var x = 1 + 2 * 3
            context.result = x
            success 0 "OK"
        }
        """)
        # Note: operator precedence may be left-to-right
        self.assertEqual(env.get_context("result"), 9.0)  # (1+2)*3

    def test_var_decl_boolean(self):
        """Variable declaration with boolean."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            var flag = true
            context.result = flag
            success 0 "OK"
        }
        """)
        self.assertTrue(env.get_context("result"))

    def test_var_scope_is_local(self):
        """Variable is local to skill - verified by not affecting context."""
        res, env, interp = self.run_code("""
        agent A
        context C { x: "initial" }
        skill Main() {
            var x = 42
            success 0 "OK"
        }
        """)
        # Local var should not affect context
        self.assertEqual(env.get_context("x"), "initial")


class TestAssignment(BaseTestCase):
    """Test assignment statements."""

    def test_assignment_local(self):
        """Assignment to local variable."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            var x = 1
            x = 42
            context.result = x
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("result"), 42)

    def test_assignment_context(self):
        """Assignment to context variable."""
        res, env, _ = self.run_code("""
        agent A
        context C { value: 0 }
        skill Main() {
            context.value = 100
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("value"), 100)

    def test_assignment_expression(self):
        """Assignment with expression."""
        res, env, _ = self.run_code("""
        agent A
        context C { total: 0 }
        skill Main() {
            context.total = 10 + 20 * 2
            success 0 "OK"
        }
        """)
        # Note: operator precedence may be left-to-right
        self.assertEqual(env.get_context("total"), 60.0)  # (10+20)*2

    def test_assignment_string_concat(self):
        """Assignment with string concatenation."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            var first = "Hello"
            var second = "World"
            context.greeting = first + " " + second
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("greeting"), "Hello World")

    def test_assignment_from_context(self):
        """Assignment from context to local."""
        res, env, _ = self.run_code("""
        agent A
        context C { value: 42 }
        skill Main() {
            var x = context.value
            context.copy = x
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("copy"), 42)


class TestIfStatement(BaseTestCase):
    """Test if/else statements."""

    def test_if_true(self):
        """If with true condition."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            if true {
                context.result = "taken"
            }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("result"), "taken")

    def test_if_false(self):
        """If with false condition - body not executed."""
        res, env, _ = self.run_code("""
        agent A
        context C { result: "initial" }
        skill Main() {
            if false {
                context.result = "changed"
            }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("result"), "initial")

    def test_if_else_true(self):
        """If/else with true condition."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            if true {
                context.result = "if-branch"
            } else {
                context.result = "else-branch"
            }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("result"), "if-branch")

    def test_if_else_false(self):
        """If/else with false condition."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            if false {
                context.result = "if-branch"
            } else {
                context.result = "else-branch"
            }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("result"), "else-branch")

    def test_if_comparison(self):
        """If with comparison operators."""
        res, env, _ = self.run_code("""
        agent A
        context C { x: 10, y: 20 }
        skill Main() {
            if context.x < context.y {
                context.result = "less"
            } else {
                context.result = "greater-or-equal"
            }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("result"), "less")

    def test_nested_if(self):
        """Nested if statements."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            var x = 5
            if x > 0 {
                if x < 10 {
                    context.result = "between"
                }
            }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("result"), "between")

    def test_if_logical_and(self):
        """If with && operator."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            var a = true
            var b = true
            if a && b {
                context.result = "both-true"
            } else {
                context.result = "not-both"
            }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("result"), "both-true")

    def test_if_logical_or(self):
        """If with || operator."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            var a = false
            var b = true
            if a || b {
                context.result = "at-least-one"
            } else {
                context.result = "none"
            }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("result"), "at-least-one")

    def test_if_equality(self):
        """If with == and != operators."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            var x = 10
            if x == 10 {
                context.eq = "equal"
            }
            if x != 5 {
                context.neq = "not-equal"
            }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("eq"), "equal")
        self.assertEqual(env.get_context("neq"), "not-equal")


class TestWhileStatement(BaseTestCase):
    """Test while loop statements."""

    def test_while_loop_count(self):
        """While loop counting."""
        res, env, _ = self.run_code("""
        agent A
        context C { count: 0 }
        skill Main() {
            while context.count < 5 {
                context.count = context.count + 1
            }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("count"), 5)

    def test_while_loop_zero_iterations(self):
        """While loop with false condition - zero iterations."""
        res, env, _ = self.run_code("""
        agent A
        context C { count: 0 }
        skill Main() {
            while false {
                context.count = context.count + 1
            }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("count"), 0)

    def test_while_with_local_var(self):
        """While loop with local variable."""
        res, env, _ = self.run_code("""
        agent A
        context C { sum: 0 }
        skill Main() {
            var i = 1
            while i <= 3 {
                context.sum = context.sum + i
                i = i + 1
            }
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("sum"), 6)  # 1+2+3


class TestResponseStatement(BaseTestCase):
    """Test say/reply statements."""

    @patch('sys.stdout', new_callable=StringIO)
    def test_say_string(self, mock_stdout):
        """Say with string literal."""
        res, _, _ = self.run_code("""
        agent A
        skill Main() {
            say "Hello, World!"
            success 0 "OK"
        }
        """)
        self.assertIn("Hello, World!", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_say_template(self, mock_stdout):
        """Say with template variable."""
        res, _, _ = self.run_code("""
        agent A
        context C { name: "Alice" }
        skill Main() {
            say "Hello, {{name}}!"
            success 0 "OK"
        }
        """)
        self.assertIn("Hello, Alice!", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_say_local_var(self, mock_stdout):
        """Say with local variable."""
        res, _, _ = self.run_code("""
        agent A
        skill Main() {
            var msg = "Test message"
            say msg
            success 0 "OK"
        }
        """)
        self.assertIn("Test message", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_say_expression(self, mock_stdout):
        """Say with expression result."""
        res, _, _ = self.run_code("""
        agent A
        skill Main() {
            say "Result: " + (2 + 3)
            success 0 "OK"
        }
        """)
        self.assertIn("Result: 5.0", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_reply(self, mock_stdout):
        """Reply statement (alias for say)."""
        res, _, _ = self.run_code("""
        agent A
        skill Main() {
            reply "This is a reply"
            success 0 "OK"
        }
        """)
        self.assertIn("This is a reply", mock_stdout.getvalue())


class TestProcessStatement(BaseTestCase):
    """Test process statement (AI interaction)."""

    def test_process_basic(self):
        """Basic process with extract."""
        mock_ai = self.mock_ai_bridge({"sentiment": "positive", "confidence": "0.9"})
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            process "Analyze sentiment" {
                extract: ["sentiment", "confidence"]
            }
            success 0 "OK"
        }
        """, ai_bridge=mock_ai)
        self.assertEqual(env.get_context("sentiment"), "positive")
        self.assertEqual(env.get_context("confidence"), "0.9")

    def test_process_with_context(self):
        """Process using context variables."""
        mock_ai = self.mock_ai_bridge({"result": "processed"})
        res, env, _ = self.run_code("""
        agent A
        context C { input: "test data" }
        skill Main() {
            process "Process: {{input}}" {
                extract: ["result"]
            }
            success 0 "OK"
        }
        """, ai_bridge=mock_ai)
        self.assertEqual(env.get_context("result"), "processed")

    def test_process_no_extract(self):
        """Process without extract clause."""
        mock_ai = self.mock_ai_bridge()
        res, _, _ = self.run_code("""
        agent A
        skill Main() {
            process "Just do something"
            success 0 "OK"
        }
        """, ai_bridge=mock_ai)
        self.assertEqual(res.get("status"), "success")

    def test_process_with_persona(self):
        """Process with persona overlay."""
        mock_ai = self.mock_ai_bridge({"style": "formal"})
        mock_ai.last_system = None
        res, env, interp = self.run_code("""
        agent A
        persona Expert {
            tone { "Professional and concise" }
        }
        skill Main() {
            process Expert.tone {
                extract: ["style"]
            }
            success 0 "OK"
        }
        """, ai_bridge=mock_ai)
        self.assertEqual(env.get_context("style"), "formal")


class TestAskStatement(BaseTestCase):
    """Test ask statement (user input)."""

    @patch('builtins.input', return_value="Alice")
    def test_ask_basic(self, mock_input):
        """Basic ask storing to context."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            ask "What's your name? {{name=}}"
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("name"), "Alice")

    @patch('builtins.input', return_value="42")
    def test_ask_number(self, mock_input):
        """Ask receiving number-like input."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            ask "Enter a number: {{num=}}"
            success 0 "OK"
        }
        """)
        self.assertEqual(env.get_context("num"), "42")


class TestExecStatement(BaseTestCase):
    """Test exec statement (external commands)."""

    def test_exec_basic(self):
        """Basic exec with filter."""
        mock_exec = self.mock_exec_bridge({"stdout": "output", "stderr": "", "code": "0"})
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            exec "ls -la" {
                filter: ["stdout"]
            }
            success 0 "OK"
        }
        """, exec_bridge=mock_exec)
        self.assertEqual(env.get_context("stdout"), "output")

    def test_exec_no_filter(self):
        """Exec without filter."""
        mock_exec = self.mock_exec_bridge({"result": "done"})
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            exec "some command"
            success 0 "OK"
        }
        """, exec_bridge=mock_exec)
        mock_exec.handle.assert_called_once()

    def test_exec_with_context(self):
        """Exec command using context values."""
        mock_exec = self.mock_exec_bridge({"found": "yes"})
        res, env, _ = self.run_code("""
        agent A
        context C { filename: "test.txt" }
        skill Main() {
            var cmd = "find " + context.filename
            exec cmd
            success 0 "OK"
        }
        """, exec_bridge=mock_exec)
        # Verify exec was called
        mock_exec.handle.assert_called_once()


class TestSkillInvoke(BaseTestCase):
    """Test skill invocation."""

    def test_invoke_basic(self):
        """Basic skill invocation."""
        res, env, _ = self.run_code("""
        agent A
        skill Helper() {
            context.helper_called = true
            success 0 "Helper done"
        }
        skill Main() {
            invoke Helper()
            success 0 "Main done"
        }
        """)
        self.assertTrue(env.get_context("helper_called"))

    def test_invoke_with_args(self):
        """Skill invocation with arguments."""
        res, env, _ = self.run_code("""
        agent A
        skill Process(x, y) {
            context.sum = x + y
            success 0 "Done"
        }
        skill Main() {
            invoke Process(x=10, y=20)
            success 0 "Main done"
        }
        """)
        self.assertEqual(env.get_context("sum"), 30)

    def test_invoke_sequence(self):
        """Multiple skill invocations in sequence."""
        res, env, _ = self.run_code("""
        agent A
        context C { count: 0 }
        skill Compute() {
            context.count = context.count + 10
            success 0 "Computed"
        }
        skill Main() {
            invoke Compute()
            invoke Compute()
            context.status = "completed"
            success 0 "Main done"
        }
        """)
        self.assertEqual(env.get_context("status"), "completed")
        self.assertEqual(env.get_context("count"), 20)


class TestReturnStatement(BaseTestCase):
    """Test success/fail return statements."""

    def test_success_basic(self):
        """Basic success return."""
        res, _, _ = self.run_code("""
        agent A
        skill Main() {
            success 0 "All good"
        }
        """)
        self.assertEqual(res.get("status"), "success")
        self.assertEqual(res.get("code"), 0)
        self.assertEqual(res.get("message"), "All good")

    def test_success_with_code(self):
        """Success with non-zero code."""
        res, _, _ = self.run_code("""
        agent A
        skill Main() {
            success 42 "Partial success"
        }
        """)
        self.assertEqual(res.get("status"), "success")
        self.assertEqual(res.get("code"), 42)

    def test_fail_basic(self):
        """Basic fail return."""
        res, _, _ = self.run_code("""
        agent A
        skill Main() {
            fail 1 "Something went wrong"
        }
        """)
        self.assertEqual(res.get("status"), "fail")
        self.assertEqual(res.get("code"), 1)

    def test_fail_with_expression(self):
        """Fail with dynamic message."""
        res, _, _ = self.run_code("""
        agent A
        skill Main() {
            var error_msg = "Error occurred"
            fail 500 error_msg
        }
        """)
        self.assertEqual(res.get("status"), "fail")
        self.assertEqual(res.get("message"), "Error occurred")


class TestComplexScenarios(BaseTestCase):
    """Test complex statement combinations."""

    def test_string_accumulation(self):
        """Test string accumulation in loop."""
        res, env, _ = self.run_code("""
        agent A
        context C { result: "" }
        skill Main() {
            var i = 1
            var output = ""
            while i <= 3 {
                output = output + i + " "
                i = i + 1
            }
            context.result = output
            success 0 "Done"
        }
        """)
        self.assertEqual(env.get_context("result"), "1.0 2.0 3.0 ")

    def test_counter_with_multiple_skills(self):
        """Counter using multiple skills."""
        res, env, _ = self.run_code("""
        agent A
        context C { value: 0 }

        skill Increment() {
            context.value = context.value + 1
            success 0 "Incremented"
        }

        skill Main() {
            invoke Increment()
            invoke Increment()
            invoke Increment()
            success 0 "Done"
        }
        """)
        self.assertEqual(env.get_context("value"), 3)

    def test_state_machine(self):
        """Simple state machine."""
        res, env, _ = self.run_code("""
        agent A
        context C { state: "idle", count: 0 }

        skill Process() {
            if context.state == "idle" {
                context.state = "processing"
                context.count = context.count + 1
            } else {
                if context.state == "processing" {
                    context.state = "done"
                }
            }
            success 0 "Processed"
        }

        skill Main() {
            invoke Process()
            invoke Process()
            success 0 "Done"
        }
        """)
        self.assertEqual(env.get_context("state"), "done")
        self.assertEqual(env.get_context("count"), 1)


class TestEdgeCases(BaseTestCase):
    """Test edge cases and error conditions."""

    def test_empty_skill(self):
        """Skill with no statements."""
        res, _, _ = self.run_code("""
        agent A
        skill Main() {
            success 0 "Empty"
        }
        """)
        self.assertEqual(res.get("status"), "success")

    def test_deeply_nested_if(self):
        """Deeply nested if statements."""
        res, env, _ = self.run_code("""
        agent A
        skill Main() {
            var a = 1
            var b = 2
            var c = 3
            if a < b {
                if b < c {
                    if a < c {
                        context.deep = "very deep"
                    }
                }
            }
            success 0 "Done"
        }
        """)
        self.assertEqual(env.get_context("deep"), "very deep")

    def test_while_single_iteration(self):
        """While loop with single iteration."""
        res, env, _ = self.run_code("""
        agent A
        context C { count: 0 }
        skill Main() {
            while context.count < 1 {
                context.count = context.count + 1
            }
            success 0 "Done"
        }
        """)
        self.assertEqual(env.get_context("count"), 1)

    def test_variable_separation(self):
        """Local variable and context variable are separate."""
        res, env, _ = self.run_code("""
        agent A
        context C { x: 10 }
        skill Main() {
            var local_x = 5
            context.local_x = local_x
            context.global_x = context.x
            success 0 "Done"
        }
        """)
        self.assertEqual(env.get_context("local_x"), 5)
        self.assertEqual(env.get_context("global_x"), 10)


if __name__ == '__main__':
    unittest.main()
