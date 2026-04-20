"""Main solver class for AIMO3 mathematical problems."""

import re
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional

from .config import Config
from .voting import select_answer, check_early_stop


class AIMO3Solver:
    """
    Solver for IMO-level mathematical problems using GPT-OSS-120B.

    Features:
    - 8 parallel solution attempts
    - Tool-Integrated Reasoning (Python code execution)
    - Entropy-weighted voting for answer selection
    - Early stopping when 4 attempts agree
    """

    def __init__(self, client, sandbox_pool):
        """
        Initialize solver.

        Args:
            client: OpenAI-compatible client for vLLM
            sandbox_pool: Queue of Jupyter sandbox instances
        """
        self.client = client
        self.sandbox_pool = sandbox_pool
        self.model = "gpt-oss"

    def solve(self, problem: str, timeout: int = None) -> int:
        """
        Solve a mathematical problem.

        Args:
            problem: Problem text
            timeout: Maximum time in seconds (default: Config.BASE_PROBLEM_TIMEOUT)

        Returns:
            Answer as integer (0-99999)
        """
        if timeout is None:
            timeout = Config.BASE_PROBLEM_TIMEOUT

        deadline = time.time() + timeout
        results = []
        stop_event = threading.Event()

        with ThreadPoolExecutor(max_workers=Config.ATTEMPTS * 2) as executor:
            futures = [
                executor.submit(
                    self._process_attempt,
                    problem,
                    i,
                    deadline,
                    stop_event
                )
                for i in range(Config.ATTEMPTS)
            ]

            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result and result.get('Answer') is not None:
                        results.append(result)

                        # Check for early stopping
                        early_answer = check_early_stop(results, Config.EARLY_STOP)
                        if early_answer is not None:
                            stop_event.set()
                            return early_answer
                except Exception:
                    pass

                if time.time() > deadline:
                    stop_event.set()
                    break

        # Select answer from all results
        answer = select_answer(results)
        return answer if answer is not None else 0

    def _process_attempt(
        self,
        problem: str,
        attempt_id: int,
        deadline: float,
        stop_event: threading.Event
    ) -> Optional[Dict[str, Any]]:
        """
        Process a single solution attempt.

        Args:
            problem: Problem text
            attempt_id: Attempt identifier
            deadline: Deadline timestamp
            stop_event: Event to signal early stopping

        Returns:
            Result dict with 'Answer' and 'Entropy', or None
        """
        if stop_event.is_set() or time.time() > deadline:
            return None

        messages = [
            {"role": "system", "content": Config.SYSTEM_PROMPT},
            {"role": "user", "content": problem}
        ]

        all_logprobs = []
        max_iterations = 10

        for iteration in range(max_iterations):
            if stop_event.is_set() or time.time() > deadline:
                break

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=Config.TEMPERATURE,
                    min_p=Config.MIN_P,
                    max_tokens=Config.MAX_TOKENS,
                    logprobs=True,
                    top_logprobs=5,
                )

                content = response.choices[0].message.content

                # Collect logprobs
                if hasattr(response.choices[0], 'logprobs') and response.choices[0].logprobs:
                    for token_info in response.choices[0].logprobs.content:
                        if hasattr(token_info, 'top_logprobs'):
                            probs = [2 ** lp.logprob for lp in token_info.top_logprobs]
                            all_logprobs.append(probs)

                # Check for final answer
                answer = self._extract_answer(content)
                if answer is not None:
                    return {
                        'Answer': answer,
                        'logprobs': all_logprobs,
                        'attempt_id': attempt_id
                    }

                # Check for code execution
                code = self._extract_code(content)
                if code:
                    output = self._execute_code(code)
                    messages.append({"role": "assistant", "content": content})
                    messages.append({"role": "user", "content": f"Code output:\n{output}"})
                else:
                    messages.append({"role": "assistant", "content": content})
                    messages.append({"role": "user", "content": "Continue solving."})

            except Exception:
                break

        return None

    def _extract_answer(self, text: str) -> Optional[int]:
        """Extract answer from \\boxed{} format."""
        patterns = [
            r'\\boxed\{(\d+)\}',
            r'\\boxed\s*\{(\d+)\}',
            r'boxed\{(\d+)\}',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                try:
                    answer = int(matches[-1])
                    if 0 <= answer <= 99999:
                        return answer
                except ValueError:
                    pass
        return None

    def _extract_code(self, text: str) -> Optional[str]:
        """Extract Python code from response."""
        patterns = [
            r'```python\n(.*?)```',
            r'```\n(.*?)```',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            if matches:
                return matches[-1].strip()
        return None

    def _execute_code(self, code: str) -> str:
        """Execute code in sandbox and return output."""
        try:
            sandbox = self.sandbox_pool.get(timeout=5)
            try:
                result = sandbox.execute(code, timeout=6)
                return result[:2000] if result else "No output"
            finally:
                self.sandbox_pool.put(sandbox)
        except Exception as e:
            return f"Error: {str(e)}"
