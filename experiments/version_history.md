# AIMO3 Experiment Version History

Complete log of 60+ experiments across 157+ notebook versions.

## Summary Statistics

- **Total Versions:** 157+
- **Best Score:** 42/50 (V40)
- **Mean Score:** ~40/50
- **Experiments Documented:** 60+

---

## Phase 1: Initial Setup & Baseline (V1-V15)

| Version | Score | Configuration | Learning |
|---------|-------|---------------|----------|
| V1 | 25/50 | Basic GPT-OSS-120B, temp=0.7 | Initial baseline established |
| V2 | 26/50 | Added system prompt | Minimal improvement |
| V3 | 24/50 | Longer system prompt | Regression - shorter is better |
| V4 | 27/50 | temp=0.8 | Slight improvement |
| V5 | 28/50 | Added code execution | +1 from code capability |
| V6 | 27/50 | Structured output format | No improvement |
| V7 | 29/50 | 2 parallel attempts | +1 from parallelism |
| V8 | 28/50 | 3 parallel attempts | Diminishing returns |
| V9 | 30/50 | 4 parallel attempts + majority vote | +2 from voting |
| V10 | 32/50 | Improved code sandbox | +2 from reliable execution |
| V11 | 31/50 | Added timeout handling | Slight regression |
| V12 | 33/50 | 6 parallel attempts | +1 from more attempts |
| V13 | 32/50 | Answer verification step | No improvement |
| V14 | 34/50 | 8 parallel attempts | +1 from more diversity |
| V15 | 33/50 | Added self-refinement | -1 regression |

**Key Learning:** More parallel attempts help, but self-refinement hurts.

---

## Phase 2: Voting Strategies (V16-V30)

| Version | Score | Configuration | Learning |
|---------|-------|---------------|----------|
| V16 | 34/50 | Simple majority voting | Baseline voting |
| V17 | 35/50 | Weighted by confidence | +1 from weighting |
| V18 | 34/50 | Weighted by answer length | No improvement |
| V19 | 36/50 | Entropy-based weighting | +1 from entropy |
| V20 | 36/50 | Mean entropy weighting | Stable |
| V21 | 35/50 | Max entropy penalty | -1 regression |
| V22 | 37/50 | Position-weighted entropy | +1 from emphasizing end tokens |
| V23 | 36/50 | Variance penalty added | Slight regression |
| V24 | 38/50 | Combined 3-component entropy | +1 from combination |
| V25 | 37/50 | Added streak bonus | Mixed results |
| V26 | 38/50 | Early stopping at 6 consensus | Faster, same accuracy |
| V27 | 39/50 | Early stopping at 5 consensus | Good balance |
| V28 | 38/50 | Early stopping at 3 consensus | Too aggressive |
| V29 | 40/50 | Early stopping at 4 consensus | Optimal threshold |
| V30 | 38/50 | Dynamic early stopping | Overcomplicated |

**Key Learning:** Early stopping at 4/8 consensus is optimal. Simple rules beat complex ones.

---

## Phase 3: Prompt Engineering (V31-V45)

| Version | Score | Configuration | Learning |
|---------|-------|---------------|----------|
| V31 | 39/50 | Detailed IMO instructions | -1 from baseline |
| V32 | 37/50 | Chain-of-thought prompt | -3 regression |
| V33 | 36/50 | Step-by-step format | -4 regression |
| V34 | 38/50 | Mathematical notation emphasis | -2 regression |
| V35 | 40/50 | Minimal 2-line prompt | Back to baseline |
| V36 | 41/50 | "World-class IMO competitor" | +1 from identity priming |
| V37 | 40/50 | Added "think carefully" | No improvement |
| V38 | 39/50 | Added "verify your answer" | -1 regression |
| V39 | 41/50 | Removed verification instruction | Back to +1 |
| V40 | **42/50** | Simple 3-line prompt + 5-component entropy | **BEST RESULT** |
| V41 | 34/50 | temp=0.5 | -8 regression - diversity matters |
| V42 | 36/50 | temp=0.7 | -6 regression |
| V43 | 38/50 | temp=0.9 | -4 regression |
| V44 | 40/50 | temp=1.0 restored | Back to -2 from best |
| V45 | 39/50 | temp=1.1 | -1 regression - too random |

**Key Learning:** Simple 3-line prompts outperform complex instructions by 9 points. Temperature 1.0 is optimal for voting.

---

## Phase 4: Model Configuration (V46-V60)

| Version | Score | Configuration | Learning |
|---------|-------|---------------|----------|
| V46 | 40/50 | 32K context | -2 from best |
| V47 | 41/50 | 48K context | -1 from best |
| V48 | 42/50 | 65K context | Matches best |
| V49 | 40/50 | 98K context | -2 regression |
| V50 | 38/50 | 131K context | -4 regression - concurrency issue |
| V51 | 41/50 | Back to 65K | Restored |
| V52 | 40/50 | min_p=0.01 | -1 regression |
| V53 | 41/50 | min_p=0.02 | Stable |
| V54 | 40/50 | min_p=0.05 | -1 regression |
| V55 | 39/50 | top_p=0.9 | -2 regression |
| V56 | 40/50 | top_p=0.95 | -1 regression |
| V57 | 41/50 | No top_p, min_p=0.02 only | Best sampling config |
| V58 | 40/50 | Added repetition penalty | -1 regression |
| V59 | 41/50 | Removed repetition penalty | Restored |
| V60 | 40/50 | Increased max_tokens to 24K | Timeout issues |

**Key Learning:** 65K context optimal (not 131K). min_p=0.02 works best. Larger context reduces concurrency.

---

## Phase 5: Code Execution Improvements (V61-V75)

| Version | Score | Configuration | Learning |
|---------|-------|---------------|----------|
| V61 | 41/50 | 8 sandbox pool | Stable |
| V62 | 40/50 | 16 sandbox pool | No improvement |
| V63 | 41/50 | 6 second code timeout | Stable |
| V64 | 39/50 | 10 second code timeout | Slower, same accuracy |
| V65 | 40/50 | Added numpy to sandbox | Minor improvement |
| V66 | 41/50 | Added sympy to sandbox | Stable |
| V67 | 40/50 | Added scipy | No improvement |
| V68 | 41/50 | Reverted to math+numpy+sympy | Clean config |
| V69 | 39/50 | Multiple code blocks per turn | -2 regression |
| V70 | 40/50 | Single code block only | Better |
| V71 | 41/50 | Code output truncation at 2000 chars | Good balance |
| V72 | 40/50 | Code output at 5000 chars | No improvement |
| V73 | 41/50 | Back to 2000 chars | Stable |
| V74 | 40/50 | Added execution retry | Overcomplicated |
| V75 | 41/50 | Removed retry logic | Simpler is better |

**Key Learning:** Simple code execution setup works best. Don't overcomplicate.

---

## Phase 6: Advanced Voting Attempts (V76-V90)

| Version | Score | Configuration | Learning |
|---------|-------|---------------|----------|
| V76 | 40/50 | Bayesian confidence | -1 regression |
| V77 | 38/50 | Thompson sampling | -3 regression |
| V78 | 39/50 | UCB-style voting | -2 regression |
| V79 | 37/50 | Neural voting model | -4 regression |
| V80 | 40/50 | Back to weighted entropy | Restored |
| V81 | 39/50 | Answer clustering | -2 regression |
| V82 | 40/50 | Removed clustering | Restored |
| V83 | 38/50 | Multi-round voting | -3 regression |
| V84 | 39/50 | Confidence calibration | -2 regression |
| V85 | 41/50 | Simple entropy only | -1 from best |
| V86 | 40/50 | Added answer verification | -1 regression |
| V87 | 41/50 | Removed verification | Restored |
| V88 | 39/50 | Ensemble methods | -2 regression |
| V89 | 40/50 | Single model approach | Better |
| V90 | 41/50 | Baseline restored | Stable |

**Key Learning:** Advanced voting strategies consistently underperform simple weighted entropy.

---

## Phase 7: Scaling Experiments (V91-V110)

| Version | Score | Configuration | Learning |
|---------|-------|---------------|----------|
| V91 | 40/50 | 10 parallel attempts | +0 from 8 attempts |
| V92 | 41/50 | 12 parallel attempts | +0 |
| V93 | 40/50 | 16 parallel attempts | Memory issues |
| V94 | 41/50 | Back to 8 attempts | Optimal |
| V95 | 40/50 | 2x iterations per problem | Timeout issues |
| V96 | 39/50 | Adaptive timeout | Complicated |
| V97 | 40/50 | Fixed 270s timeout | Good balance |
| V98 | 41/50 | 300s timeout | Slight improvement |
| V99 | 40/50 | 360s timeout | Diminishing returns |
| V100 | 41/50 | Back to 270s | Optimal for 50 problems |
| V101 | 40/50 | Batch processing | No improvement |
| V102 | 41/50 | Sequential processing | Restored |
| V103 | 39/50 | Dynamic batching | Overcomplicated |
| V104 | 40/50 | Fixed batch size | No improvement |
| V105 | 41/50 | Single problem at a time | Best approach |
| V106 | 40/50 | Prefetching | No improvement |
| V107 | 41/50 | No prefetching | Simpler |
| V108 | 40/50 | GPU memory 0.98 | OOM issues |
| V109 | 41/50 | GPU memory 0.96 | Stable |
| V110 | 41/50 | GPU memory 0.94 | Slightly slower |

**Key Learning:** 8 attempts, 270s timeout, 0.96 GPU utilization is optimal.

---

## Phase 8: Final Optimization Attempts (V111-V130)

| Version | Score | Configuration | Learning |
|---------|-------|---------------|----------|
| V111 | 41/50 | FP8 KV cache | Good memory efficiency |
| V112 | 40/50 | FP16 KV cache | Slower |
| V113 | 41/50 | Back to FP8 | Best |
| V114 | 40/50 | Chunked prefill | No improvement |
| V115 | 41/50 | Standard prefill | Stable |
| V116 | 40/50 | Speculative decoding | Compatibility issues |
| V117 | 41/50 | Standard decoding | Reliable |
| V118 | 40/50 | Async scheduling disabled | -1 |
| V119 | 41/50 | Async scheduling enabled | Optimal |
| V120 | 40/50 | Prefix caching disabled | -1 |
| V121 | 41/50 | Prefix caching enabled | Best |
| V122 | 40/50 | Different rope scaling | No improvement |
| V123 | 41/50 | Default rope scaling | Stable |
| V124 | 40/50 | Adjusted attention | No improvement |
| V125 | 41/50 | temp=1.0 + top_p=0.8 | Stable alternative |
| V126 | 40/50 | top_p=0.7 | -1 |
| V127 | 33/50 | Verbose prompts again | -8 regression confirmed |
| V128 | 40/50 | Restored simple prompts | Back to normal |
| V129 | 41/50 | Final optimization | Stable |
| V130 | 38/50 | 98K context test | -3 regression |

**Key Learning:** FP8 KV cache, prefix caching, async scheduling are optimal vLLM settings.

---

## Phase 9: Context Window Experiments (V131-V145)

| Version | Score | Configuration | Learning |
|---------|-------|---------------|----------|
| V131 | 39/50 | 80K context | -2 |
| V132 | 40/50 | 72K context | -1 |
| V133 | 41/50 | 65K context | Optimal |
| V134 | 39/50 | 100K context | -2 |
| V135 | 35/50 | 131K context | -6 severe regression |
| V136 | 40/50 | Back to 65K | Restored |
| V137 | 39/50 | Variable context | Complicated |
| V138 | 40/50 | Fixed 65K | Simpler |
| V139 | 41/50 | Final context config | Stable |
| V140 | 40/50 | Max_num_seqs=512 | Memory issues |
| V141 | 41/50 | Max_num_seqs=256 | Optimal |
| V142 | 30/50 | Bayesian VOI voting | -11 severe regression |
| V143 | 41/50 | Restored weighted entropy | Back to normal |
| V144 | 40/50 | Minor prompt tweaks | No improvement |
| V145 | 39/50 | GenSelect voting | -2 |

**Key Learning:** 65K context is optimal. 131K reduces concurrency and hurts performance.

---

## Phase 10: Final Experiments (V146-V157+)

| Version | Score | Configuration | Learning |
|---------|-------|---------------|----------|
| V146 | 40/50 | Adjusted entropy weights | -1 |
| V147 | 41/50 | Restored V40 weights | Stable |
| V148 | 38/50 | GenSelect + entropy | -3 regression |
| V149 | 40/50 | Pure entropy voting | -1 |
| V150 | 41/50 | 5-component entropy | Optimal |
| V151 | 40/50 | 6-component entropy | Overcomplicated |
| V152 | 41/50 | Back to 5-component | Best |
| V153 | 40/50 | Different decay rate | -1 |
| V154 | 41/50 | decay=0.995 | Optimal |
| V155 | 40/50 | decay=0.99 | -1 |
| V156 | 41/50 | Final configuration | Stable |
| V157+ | 40-41/50 | Various minor tests | No improvements found |

**Key Learning:** The V40 configuration remains optimal. No improvements found in 117+ subsequent versions.

---

## Best Configuration (V40 - 42/50)

```python
# Model
model = "openai/gpt-oss-120b"
context_tokens = 65536
kv_cache_dtype = "fp8_e4m3"
gpu_memory_utilization = 0.96

# Sampling
temperature = 1.0
min_p = 0.02

# Voting
attempts = 8
early_stop = 4
voting = "5-component weighted entropy"
entropy_decay = 0.995
entropy_weights = {
    "mean": 0.3,
    "position": 0.4,
    "variance": 0.2,
    "high_penalty": 0.3
}

# Prompts
system_prompt = (
    "You are a world-class IMO competitor. "
    "The final answer must be 0-99999. "
    "Place answer inside \\boxed{}."
)

# Timeout
problem_timeout = 270  # seconds
```

---

## Failed Experiments Summary

| Approach | Best Score | Regression | Conclusion |
|----------|-----------|------------|------------|
| Verbose prompts | 33/50 | -9 | Simpler prompts work better |
| Bayesian VOI voting | 30/50 | -12 | Overcomplicated, unreliable |
| Self-refinement | 38/50 | -4 | Single-shot works better |
| 131K context | 35/50 | -7 | Reduces concurrency |
| Low temperature | 34/50 | -8 | Diversity helps voting |
| Thompson sampling | 38/50 | -4 | Simple voting wins |
| Answer verification | 40/50 | -2 | No benefit, adds latency |
| Neural voting | 37/50 | -5 | Simple heuristics win |

---

## Key Insights

### What Works
1. **Simple 3-line prompts** - Complex instructions confuse the model
2. **Temperature 1.0** - Diversity improves voting accuracy
3. **5-component weighted entropy** - Position weighting is crucial
4. **8 parallel attempts** - Optimal diversity/throughput balance
5. **Early stopping at 4** - Good consensus threshold
6. **65K context** - Best concurrency/capability balance
7. **FP8 KV cache** - Memory efficient without accuracy loss

### What Doesn't Work
1. **Verbose prompts** - Consistently hurt performance
2. **Bayesian methods** - Overcomplicated, worse results
3. **Self-refinement** - Model second-guesses correct answers
4. **Large context** - Reduces parallel throughput
5. **Low temperature** - Reduces diversity, hurts voting
6. **Complex voting** - Simple weighted voting wins

### The "Simplicity Principle"
Across 157+ versions, the consistent finding is that simpler approaches outperform complex ones:
- Simple prompts > Verbose instructions
- Simple voting > Bayesian/ML voting
- Single-shot > Multi-round refinement
- Fixed config > Adaptive strategies

The best score (42/50) was achieved in V40, and despite 117+ subsequent attempts, no improvement was found. This strongly suggests the solution is near-optimal for this model and task.
