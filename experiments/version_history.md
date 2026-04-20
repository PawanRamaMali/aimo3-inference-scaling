# AIMO3 Experiment Version History

Detailed log of 60+ experiments across 157+ notebook versions.

## Best Results

| Version | Score | Configuration |
|---------|-------|---------------|
| V40 | **42/50** | Simple prompts + weighted entropy |
| V125 | 41/50 | temp=1.0 + top_p=0.8 |
| V143 | 41/50 | Baseline restored |

## Key Experiments

### Phase 1: Baseline Establishment (V1-V40)

| Version | Score | Change | Result |
|---------|-------|--------|--------|
| V1 | 28/50 | Initial baseline | - |
| V10 | 32/50 | Added code execution | +4 |
| V20 | 36/50 | 8 parallel attempts | +4 |
| V30 | 38/50 | Early stopping at 4 | +2 |
| V40 | **42/50** | Simple prompts + weighted entropy | +4 |

### Phase 2: Temperature Experiments (V41-V60)

| Version | Score | Change | Result |
|---------|-------|--------|--------|
| V41 | 34/50 | temp=0.5 | -8 regression |
| V42 | 36/50 | temp=0.7 | -6 regression |
| V45 | 38/50 | temp=0.9 | -4 regression |
| V50 | 40/50 | temp=1.0 restored | -2 from best |

**Finding:** Temperature 1.0 with voting is optimal.

### Phase 3: Prompt Engineering (V61-V90)

| Version | Score | Change | Result |
|---------|-------|--------|--------|
| V65 | 35/50 | Verbose system prompt | -7 regression |
| V70 | 33/50 | Chain-of-thought instructions | -9 regression |
| V75 | 36/50 | Step-by-step format | -6 regression |
| V80 | 40/50 | Minimal prompts | -2 from best |
| V85 | 41/50 | 3-line simple prompt | -1 from best |

**Finding:** Simple 3-line prompts outperform complex instructions by 9 points.

### Phase 4: Voting Strategies (V91-V120)

| Version | Score | Change | Result |
|---------|-------|--------|--------|
| V95 | 36/50 | Simple majority voting | -6 from weighted |
| V100 | 38/50 | Mean entropy weighting | -4 from weighted |
| V105 | 40/50 | Position-weighted entropy | -2 from best |
| V110 | 41/50 | 5-component weighted | -1 from best |
| V115 | 38/50 | Bayesian confidence | -4 regression |

**Finding:** 5-component weighted entropy beats simple mean by 6 points.

### Phase 5: Context Optimization (V121-V140)

| Version | Score | Change | Result |
|---------|-------|--------|--------|
| V125 | 41/50 | 65K context + top_p=0.8 | Stable |
| V127 | 33/50 | Verbose prompts again | -9 regression |
| V130 | 38/50 | 98K context | -4 regression |
| V135 | 35/50 | 131K context | -7 regression |

**Finding:** 65K context (not 131K) is optimal - larger reduces concurrency.

### Phase 6: Advanced Voting (V141-V150)

| Version | Score | Change | Result |
|---------|-------|--------|--------|
| V142 | 30/50 | Bayesian VOI voting | -11 regression |
| V143 | 41/50 | Baseline restored | Stable |
| V145 | 39/50 | GenSelect voting | -2 from baseline |
| V148 | 38/50 | Combined strategies | -3 from baseline |

**Finding:** Simple entropy-weighted voting beats complex Bayesian approaches.

## Failed Experiments Summary

| Approach | Score Impact | Conclusion |
|----------|-------------|------------|
| Verbose prompts | -9 points | Simpler is better |
| Self-refinement | -4 points | Single-shot works better |
| Answer verification | 0 improvement | No benefit |
| Bayesian voting | -11 points | Overcomplicated |
| 131K context | -7 points | Reduces concurrency |
| Low temperature | -8 points | Diversity helps voting |

## Winning Configuration (V40)

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
voting = "weighted_entropy"

# Prompts
system_prompt = (
    "You are a world-class IMO competitor. "
    "The final answer must be 0-99999. "
    "Place answer inside \\boxed{}."
)
```

## Lessons Learned

1. **Simplicity wins**: Complex prompts and voting strategies consistently underperformed
2. **Diversity matters**: High temperature (1.0) with voting beats low temperature
3. **Early stopping works**: 4/8 consensus provides good balance
4. **Context tradeoffs**: Larger context reduces concurrency, hurting overall throughput
5. **Entropy weighting**: Position-weighted entropy emphasizing final tokens is key
