# swarm_examples.py - Practical usage patterns for the live swarm brain
from swarm_core import swarm, Pulse
import numpy as np

# Example 1: Vectorized computation
def demo_vectorization():
    print("🔄 Breathing vectorization...")
    swarm.breathe("""
    import numpy as np
    def fast_sum(n):
        return np.arange(n).sum()
    result = fast_sum(1000000)
    print(f"Vectorized sum: {result}")
    """)

# Example 2: Live function evolution
def demo_function_evolution():
    print("🧬 Evolving functions live...")
    
    # First iteration
    swarm.breathe("""
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    """)
    
    # Evolve to memoized version
    swarm.breathe("""
    memo = {}
    def fibonacci(n):
        if n in memo:
            return memo[n]
        if n <= 1:
            return n
        memo[n] = fibonacci(n-1) + fibonacci(n-2)
        return memo[n]
    """)

# Example 3: Data structure transformation
def demo_data_structures():
    print("🏗️ Building data structures...")
    swarm.breathe("""
    class LiveGraph:
        def __init__(self):
            self.nodes = set()
            self.edges = {}
        
        def add_node(self, node):
            self.nodes.add(node)
        
        def add_edge(self, from_node, to_node, weight=1):
            if from_node not in self.edges:
                self.edges[from_node] = {}
            self.edges[from_node][to_node] = weight
    
    graph = LiveGraph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_edge("A", "B", 5)
    print(f"Graph created with {len(graph.nodes)} nodes")
    """)

# Example 4: Reactive programming pattern
def demo_reactive():
    print("⚡ Setting up reactive patterns...")
    
    # Create a reactive variable
    swarm.breathe("""
    class ReactiveVar:
        def __init__(self, initial_value):
            self._value = initial_value
            self._callbacks = []
        
        @property
        def value(self):
            return self._value
        
        @value.setter
        def value(self, new_value):
            old_value = self._value
            self._value = new_value
            for callback in self._callbacks:
                callback(old_value, new_value)
        
        def watch(self, callback):
            self._callbacks.append(callback)
    
    counter = ReactiveVar(0)
    counter.watch(lambda old, new: print(f"Counter changed: {old} -> {new}"))
    """)

# Example 5: Live debugging and inspection
def demo_live_debug():
    print("🐛 Live debugging...")
    swarm.breathe("""
    def inspect_environment():
        print("=== Live Environment Inspection ===")
        for name, obj in globals().items():
            if not name.startswith('_'):
                print(f"{name}: {type(obj).__name__}")
        print("==================================")
    
    inspect_environment()
    """)

# Example 6: Performance monitoring
def demo_performance():
    print("📊 Performance monitoring...")
    swarm.breathe("""
    import time
    import functools
    
    def timer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"{func.__name__} took {end - start:.4f} seconds")
            return result
        return wrapper
    
    @timer
    def slow_function():
        return sum(i for i in range(100000))
    
    result = slow_function()
    """)

if __name__ == "__main__":
    print("🚀 Swarm Brain Examples - Live Execution Demo")
    print("=" * 50)
    
    # Run all demos
    demo_vectorization()
    demo_function_evolution()
    demo_data_structures()
    demo_reactive()
    demo_live_debug()
    demo_performance()
    
    print("\n✨ All examples executed live in memory!")
    print("Your swarm brain is now enhanced with practical patterns.")
