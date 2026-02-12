"""
PawPal+ System - Pet Care Planning Logic
This module contains the core classes for managing pets, tasks, and scheduling.
"""

from dataclasses import dataclass, field
from typing import List, Tuple


# =============================================================================
# DATA CLASSES (Data-holding objects)
# =============================================================================

@dataclass
class Owner:
    """
    Represents a pet owner.
    Manages pets and tracks daily available time for pet care.
    """
    id: int
    name: str
    available_time_minutes: int
    pets: List['Pet'] = field(default_factory=list)

    def add_pet(self, pet: 'Pet') -> None:
        """Add a pet to the owner's collection."""
        pass

    def remove_pet(self, pet_id: int) -> None:
        """Remove a pet by its ID."""
        pass

    def get_pet_by_id(self, pet_id: int) -> 'Pet | None':
        """
        Find a pet by its ID.
        Returns None if no pet with that ID exists.
        """
        pass

    def get_all_tasks(self) -> List['Task']:
        """Collect all tasks from all pets owned by this owner."""
        pass

    def get_total_task_time(self) -> int:
        """Calculate the total duration of all tasks across all pets."""
        pass


@dataclass
class Pet:
    """
    Represents a pet.
    Holds pet profile information and manages associated care tasks.
    """
    id: int
    name: str
    species: str
    age: int
    tasks: List['Task'] = field(default_factory=list)

    def add_task(self, task: 'Task') -> None:
        """
        Add a care task for this pet.
        Validates that task.pet_id matches this pet's ID.
        """
        # TODO: Validate task.pet_id == self.id before adding
        pass

    def remove_task(self, task_id: int) -> None:
        """Remove a task by its ID."""
        pass

    def get_task_by_id(self, task_id: int) -> 'Task | None':
        """
        Find a task by its ID.
        Returns None if no task with that ID exists.
        """
        pass

    def get_tasks(self) -> List['Task']:
        """Return all tasks for this pet."""
        pass

    def get_total_task_time(self) -> int:
        """Calculate the total duration of all tasks for this pet."""
        pass


@dataclass
class Task:
    """
    Represents a single pet care activity.
    Contains task details including duration and priority.
    """
    id: int
    name: str
    category: str
    duration_minutes: int
    priority: str  # "high", "medium", or "low"
    pet_id: int

    def get_priority_value(self) -> int:
        """
        Convert priority string to numeric value for sorting.
        Returns: 3 for high, 2 for medium, 1 for low
        Defaults to 1 (low) if priority is invalid.
        """
        # TODO: Use PRIORITY_VALUES.get(self.priority.lower(), 1)
        pass


@dataclass
class SchedulePlan:
    """
    Represents the result of scheduling.
    Contains scheduled tasks, skipped tasks, and explanation.
    """
    scheduled_tasks: List[Task] = field(default_factory=list)
    skipped_tasks: List[Task] = field(default_factory=list)
    explanation: str = ""
    time_used: int = 0
    time_available: int = 0

    def get_summary(self) -> str:
        """Return a formatted summary of the schedule."""
        pass

    def get_scheduled_count(self) -> int:
        """Return the number of scheduled tasks."""
        pass

    def get_skipped_count(self) -> int:
        """Return the number of skipped tasks."""
        pass


# =============================================================================
# LOGIC CLASS (Scheduling engine)
# =============================================================================

class Scheduler:
    """
    Scheduling engine for pet care tasks.
    Creates daily plans based on available time and task priorities.
    This class is stateless - it doesn't store data between calls.
    """

    def generate_plan(self, owner: Owner) -> SchedulePlan:
        """
        Generate a daily care plan for the owner's pets.

        Args:
            owner: The pet owner with pets and available time

        Returns:
            SchedulePlan object containing scheduled/skipped tasks and explanation
        """
        pass

    def _sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks by priority (high to low).
        Private helper method.

        Args:
            tasks: List of tasks to sort

        Returns:
            Sorted list of tasks (high priority first)
        """
        pass

    def _fit_tasks_to_time(
        self,
        tasks: List[Task],
        available_time: int
    ) -> Tuple[List[Task], List[Task]]:
        """
        Fit tasks into available time budget using greedy algorithm.
        Private helper method.

        Args:
            tasks: List of sorted tasks
            available_time: Available time in minutes

        Returns:
            Tuple of (scheduled_tasks, skipped_tasks)
        """
        pass


# =============================================================================
# HELPER CONSTANTS
# =============================================================================

# Task priority mapping
PRIORITY_VALUES = {
    "high": 3,
    "medium": 2,
    "low": 1
}

# Valid task categories
TASK_CATEGORIES = [
    "Walk",
    "Feeding",
    "Medication",
    "Grooming",
    "Enrichment",
    "Training"
]


# =============================================================================
# OPTIONAL: ID GENERATOR UTILITY
# =============================================================================

class IDGenerator:
    """
    Simple ID generator for Owner, Pet, and Task objects.
    Optional helper to avoid manual ID management.
    """
    _counters = {"owner": 0, "pet": 0, "task": 0}

    @classmethod
    def next_id(cls, entity_type: str) -> int:
        """
        Generate next unique ID for the given entity type.

        Args:
            entity_type: One of "owner", "pet", or "task"

        Returns:
            Next available ID number
        """
        cls._counters[entity_type] += 1
        return cls._counters[entity_type]

    @classmethod
    def reset(cls) -> None:
        """Reset all counters (useful for testing)."""
        cls._counters = {"owner": 0, "pet": 0, "task": 0}
