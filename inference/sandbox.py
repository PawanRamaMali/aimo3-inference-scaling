"""Jupyter sandbox for Python code execution."""

import queue
from jupyter_client import KernelManager
from typing import Optional


class JupyterSandbox:
    """
    Sandbox for executing Python code in isolated Jupyter kernels.

    Used for Tool-Integrated Reasoning (TIR) where the model can
    execute Python code to verify calculations.
    """

    def __init__(self):
        """Initialize a new Jupyter kernel."""
        self.km = KernelManager(kernel_name='python3')
        self.km.start_kernel()
        self.kc = self.km.client()
        self.kc.start_channels()
        self.kc.wait_for_ready(timeout=60)

    def execute(self, code: str, timeout: int = 6) -> str:
        """
        Execute Python code and return output.

        Args:
            code: Python code to execute
            timeout: Maximum execution time in seconds

        Returns:
            Output string (stdout + stderr)
        """
        msg_id = self.kc.execute(code)

        outputs = []
        try:
            while True:
                try:
                    msg = self.kc.get_iopub_msg(timeout=timeout)
                except queue.Empty:
                    break

                msg_type = msg['msg_type']
                content = msg['content']

                if msg_type == 'stream':
                    outputs.append(content['text'])
                elif msg_type == 'execute_result':
                    outputs.append(str(content['data'].get('text/plain', '')))
                elif msg_type == 'error':
                    outputs.append('\n'.join(content['traceback']))
                elif msg_type == 'status' and content['execution_state'] == 'idle':
                    break

        except Exception as e:
            outputs.append(f"Execution error: {str(e)}")

        return '\n'.join(outputs)

    def shutdown(self):
        """Shutdown the kernel."""
        self.kc.stop_channels()
        self.km.shutdown_kernel()

    def __del__(self):
        """Cleanup on deletion."""
        try:
            self.shutdown()
        except:
            pass


def create_sandbox_pool(size: int = 8) -> queue.Queue:
    """
    Create a pool of sandbox instances.

    Args:
        size: Number of sandboxes to create

    Returns:
        Queue containing sandbox instances
    """
    pool = queue.Queue()
    for _ in range(size):
        pool.put(JupyterSandbox())
    return pool
