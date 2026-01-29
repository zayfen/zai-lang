from abc import ABC, abstractmethod

class BaseBridge(ABC):
    @abstractmethod
    def handle(self, *args, **kwargs):
        pass

class AIBridge(BaseBridge):
    @abstractmethod
    def handle(self, prompt, extract_keys, system_prompt, context):
        pass

class ExecBridge(BaseBridge):
    @abstractmethod
    def handle(self, cmd, filter_keys):
        pass
