"""Entropy-weighted voting for answer selection."""

from collections import defaultdict
from math import log, sqrt
from typing import List, Dict, Any, Optional

from .config import Config


def compute_entropy(probs: List[float]) -> float:
    """Compute entropy from probability distribution."""
    return -sum(p * log(p + 1e-10) for p in probs if p > 0)


def compute_weighted_entropy(logprobs: List[List[float]]) -> float:
    """
    Compute 5-component weighted entropy.

    Components:
    1. Mean entropy (30%) - average entropy across all tokens
    2. Position-weighted entropy (40%) - emphasizes final tokens
    3. Variance penalty (20%) - penalizes inconsistent confidence
    4. High-entropy penalty - penalizes uncertain stretches
    5. Low-entropy streak bonus - rewards consistent confidence

    Args:
        logprobs: List of probability distributions for each token

    Returns:
        Weighted entropy score (lower = more confident)
    """
    if not logprobs:
        return float('inf')

    # Convert logprobs to entropies
    entropies = [compute_entropy(probs) for probs in logprobs]
    n = len(entropies)

    if n == 0:
        return float('inf')

    # 1. Mean entropy
    mean_ent = sum(entropies) / n

    # 2. Position-weighted entropy (exponential decay emphasizing end)
    decay = Config.ENTROPY_DECAY
    weights = [decay ** (n - i - 1) for i in range(n)]
    weight_sum = sum(weights)
    position_weighted = sum(e * w for e, w in zip(entropies, weights)) / weight_sum

    # 3. Variance penalty
    variance = sum((e - mean_ent) ** 2 for e in entropies) / n
    std_dev = sqrt(variance)

    # 4. High-entropy penalty
    high_ent_count = sum(1 for e in entropies if e > Config.ENTROPY_HIGH_THRESHOLD)
    high_ent_ratio = high_ent_count / n

    # 5. Low-entropy streak bonus (find longest streak of low entropy)
    max_streak = 0
    current_streak = 0
    for e in entropies:
        if e < 1.0:  # Low entropy threshold
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    streak_bonus = -0.1 * (max_streak / n) if n > 0 else 0

    # Combine components
    weighted_entropy = (
        Config.ENTROPY_MEAN_WEIGHT * mean_ent +
        Config.ENTROPY_POSITION_WEIGHT * position_weighted +
        Config.ENTROPY_VARIANCE_WEIGHT * std_dev +
        Config.ENTROPY_HIGH_PENALTY_WEIGHT * high_ent_ratio * 3.0 +
        streak_bonus
    )

    return weighted_entropy


def select_answer(results: List[Dict[str, Any]]) -> Optional[int]:
    """
    Select best answer using entropy-weighted voting.

    Args:
        results: List of attempt results, each with 'Answer' and 'logprobs'

    Returns:
        Selected answer (integer) or None if no valid answers
    """
    ans_weights = defaultdict(float)

    for r in results:
        answer = r.get('Answer')
        if answer is not None:
            logprobs = r.get('logprobs', [])
            if logprobs:
                entropy = compute_weighted_entropy(logprobs)
            else:
                entropy = r.get('Entropy', 1.0)

            # Weight is inverse of entropy (lower entropy = higher weight)
            weight = 1.0 / max(entropy, 1e-9)
            ans_weights[answer] += weight

    if not ans_weights:
        return None

    return max(ans_weights, key=ans_weights.get)


def check_early_stop(results: List[Dict[str, Any]], threshold: int = 4) -> Optional[int]:
    """
    Check if we have enough consensus for early stopping.

    Args:
        results: List of attempt results
        threshold: Number of agreements needed (default: 4)

    Returns:
        Answer if consensus reached, None otherwise
    """
    vote_counts = defaultdict(int)

    for r in results:
        answer = r.get('Answer')
        if answer is not None:
            vote_counts[answer] += 1
            if vote_counts[answer] >= threshold:
                return answer

    return None
