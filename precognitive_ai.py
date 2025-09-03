# precognitive_ai.py - Simple precognitive AI for DevDollz: Atelier Edition

import time
import json
from typing import Dict, Any, List
from collections import defaultdict

class PrecognitiveAI:
    """Simple precognitive AI system for learning from user actions"""
    
    def __init__(self):
        self.action_history = []
        self.patterns = defaultdict(int)
        self.learned_responses = {}
        self.precog_active = True
        self.last_analysis = time.time()
    
    def learn_from_action(self, action_type: str, content: str, result: str):
        """Learn from a user action"""
        action_data = {
            "type": action_type,
            "content": content[:100],  # Truncate for memory efficiency
            "result": result[:100],
            "timestamp": time.time()
        }
        
        self.action_history.append(action_data)
        
        # Keep only last 100 actions
        if len(self.action_history) > 100:
            self.action_history.pop(0)
        
        # Update patterns
        self.patterns[action_type] += 1
        
        # Learn from successful actions
        if "success" in result.lower() or "error" not in result.lower():
            self.learned_responses[action_type] = result
    
    def predict_next_action(self) -> str:
        """Predict what the user might do next"""
        if not self.action_history:
            return "No prediction available"
        
        # Simple pattern-based prediction
        recent_actions = [a["type"] for a in self.action_history[-10:]]
        if recent_actions:
            most_common = max(set(recent_actions), key=recent_actions.count)
            return f"Likely next action: {most_common}"
        
        return "No clear pattern detected"
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights about user behavior"""
        if not self.action_history:
            return {"message": "No data available"}
        
        total_actions = len(self.action_history)
        action_counts = defaultdict(int)
        
        for action in self.action_history:
            action_counts[action["type"]] += 1
        
        return {
            "total_actions": total_actions,
            "action_distribution": dict(action_counts),
            "most_common_action": max(action_counts.items(), key=lambda x: x[1])[0] if action_counts else None,
            "prediction": self.predict_next_action()
        }
    
    def optimize_suggestion(self, action_type: str) -> str:
        """Suggest optimizations based on learned patterns"""
        if action_type in self.learned_responses:
            return f"Based on previous {action_type} actions, consider: {self.learned_responses[action_type]}"
        return f"No optimization suggestions for {action_type}"
    
    def reset_learning(self):
        """Reset all learned data"""
        self.action_history.clear()
        self.patterns.clear()
        self.learned_responses.clear()
        print("🧠 Precognitive AI learning reset")

# Global instance
precognitive_ai = PrecognitiveAI()
