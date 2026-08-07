"""
Fuzzy Logic package for the ID-Oto image enhancement system.

Implements a complete Mamdani Fuzzy Inference System:
Fuzzification -> Rule Evaluation -> Aggregation -> Defuzzification
"""

from .inference import fuzzy_logic

__all__ = ["fuzzy_logic"]