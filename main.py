"""
PawPal+ Testing Ground
Run this file to test the scheduling system in the terminal.
"""

from pawpal_system import Owner, Pet, Task, Scheduler, IDGenerator


def main():
    print("=" * 60)
    print("PawPal+ Schedule Generator")
    print("=" * 60)
    print()

    # Create an owner
    owner = Owner(
        id=IDGenerator.next_id("owner"),
        name="Jordan",
        available_time_minutes=120  # 2 hours available today
    )
    print(f"Owner: {owner.name}")
    print(f"Available time: {owner.available_time_minutes} minutes")
    print()

    # Create pets
    pet1 = Pet(
        id=IDGenerator.next_id("pet"),
        name="Mochi",
        species="Dog",
        age=3
    )

    pet2 = Pet(
        id=IDGenerator.next_id("pet"),
        name="Luna",
        species="Cat",
        age=5
    )

    # Add pets to owner
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    print(f"Pet 1: {pet1.name} ({pet1.species}, {pet1.age} years old)")
    print(f"Pet 2: {pet2.name} ({pet2.species}, {pet2.age} years old)")
    print()

    # Create tasks for Mochi (Dog)
    task1 = Task(
        id=IDGenerator.next_id("task"),
        name="Morning walk",
        category="Walk",
        duration_minutes=30,
        priority="high",
        pet_id=pet1.id
    )

    task2 = Task(
        id=IDGenerator.next_id("task"),
        name="Feed breakfast",
        category="Feeding",
        duration_minutes=10,
        priority="high",
        pet_id=pet1.id
    )

    task3 = Task(
        id=IDGenerator.next_id("task"),
        name="Evening walk",
        category="Walk",
        duration_minutes=30,
        priority="medium",
        pet_id=pet1.id
    )

    # Create tasks for Luna (Cat)
    task4 = Task(
        id=IDGenerator.next_id("task"),
        name="Feed dinner",
        category="Feeding",
        duration_minutes=10,
        priority="high",
        pet_id=pet2.id
    )

    task5 = Task(
        id=IDGenerator.next_id("task"),
        name="Playtime with toys",
        category="Enrichment",
        duration_minutes=20,
        priority="medium",
        pet_id=pet2.id
    )

    task6 = Task(
        id=IDGenerator.next_id("task"),
        name="Brush fur",
        category="Grooming",
        duration_minutes=15,
        priority="low",
        pet_id=pet2.id
    )

    # Add tasks to pets
    pet1.add_task(task1)
    pet1.add_task(task2)
    pet1.add_task(task3)

    pet2.add_task(task4)
    pet2.add_task(task5)
    pet2.add_task(task6)

    print("Tasks Created:")
    print(f"  {pet1.name}: {len(pet1.tasks)} tasks ({pet1.get_total_task_time()} min total)")
    print(f"  {pet2.name}: {len(pet2.tasks)} tasks ({pet2.get_total_task_time()} min total)")
    print(f"  Total time needed: {owner.get_total_task_time()} minutes")
    print()

    # Generate schedule
    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner)

    # Display results
    print("=" * 60)
    print("TODAY'S SCHEDULE")
    print("=" * 60)
    print()

    print(f"SCHEDULED TASKS ({plan.get_scheduled_count()} tasks, {plan.time_used} min):")
    print("-" * 60)
    for i, task in enumerate(plan.scheduled_tasks, 1):
        # Get pet name for this task
        pet = owner.get_pet_by_id(task.pet_id)
        pet_name = pet.name if pet else "Unknown"

        print(f"{i}. [{task.priority.upper():6}] {task.name:20} | {pet_name:8} | {task.duration_minutes:2} min")
    print()

    if plan.skipped_tasks:
        print(f"SKIPPED TASKS ({plan.get_skipped_count()} tasks):")
        print("-" * 60)
        for i, task in enumerate(plan.skipped_tasks, 1):
            pet = owner.get_pet_by_id(task.pet_id)
            pet_name = pet.name if pet else "Unknown"

            print(f"{i}. [{task.priority.upper():6}] {task.name:20} | {pet_name:8} | {task.duration_minutes:2} min")
        print()

    print("=" * 60)
    print("EXPLANATION")
    print("=" * 60)
    print(plan.explanation)
    print()

    print("=" * 60)
    print(plan.get_summary())
    print("=" * 60)


if __name__ == "__main__":
    main()
