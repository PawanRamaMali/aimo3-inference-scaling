# Scaling Inference-Time Compute for Mathematical Reasoning

**AIMO Progress Prize 3 - Writeup Submission**

Author: Pawan Mali

## Overview

This repository contains the inference pipeline and experimental findings from 60+ experiments on IMO-level mathematical problems using GPT-OSS-120B. Our best configuration achieved 42/50 on the public leaderboard.

## Key Results

| Configuration | Score | Notes |
|--------------|-------|-------|
| Simple prompts + weighted entropy (V40) | **42/50** | Best result |
| Baseline with top_p=0.8 (V125) | 41/50 | Stable |
| Verbose prompts (V127) | 33/50 | -9 regression |
| Bayesian voting (V142) | 30/50 | -11 regression |

## Key Findings

### What Works

1. **Simple 3-line prompts** outperform complex instructions (+9 points)
2. **Temperature 1.0** with voting beats lower temperatures
3. **5-component weighted entropy** beats simple mean (+6 points)
4. **8 parallel attempts** with early stopping at 4 consensus
5. **65K context** (not 131K - larger context reduces concurrency)

### What Doesn't Work

- Verbose/structured prompts (-9 points)
- Self-refinement (-4 points)
- Answer verification (0 improvement)
- Bayesian voting with VOI (-11 points)
- Combining multiple changes simultaneously

## Architecture

```
Problem Input
     │
     ▼
┌─────────────────────┐
│  vLLM Server        │
│  GPT-OSS-120B       │
│  FP8 KV Cache       │
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  8 Parallel         │
│  Solution Attempts  │
│  (Tool-Integrated)  │
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  Entropy-Weighted   │
│  Voting             │
│  (5-component)      │
└─────────────────────┘
     │
     ▼
   Answer
```

## Configuration

### Best Configuration (V40 - 42/50)

```python
# Model
model = "openai/gpt-oss-120b"
context_tokens = 65536
kv_cache_dtype = "fp8_e4m3"

# Sampling
temperature = 1.0
min_p = 0.02

# Voting
attempts = 8
early_stop = 4
voting = "weighted_entropy"  # weight = 1.0 / max(entropy, 1e-9)

# Simple prompts
system_prompt = (
    "You are a world-class IMO competitor. "
    "The final answer must be 0-99999. "
    "Place answer inside \\boxed{}."
)
```

### Entropy-Weighted Voting

```python
def compute_weighted_entropy(logprobs):
    """
    5-component weighted entropy calculation:
    1. Mean entropy (30%)
    2. Variance penalty (20%)
    3. Position-weighted entropy (40%) - emphasizes final tokens
    4. High-entropy penalty (penalize uncertain stretches)
    5. Low-entropy streak bonus (reward consistent confidence)
    """
    entropies = [-sum(p * log(p) for p in probs) for probs in logprobs]
    n = len(entropies)

    # Position weighting - exponential decay emphasizing end
    decay = 0.995
    weights = [decay ** (n - i - 1) for i in range(n)]
    position_weighted = sum(e * w for e, w in zip(entropies, weights)) / sum(weights)

    mean_ent = sum(entropies) / n
    variance = sum((e - mean_ent)**2 for e in entropies) / n

    high_ent_ratio = sum(1 for e in entropies if e > 2.0) / n

    # Compute final weighted entropy
    weighted_entropy = (
        0.3 * mean_ent +
        0.4 * position_weighted +
        0.2 * sqrt(variance) +
        0.3 * high_ent_ratio * 3.0
    )

    return weighted_entropy

def select_answer(results):
    """Select answer with highest confidence-weighted votes."""
    ans_weights = defaultdict(float)

    for r in results:
        if r['Answer'] is not None:
            entropy = compute_weighted_entropy(r['logprobs'])
            ans_weights[r['Answer']] += 1.0 / max(entropy, 1e-9)

    return max(ans_weights, key=ans_weights.get)
```

## vLLM Server Configuration

```python
cmd = [
    'python', '-m', 'vllm.entrypoints.openai.api_server',
    '--model', '/path/to/gpt-oss-120b',
    '--served-model-name', 'gpt-oss',
    '--tensor-parallel-size', '1',
    '--max-num-seqs', '256',
    '--gpu-memory-utilization', '0.96',
    '--dtype', 'auto',
    '--kv-cache-dtype', 'fp8_e4m3',
    '--max-model-len', '65536',
    '--enable-prefix-caching',
]
```

## Experimental Timeline

| Date | Version | Score | Key Change |
|------|---------|-------|------------|
| Feb 6 | V40 | **42/50** | Simple prompts + weighted entropy |
| Feb 7 | V41 | 34/50 | temp=0.5 (regression) |
| Mar 19 | V125 | 41/50 | temp=1.0 + top_p=0.8 |
| Mar 22 | V127 | 33/50 | Verbose prompts (regression) |
| Mar 29 | V135 | 35/50 | 131K context (regression) |
| Apr 5 | V142 | 30/50 | Bayesian voting (regression) |
| Apr 6 | V143 | 41/50 | Baseline restored |

## Repository Structure

```
.
├── README.md
├── LICENSE                    # MIT License
├── requirements.txt
├── inference/
│   ├── __init__.py           # Module exports
│   ├── config.py             # Configuration settings
│   ├── solver.py             # Main solver class
│   ├── voting.py             # Entropy-weighted voting
│   └── sandbox.py            # Jupyter sandbox for code execution
├── notebooks/
│   └── demo.ipynb            # Google Colab demo notebook
└── experiments/
    └── version_history.md    # Detailed experiment log
```

## Requirements

- Python 3.10+
- vLLM 0.6.6+
- NVIDIA H100 (80GB)
- ~4.8 hours runtime for 50 problems

## Links

- **Kaggle Notebook:** https://www.kaggle.com/code/pawanmali/aimo3-gpt-oss-120b
- **Kaggle Writeup:** https://www.kaggle.com/code/pawanmali/chasing-47-50-aimo3-journey-of-50-experiments
- **Google Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PawanRamaMali/aimo3-inference-scaling/blob/master/notebooks/demo.ipynb)
- **Model (Kaggle):** https://www.kaggle.com/models/danielhanchen/gpt-oss-120b
- **Model (HuggingFace):** https://huggingface.co/unsloth/gpt-oss-120B

## Acknowledgments

- AIMO Prize Foundation for organizing the competition
- Daniel Hanchen / Unsloth for GPT-OSS-120B model
- XTX Markets for sponsoring the prize
- Kaggle community (nihilisticneuralnet, huikang, datasciencegrad) for public notebooks

## License

MIT License
