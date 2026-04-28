"""
Quick Start Demo — RO-LE-MA in 10 lines
"""
from datetime import datetime
from src.ro_le_ma.enhanced_grid import EnhancedROLEMAGrid, RO_LE_MA_Memory
from src.ro_le_ma.route_finder import RouteFinder
from src.ro_le_ma.level_detector import LevelDetector

def main():
    print("🧠 RO-LE-MA Quick Start\n" + "="*50)
    grid = EnhancedROLEMAGrid()
    routes = RouteFinder(grid)
    levels = LevelDetector()
    
    # Add 3 memories from different traditions about "anger control"
    memories = [
        ("The Prophet said: The strong person controls themselves when angry", "sunnah.com", "islamic"),
        ("Stoic philosophy: You have power over your mind, not external events", "plato.stanford.edu", "philosophy"),
        ("Buddhist teaching: Anger is like holding a hot coal to throw", "buddhism.org", "spirituality"),
    ]
    
    for text, source, domain in memories:
        level, conf, exp = levels.detect_level(text, source)
        # Simple map coordinates: domain (x), time (y), certainty (z)
        x = {'islamic': 0.7, 'philosophy': 0.2, 'spirituality': 0.6}.get(domain, 0.5)
        mem = RO_LE_MA_Memory(
            text=text, source=source, timestamp=datetime.now(),
            authority_key=f"{domain}_teaching", content_key=f"anger_control_{domain}",
            depth_level=level, depth_confidence=conf, depth_explanation=exp,
            map_coordinates=(x, 0.3, 0.8), map_domain=domain
        )
        grid.add_memory(mem)
    
    # Find routes
    routes.find_all_routes(min_strength=0.2)
    
    # Query example
    print(f"\n🔍 Query: 'anger control'")
    connections = grid.get_connected("islamic_teaching", min_strength=0.2)
    for key, strength, rtype in connections:
        mem = grid.memories[grid.memory_index[key]]
        print(f"  🔗 {mem.map_domain:12} | Level {mem.depth_level} | {strength:.2f} ({rtype})")
        print(f"     \"{mem.text[:60]}...\"")
    
    print(f"\n📊 Stats: {grid.get_stats()}")
    print("\n✨ RO-LE-MA ready. Build wisdom-aware AI.")

if __name__ == "__main__":
    main()