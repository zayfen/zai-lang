import unittest
from unittest.mock import MagicMock, patch
import os
import json
from zai.runtime.default_bridge import DefaultAIBridge, DefaultExecBridge
from zai.builtin import tools

class TestDefaultBridges(unittest.TestCase):
    
    @patch('zai.runtime.default_bridge.OpenAI')
    def test_ai_bridge(self, mock_openai):
        # Setup mock
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content=json.dumps({"mood": "happy"})))]
        mock_client.chat.completions.create.return_value = mock_response
        
        bridge = DefaultAIBridge(api_key="test_key")
        result = bridge.handle("How are you?", ["mood"], "You are a helpful assistant", {})
        
        self.assertEqual(result, {"mood": "happy"})
        mock_client.chat.completions.create.assert_called_once()

    def test_exec_bridge_builtin(self):
        bridge = DefaultExecBridge()
        # Test 'ls' builtin
        with patch('zai.builtin.tools.ls') as mock_ls:
            mock_ls.return_value = {"items": ["file1.txt"], "path": "/tmp"}
            result = bridge.handle("ls .", ["items"])
            self.assertEqual(result, {"items": ["file1.txt"]})
            mock_ls.assert_called_once_with(".")

    def test_exec_bridge_bash(self):
        bridge = DefaultExecBridge()
        # Test fallback to bash
        with patch('zai.builtin.tools.bash') as mock_bash:
            mock_bash.return_value = {"stdout": "hello", "stderr": "", "code": 0}
            result = bridge.handle("echo hello", ["stdout"])
            self.assertEqual(result, {"stdout": "hello"})
            mock_bash.assert_called_once_with("echo hello")

    def test_builtin_tools_logic(self):
        # Test a real builtin tool logic (e.g., mkdir and delete)
        test_dir = "test_builtin_dir"
        if os.path.exists(test_dir):
            tools.delete(test_dir)
            
        res = tools.mkdir(test_dir)
        self.assertTrue(res.get("success"))
        self.assertTrue(os.path.exists(test_dir))
        
        res = tools.delete(test_dir)
        self.assertTrue(res.get("success"))
        self.assertFalse(os.path.exists(test_dir))

if __name__ == '__main__':
    unittest.main()
