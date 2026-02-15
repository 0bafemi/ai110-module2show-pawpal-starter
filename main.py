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

    # Create tasks for Mochi (Dog) - times scrambled!
    task1 = Task(
        id=IDGenerator.next_id("task"),
        name="Morning walk",
        category="Walk",
        duration_minutes=30,
        priority="high",
        pet_id=pet1.id,
        time="08:00"
    )

    task2 = Task(
        id=IDGenerator.next_id("task"),
        name="Feed breakfast",
        category="Feeding",
        duration_minutes=10,
        priority="high",
        pet_id=pet1.id,
        time="07:30"  # Earlier than task1!
    )

    task3 = Task(
        id=IDGenerator.next_id("task"),
        name="Evening walk",
        category="Walk",
        duration_minutes=30,
        priority="medium",
        pet_id=pet1.id,
        time="17:00"  # Much later
    )

    # Create tasks for Luna (Cat) - also scrambled
    task4 = Task(
        id=IDGenerator.next_id("task"),
        name="Feed dinner",
        category="Feeding",
        duration_minutes=10,
        priority="high",
        pet_id=pet2.id,
        time="18:00"
    )

    task5 = Task(
        id=IDGenerator.next_id("task"),
        name="Playtime with toys",
        category="Enrichment",
        duration_minutes=20,
        priority="medium",
        pet_id=pet2.id,
        time="14:00"  # Earlier in day
    )

    task6 = Task(
        id=IDGenerator.next_id("task"),
        name="Brush fur",
        category="Grooming",
        duration_minutes=15,
        priority="low",
        pet_id=pet2.id,
        time="20:00"  # Last task of day
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

    # ========== DEMONSTRATE SORTING BY TIME ==========
    print("=" * 60)
    print("DEMONSTRATION: Sort Tasks by Time")
    print("=" * 60)

    scheduler = Scheduler()
    all_tasks = owner.get_all_tasks()

    print(f"\nOriginal order ({len(all_tasks)} tasks):")
    for task in all_tasks:
        pet = owner.get_pet_by_id(task.pet_id)
        print(f"  {task.time} - {task.name} ({pet.name if pet else 'Unknown'})")

    sorted_tasks = scheduler.sort_by_time(all_tasks)
    print(f"\nSorted by time:")
    for task in sorted_tasks:
        pet = owner.get_pet_by_id(task.pet_id)
        print(f"  {task.time} - {task.name} ({pet.name if pet else 'Unknown'})")
    print()

    # ========== DEMONSTRATE FILTERING ==========
    print("=" * 60)
    print("DEMONSTRATION: Filter Tasks")
    print("=" * 60)

    # Filter by status (all should be incomplete initially)
    pending = scheduler.filter_by_status(all_tasks, is_completed=False)
    print(f"\nPending tasks: {len(pending)}")

    # Mark one task complete
    task2.mark_complete()
    completed = scheduler.filter_by_status(all_tasks, is_completed=True)
    print(f"Completed tasks after marking task2: {len(completed)}")
    for task in completed:
        print(f"  [DONE] {task.name}")

    # Filter by pet
    mochi_tasks = scheduler.filter_by_pet_name(all_tasks, "Mochi", owner)
    luna_tasks = scheduler.filter_by_pet_name(all_tasks, "Luna", owner)
    print(f"\nMochi's tasks: {len(mochi_tasks)}")
    for task in mochi_tasks:
        print(f"  [{pet1.name}] {task.time} - {task.name}")
    print(f"\nLuna's tasks: {len(luna_tasks)}")
    for task in luna_tasks:
        print(f"  [{pet2.name}] {task.time} - {task.name}")
    print()

    # Generate schedule
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
