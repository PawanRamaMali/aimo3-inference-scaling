"""Configuration settings for AIMO3 inference."""

class Config:
    """Best configuration (V40 - 42/50)."""

    # Model settings
    # Kaggle: https://www.kaggle.com/models/danielhanchen/gpt-oss-120b
    # HuggingFace: https://huggingface.co/unsloth/gpt-oss-120B
    MODEL_PATH = "danielhanchen/gpt-oss-120b"
    CONTEXT_TOKENS = 65536
    KV_CACHE_DTYPE = "fp8_e4m3"
    GPU_MEMORY_UTILIZATION = 0.96
    MAX_NUM_SEQS = 256

    # Sampling parameters
    TEMPERATURE = 1.0
    MIN_P = 0.02
    TOP_P = None  # Not used in best config
    MAX_TOKENS = 16384

    # Voting parameters
    ATTEMPTS = 8
    EARLY_STOP = 4

    # Timeouts
    BASE_PROBLEM_TIMEOUT = 270  # seconds
    HIGH_PROBLEM_TIMEOUT = 900  # for hard problems
    NOTEBOOK_LIMIT = 17400  # 4.8 hours total

    # Prompts (Simple - proven to work best)
    SYSTEM_PROMPT = (
        "You are a world-class IMO competitor. "
        "The final answer must be 0-99999. "
        "Place answer inside \\boxed{}."
    )

    TOOL_PROMPT = (
        "Use this tool to execute Python code. "
        "Use print() to output results."
    )

    PREFERENCE_PROMPT = "You have access to math, numpy, sympy."

    # Entropy weighting parameters
    ENTROPY_DECAY = 0.995
    ENTROPY_MEAN_WEIGHT = 0.3
    ENTROPY_POSITION_WEIGHT = 0.4
    ENTROPY_VARIANCE_WEIGHT = 0.2
    ENTROPY_HIGH_PENALTY_WEIGHT = 0.3
    ENTROPY_HIGH_THRESHOLD = 2.0


class VLLMConfig:
    """vLLM server configuration."""

    @staticmethod
    def get_server_cmd(model_path: str) -> list:
        return [
            'python', '-m', 'vllm.entrypoints.openai.api_server',
            '--model', model_path,
            '--served-model-name', 'gpt-oss',
            '--tensor-parallel-size', '1',
            '--max-num-seqs', str(Config.MAX_NUM_SEQS),
            '--gpu-memory-utilization', str(Config.GPU_MEMORY_UTILIZATION),
            '--dtype', 'auto',
            '--kv-cache-dtype', Config.KV_CACHE_DTYPE,
            '--max-model-len', str(Config.CONTEXT_TOKENS),
            '--enable-prefix-caching',
            '--async-scheduling',
            '--disable-log-stats',
        ]
