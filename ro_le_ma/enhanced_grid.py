"""
Enhanced Universal Grid — With RO-LE-MA dimensions
RO: Routes (connections) | LE: Levels (depth) | MA: Maps (coordinates)
"""
import numpy as np
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class RO_LE_MA_Memory:
    """A memory with full RO-LE-MA dimensions"""
    text: str
    source: str
    timestamp: datetime
    authority_key: str
    content_key: str
    
    # 📚 RO (Routes) - Connections
    routes: Dict[str, float] = field(default_factory=dict)
    
    # 💡 LE (Levels) - Depth (0-4)
    depth_level: int = 1
    depth_confidence: float = 0.5
    depth_explanation: str = ""
    
    # 🎯 MA (Maps) - 3D coordinates
    map_coordinates: Tuple[float, float, float] = (0.5, 0.5, 0.5)
    map_domain: str = "unknown"
    
    access_count: int = 0
    last_accessed: datetime = None

class EnhancedROLEMAGrid:
    """5D Grid extended with RO-LE-MA dimensions"""
    
    def __init__(self, max_memories: int = 1000):
        self.max_memories = max_memories
        self.memories: Dict[str, RO_LE_MA_Memory] = {}
        self.memory_index: Dict[str, str] = {}  # key -> memory_id
        self.connection_matrix = np.zeros((max_memories, max_memories), dtype=np.float16)
        self.connection_types: Dict[Tuple[int, int], str] = {}
        self.level_assignments: Dict[str, int] = {}
        self.map_coordinates: Dict[str, Tuple[float, float, float]] = {}
        print("✅ Enhanced RO-LE-MA Grid initialized")
    
    def add_memory(self, memory: RO_LE_MA_Memory) -> str:
        memory_id = f"{len(self.memories)}_{datetime.now().timestamp()}"
        self.memories[memory_id] = memory
        self.memory_index[memory.authority_key] = memory_id
        self.memory_index[memory.content_key] = memory_id
        self.level_assignments[memory_id] = memory.depth_level
        self.map_coordinates[memory_id] = memory.map_coordinates
        print(f"✅ Added memory {memory_id[:8]} | Level {memory.depth_level} | {memory.map_domain}")
        return memory_id
    
    def add_route(self, from_key: str, to_key: str, strength: float, route_type: str = "semantic"):
        if from_key in self.memory_index and to_key in self.memory_index:
            from_id = self.memory_index[from_key]
            to_id = self.memory_index[to_key]
            i = int(from_id.split('_')[0])
            j = int(to_id.split('_')[0])
            if i < self.max_memories and j < self.max_memories:
                self.connection_matrix[i, j] = strength
                self.connection_matrix[j, i] = strength
                self.connection_types[(i, j)] = route_type
                self.connection_types[(j, i)] = route_type
                if from_id in self.memories:
                    self.memories[from_id].routes[to_key] = strength
                if to_id in self.memories:
                    self.memories[to_id].routes[from_key] = strength
                print(f"🔗 Route: {from_key[:30]} ←{strength:.2f}→ {to_key[:30]}")
    
    def get_connected(self, key: str, min_strength: float = 0.3) -> List[Tuple[str, float, str]]:
        if key not in self.memory_index:
            return []
        mem_id = self.memory_index[key]
        i = int(mem_id.split('_')[0])
        connections = []
        for j in range(min(len(self.memories), self.max_memories)):
            strength = self.connection_matrix[i, j]
            if strength >= min_strength and j != i:
                for k, v in self.memory_index.items():
                    if v.startswith(f"{j}_"):
                        connections.append((k, strength, self.connection_types.get((i, j), "unknown")))
                        break
        return sorted(connections, key=lambda x: x[1], reverse=True)[:10]
    
    def get_by_level(self, level: int) -> List[str]:
        return [mid for mid, lvl in self.level_assignments.items() if lvl == level]
    
    def get_in_map_region(self, domain_range: Tuple[float, float], 
                          time_range: Tuple[float, float],
                          certainty_range: Tuple[float, float]) -> List[str]:
        results = []
        for mem_id, coords in self.map_coordinates.items():
            x, y, z = coords
            if (domain_range[0] <= x <= domain_range[1] and
                time_range[0] <= y <= time_range[1] and
                certainty_range[0] <= z <= certainty_range[1]):
                results.append(mem_id)
        return results
    
    def get_stats(self) -> Dict:
        return {
            'total_memories': len(self.memories),
            'total_routes': int(np.count_nonzero(self.connection_matrix) // 2),
            'level_distribution': {lvl: len([m for m, l in self.level_assignments.items() if l == lvl]) for lvl in range(5)},
        }