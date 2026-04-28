"""
LEVEL DETECTOR (LE) — Measures depth of understanding (0-4)
0:Raw | 1:Literal | 2:Interpreted | 3:Applied | 4:Transcendent
"""
import re
from typing import Tuple, List

class LevelDetector:
    def __init__(self):
        self.indicators = {
            0: [r'<.*?>', r'http[s]?://', r'\.(jpg|png|pdf)', 'DOCTYPE', 'html'],
            1: ['said that', 'states that', 'according to', 'in the text'],
            2: ['means that', 'implies', 'suggests', 'can be understood as', 'symbolizes'],
            3: ['therefore', 'thus', 'hence', 'practical implication', 'application'],
            4: ['universal truth', 'fundamental principle', 'essence of', 'consciousness', 'beyond']
        }
        self.transcendent_terms = ['truth', 'reality', 'being', 'existence', 'divine', 'infinite', 'eternal']
    
    def detect_level(self, text: str, source: str = "") -> Tuple[int, float, str]:
        text_lower = text.lower()
        # Level 0 check
        for pattern in self.indicators[0]:
            if re.search(pattern, text, re.IGNORECASE):
                return 0, 0.9, "Raw/unprocessed content"
        # Score each level
        scores = {}
        for level in range(1, 5):
            scores[level] = sum(1 for ind in self.indicators[level] if ind in text_lower) / max(len(self.indicators[level]), 1)
            if level >= 2: scores[level] *= 1.5  # Weight higher levels
        # Sentence complexity bonus
        sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
        avg_words = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        if avg_words > 25: scores[2] += 0.2
        if avg_words > 40: scores[3] += 0.3
        if avg_words > 60: scores[4] += 0.4
        # Transcendent terms bonus
        transcendent_count = sum(1 for t in self.transcendent_terms if t in text_lower)
        if transcendent_count >= 2: scores[4] += 0.3 * transcendent_count
        # Determine level
        if max(scores.values()) == 0:
            return 1, 0.5, "Default literal level"
        level = max(scores, key=scores.get)
        confidence = min(1.0, scores[level] * 0.8)
        explanations = {
            1: "Literal statement", 2: "Interpreted meaning", 
            3: "Applied wisdom", 4: "Transcendent truth"
        }
        return level, confidence, explanations.get(level, "Unknown")