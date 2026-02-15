"""
Tests for PawPal+ System
Run with: python -m pytest
"""

from pawpal_system import Pet, Task


def test_task_completion():
    """Verify that calling mark_complete() actually changes the task's status."""
    # Arrange
    task = Task(
        id=1,
        name="Morning walk",
        category="Walk",
        duration_minutes=30,
        priority="high",
        pet_id=1
    )

    # Act
    initial_status = task.is_completed
    task.mark_complete()
    final_status = task.is_completed

    # Assert
    assert initial_status is False, "Task should start as not completed"
    assert final_status is True, "Task should be completed after mark_complete()"


def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    # Arrange
    pet = Pet(id=1, name="Mochi", species="Dog", age=3)
    task = Task(
        id=101,
        name="Feed breakfast",
        category="Feeding",
        duration_minutes=10,
        priority="high",
        pet_id=pet.id
    )

    # Act
    initial_count = len(pet.tasks)
    pet.add_task(task)
    final_count = len(pet.tasks)

    # Assert
    assert initial_count == 0, "Pet should start with 0 tasks"
    assert final_count == 1, "Pet should have 1 task after adding"
