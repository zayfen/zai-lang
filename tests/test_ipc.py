import os
import time
import shutil
import multiprocessing
from zai.core.interpreter import Interpreter
from zai.core.parser import get_parser

SENDER_CODE = """
agent Sender
skill Main() {
    wait_time = 2
    notify Receiver "HELLO" "World"
    say "Sent message"
    success 0 "Done"
}
"""

RECEIVER_CODE = """
agent Receiver
skill Main() {
    [code, payload] = wait Sender
    say "Received: {code} - {payload}"
    if code != "HELLO" { fail 1 "Wrong code" }
    if payload != "World" { fail 1 "Wrong payload" }
    success 0 "Done"
}
"""

def run_agent(name, code):
    parser = get_parser()
    tree = parser.parse(code, start='agent')
    interpreter = Interpreter(tree)
    # Using a shared temp directory for IPC relative to CWD
    interpreter.run()

class TestIPC:
    def setup_method(self):
        if os.path.exists(".zai_ipc"):
            shutil.rmtree(".zai_ipc")

    def test_ipc(self):
        self.setup_method()
        
        # Start Receiver in a separate process
        p_receiver = multiprocessing.Process(target=run_agent, args=("Receiver", RECEIVER_CODE))
        p_receiver.start()
        
        time.sleep(1) # Give receiver time to start waiting
        
        # Start Sender
        p_sender = multiprocessing.Process(target=run_agent, args=("Sender", SENDER_CODE))
        p_sender.start()
        
        p_sender.join(timeout=5)
        p_receiver.join(timeout=5)
        
        assert p_sender.exitcode == 0
        assert p_receiver.exitcode == 0

if __name__ == "__main__":
    t = TestIPC()
    t.test_ipc()
    print("IPC Test Passed!")
