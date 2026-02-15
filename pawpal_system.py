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
        self.pets.append(pet)

    def remove_pet(self, pet_id: int) -> None:
        """Remove a pet by its ID."""
        self.pets = [pet for pet in self.pets if pet.id != pet_id]

    def get_pet_by_id(self, pet_id: int) -> 'Pet | None':
        """
        Find a pet by its ID.
        Returns None if no pet with that ID exists.
        """
        for pet in self.pets:
            if pet.id == pet_id:
                return pet
        return None

    def get_all_tasks(self) -> List['Task']:
        """Collect all tasks from all pets owned by this owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_total_task_time(self) -> int:
        """Calculate the total duration of all tasks across all pets."""
        return sum(task.duration_minutes for task in self.get_all_tasks())


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
        if task.pet_id != self.id:
            raise ValueError(
                f"Task pet_id ({task.pet_id}) doesn't match Pet id ({self.id})"
            )
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> None:
        """Remove a task by its ID."""
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def get_task_by_id(self, task_id: int) -> 'Task | None':
        """
        Find a task by its ID.
        Returns None if no task with that ID exists.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_tasks(self) -> List['Task']:
        """Return all tasks for this pet."""
        return self.tasks

    def get_total_task_time(self) -> int:
        """Calculate the total duration of all tasks for this pet."""
        return sum(task.duration_minutes for task in self.tasks)


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
        return PRIORITY_VALUES.get(self.priority.lower(), 1)


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
        summary_lines = [
            f"Daily Schedule Summary",
            f"Time Available: {self.time_available} minutes",
            f"Scheduled: {self.get_scheduled_count()} tasks ({self.time_used} min)",
            f"Skipped: {self.get_skipped_count()} tasks",
            f"",
            f"{self.explanation}"
        ]
        return "\n".join(summary_lines)

    def get_scheduled_count(self) -> int:
        """Return the number of scheduled tasks."""
        return len(self.scheduled_tasks)

    def get_skipped_count(self) -> int:
        """Return the number of skipped tasks."""
        return len(self.skipped_tasks)


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
        # Step 1: Collect all tasks from all pets
        all_tasks = owner.get_all_tasks()

        # Step 2: Sort tasks by priority (high to low)
        sorted_tasks = self._sort_tasks_by_priority(all_tasks)

        # Step 3: Fit tasks into available time
        scheduled, skipped = self._fit_tasks_to_time(
            sorted_tasks,
            owner.available_time_minutes
        )

        # Step 4: Calculate time used
        time_used = sum(task.duration_minutes for task in scheduled)

        # Step 5: Generate explanation
        explanation = self._generate_explanation(
            scheduled, skipped, time_used, owner.available_time_minutes
        )

        # Step 6: Return plan
        return SchedulePlan(
            scheduled_tasks=scheduled,
            skipped_tasks=skipped,
            explanation=explanation,
            time_used=time_used,
            time_available=owner.available_time_minutes
        )

    def _sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks by priority (high to low).
        Private helper method.

        Args:
            tasks: List of tasks to sort

        Returns:
            Sorted list of tasks (high priority first)
        """
        return sorted(tasks, key=lambda task: task.get_priority_value(), reverse=True)

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
        scheduled = []
        skipped = []
        time_remaining = available_time

        for task in tasks:
            if task.duration_minutes <= time_remaining:
                # Task fits! Schedule it
                scheduled.append(task)
                time_remaining -= task.duration_minutes
            else:
                # Task doesn't fit, skip it
                skipped.append(task)

        return scheduled, skipped

    def _generate_explanation(
        self,
        scheduled: List[Task],
        skipped: List[Task],
        time_used: int,
        time_available: int
    ) -> str:
        """
        Generate a human-readable explanation of the schedule.
        Private helper method.

        Args:
            scheduled: List of scheduled tasks
            skipped: List of skipped tasks
            time_used: Total minutes scheduled
            time_available: Owner's available time

        Returns:
            Explanation string
        """
        if not scheduled and not skipped:
            return "No tasks to schedule today. Enjoy your free time!"

        if not skipped:
            return (
                f"All {len(scheduled)} tasks fit! "
                f"Used {time_used}/{time_available} minutes. "
                f"Tasks were prioritized by importance (high > medium > low)."
            )

        return (
            f"Scheduled {len(scheduled)} high-priority tasks ({time_used} min). "
            f"Skipped {len(skipped)} lower-priority tasks due to time constraints. "
            f"Consider rescheduling skipped tasks for tomorrow or reducing task durations."
        )


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
