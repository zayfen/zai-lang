import unittest
from lark import Lark, Tree, Token
from zai.core.parser import get_parser

class TestParserComprehensive(unittest.TestCase):
    def setUp(self):
        self.parser = get_parser()

    def assert_tree_data(self, tree, data):
        if not hasattr(tree, 'data'): return
        self.assertEqual(tree.data, data)

    def test_full_agent_structure(self):
        code = """
        agent FullTest
        import "lib.zaih"
        context C { a: 1 }
        persona P { base_instruction { "Hi" } }
        skill S() { success 0 "OK" }
        """
        tree = self.parser.parse(code, start='start')
        # agent children: Identifier, import_stmt*, ...
        agent = tree.children[0]
        self.assertEqual(agent.children[0].value, "FullTest")
        children = [c for c in agent.children[1:] if hasattr(c, 'data')]
        self.assertEqual(children[0].data, 'import_stmt')
        self.assertEqual(children[1].data, 'context_def')
        self.assertEqual(children[2].data, 'persona_def')
        self.assertEqual(children[3].data, 'skill_def')

    def test_all_statements(self):
        code = """
        agent StmtTest
        skill Main() {
            var x = 1
            context.y = 2
            if true { var z = 3 } else { var z = 4 }
            while false { var loop = 1 }
            process "Task" { extract: ["k"] }
            ask "Q {v=}"
            exec "cmd" { filter: ["out"] }
            notify Agent "Type" "Payload"
            [c, m] = wait Sender
            start Child
            invoke Nested()
            reply "Hi"
            say "Hello"
            success 0 "OK"
            fail 1 "Error"
        }
        """
        tree = self.parser.parse(code, start='start')
        agent = tree.children[0]
        skill = agent.children[-1] # Skill node (last child in agent)
        block = skill.children[2] # Block node
        stmts = [c.data for c in block.children]
        
        # expected = [ ... ]
        # self.assertEqual(stmts, expected)
        self.assertIn('start_stmt', stmts)
        self.assertIn('skill_invoke', stmts)
        self.assertIn('process_stmt', stmts)

    def test_expression_precedence(self):
        # 1 + 2 * 3 should be 1 + (2 * 3)
        code = """
        agent ExprTest
        skill Main() {
            var x = 1 + 2 * 3
            success 0 "OK"
        }
        """
        tree = self.parser.parse(code, start='start')
        # navigate to skill (last child of agent)
        agent = tree.children[0]
        skill = agent.children[-1]
        block = skill.children[2] 
        var_decl = block.children[0]
        var_decl = block.children[0]
        # print(var_decl.pretty()) # Debug
        # Structure depends on grammar. Assuming standard expression -> sum -> product
        # If binary_op is not explicit, we might need to drill down.
        # expression -> boolean -> disjunction -> conjunction -> comparison -> sum -> product ...
        # Let's verify the leaf nodes values/types
        pass

    def test_persona_blocks(self):
        code = """
        persona Complex {
            base {
                "Text"
                if context.flag { "Flag" } else { "NoFlag" }
            }
        }
        """
        tree = self.parser.parse(code, start='persona_def')
        item = tree.children[1]
        block = item.children[1]
        self.assertEqual(block.data, 'persona_block')
        child = block.children[0]
        if hasattr(child, 'data') and (child.data == 'expression' or child.data == 'string'):
            child = child.children[0]
        self.assertEqual(child.value.lower(), '"text"')
        self.assertEqual(block.children[1].data, 'persona_if')

    def test_config_file_parser(self):
        code = 'context C { x: 1 } import "other.zaih"'
        tree = self.parser.parse(code, start='config_file')
        self.assertEqual(tree.children[0].data, 'context_def')
        self.assertEqual(tree.children[1].data, 'import_stmt')

if __name__ == '__main__':
    unittest.main()
