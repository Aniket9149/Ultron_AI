"""
01_Memory/pending_actions.py
Robust Persistent Task & Milestone Memory Engine for Ultron.
Tracks in-flight actions, interrupted goals, and game studio milestones.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

MEMORY_DIR = Path(__file__).resolve().parent
STORAGE_FILE = MEMORY_DIR / "pending_tasks.json"

class PendingActionManager:
    def __init__(self, storage_path: Path = STORAGE_FILE):
        self.storage_path = storage_path
        self._ensure_storage()

    def _ensure_storage(self):
        if not self.storage_path.exists():
            initial_data = {
                "version": "1.0.0",
                "last_updated": time.time(),
                "active_project": None,
                "pending_tasks": [],
                "completed_history": []
            }
            self._write(initial_data)

    def _read(self) -> Dict[str, Any]:
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"active_project": None, "pending_tasks": [], "completed_history": []}

    def _write(self, data: Dict[str, Any]):
        data["last_updated"] = time.time()
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def set_active_project(self, project_name: str, project_meta: Optional[Dict[str, Any]] = None):
        data = self._read()
        data["active_project"] = {
            "name": project_name,
            "created_at": time.time(),
            "meta": project_meta or {}
        }
        self._write(data)

    def get_active_project(self) -> Optional[Dict[str, Any]]:
        return self._read().get("active_project")

    def register_task(self, task_id: str, agent: str, description: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        data = self._read()
        # Prevent duplicate pending tasks
        for task in data["pending_tasks"]:
            if task["id"] == task_id:
                task["updated_at"] = time.time()
                task["payload"] = payload or task.get("payload", {})
                self._write(data)
                return task

        task = {
            "id": task_id,
            "agent": agent,
            "description": description,
            "status": "pending",
            "created_at": time.time(),
            "updated_at": time.time(),
            "payload": payload or {}
        }
        data["pending_tasks"].append(task)
        self._write(data)
        return task

    def update_task_status(self, task_id: str, status: str, result: Optional[Any] = None):
        data = self._read()
        task_to_move = None

        for task in data["pending_tasks"]:
            if task["id"] == task_id:
                task["status"] = status
                task["updated_at"] = time.time()
                if result is not None:
                    task["result"] = result
                if status.lower() in ("completed", "resolved"):
                    task_to_move = task
                break

        if task_to_move:
            data["pending_tasks"].remove(task_to_move)
            data["completed_history"].append(task_to_move)
            # Keep completed history bounded to last 50 items
            if len(data["completed_history"]) > 50:
                data["completed_history"] = data["completed_history"][-50:]

        self._write(data)

    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        return self._read().get("pending_tasks", [])

    def get_next_task(self) -> Optional[Dict[str, Any]]:
        tasks = self.get_pending_tasks()
        return tasks[0] if tasks else None

    def clear_all(self):
        self._write({
            "version": "1.0.0",
            "last_updated": time.time(),
            "active_project": None,
            "pending_tasks": [],
            "completed_history": []
        })

pending_actions = PendingActionManager()
