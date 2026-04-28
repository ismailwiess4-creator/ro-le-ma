"""
ROUTE FINDER (RO) — Discovers connections between memories
"""
import re
from typing import List, Dict, Tuple
from itertools import combinations
from datetime import datetime

class RouteFinder:
    def __init__(self, grid):
        self.grid = grid
        self.thematic_keywords = {
            'anger': ['anger', 'rage', 'wrath', 'control', 'patience'],
            'knowledge': ['knowledge', 'wisdom', 'learning', 'study'],
            'beauty': ['beauty', 'beautiful', 'aesthetic', 'divine'],
            'faith': ['faith', 'belief', 'trust', 'certainty'],
            'ethics': ['ethics', 'moral', 'virtue', 'right', 'good'],
            'consciousness': ['consciousness', 'awareness', 'mind', 'soul'],
        }
        
    def find_all_routes(self, min_strength: float = 0.3) -> int:
        print("\n🔗 Finding routes...")
        memories = list(self.grid.memories.items())
        routes_found = 0
        for (id1, mem1), (id2, mem2) in combinations(memories, 2):
            strength, route_type = self._calculate_route_strength(mem1, mem2)
            if strength >= min_strength:
                self.grid.add_route(mem1.authority_key, mem2.authority_key, strength, route_type)
                routes_found += 1
        print(f"✅ Found {routes_found} routes")
        return routes_found
    
    def _calculate_route_strength(self, mem1, mem2) -> Tuple[float, str]:
        strengths, types = [], []
        # Semantic similarity
        words1 = set(mem1.content_key.split('_'))
        words2 = set(mem2.content_key.split('_'))
        overlap = len(words1 & words2) / max(len(words1 | words2), 1)
        if overlap > 0:
            strengths.append(overlap * 0.8)
            types.append('semantic')
        # Thematic
        theme_strength = self._check_thematic(mem1.text, mem2.text)
        if theme_strength > 0:
            strengths.append(theme_strength)
            types.append('thematic')
        # Same source
        if mem1.source == mem2.source:
            strengths.append(0.7)
            types.append('authoritative')
        if not strengths:
            return 0.0, 'none'
        max_idx = strengths.index(max(strengths))
        return strengths[max_idx], types[max_idx]
    
    def _check_thematic(self, text1: str, text2: str) -> float:
        t1, t2 = text1.lower(), text2.lower()
        max_strength = 0.0
        for theme, keywords in self.thematic_keywords.items():
            c1 = sum(1 for k in keywords if k in t1)
            c2 = sum(1 for k in keywords if k in t2)
            if c1 > 0 and c2 > 0:
                strength = (c1 + c2) / (len(keywords) * 2)
                max_strength = max(max_strength, strength)
        return max_strength
    
    def find_path(self, start_key: str, end_key: str, max_depth: int = 3) -> List[str]:
        if start_key not in self.grid.memory_index or end_key not in self.grid.memory_index:
            return []
        from collections import deque
        visited = set()
        queue = deque([(start_key, [start_key])])
        while queue:
            current, path = queue.popleft()
            if current == end_key:
                return path
            if current in visited or len(path) > max_depth:
                continue
            visited.add(current)
            for conn_key, strength, _ in self.grid.get_connected(current, min_strength=0.2):
                if conn_key not in visited:
                    queue.append((conn_key, path + [conn_key]))
        return []