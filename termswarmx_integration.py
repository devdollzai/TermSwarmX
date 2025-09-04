#!/usr/bin/env python3
"""
TermSwarmX Integration Module for DevDollz: Atelier Edition
Provides a clean interface to DevDollz functionality

Author: Alexis Andrews
Brand: DevDollz: Atelier Edition
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
from swarm_ide import Orchestrator, create_message, parse_message

class TermSwarmXIntegration:
    def __init__(self):
        self.orchestrator = Orchestrator()

    def integrate_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        agent_name = task.get('agent', '')
        cmd_type = task.get('type', 'custom')
        task_content = task.get('content', '')
        return self.orchestrator.route_task(agent_name, cmd_type, task_content)

    def load_plugin(self, file_path: str) -> Dict[str, Any]:
        file_path = os.path.normpath(file_path)
        return self.orchestrator.load_plugin(file_path)

if __name__ == "__main__":
    integration = TermSwarmXIntegration()
    task = {"agent": "code_gen", "type": "function", "content": "read_csv_to_dataframe"}
    result = integration.integrate_task(task)
    print(f"Integration result: {result}")
