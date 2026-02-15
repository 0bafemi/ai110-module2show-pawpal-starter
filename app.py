import streamlit as st
# Step 1: Import our backend classes
from pawpal_system import Owner, Pet, Task, Scheduler, IDGenerator

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Step 2: Initialize session state "memory vault"
# This runs ONCE per session, not on every button click
if "owner" not in st.session_state:
    # Create a new Owner with default values
    st.session_state.owner = Owner(
        id=IDGenerator.next_id("owner"),
        name="Jordan",  # Default name
        available_time_minutes=120  # Default: 2 hours
    )

if "scheduler" not in st.session_state:
    # Create the scheduler (stateless, but we store it for convenience)
    st.session_state.scheduler = Scheduler()

if "current_plan" not in st.session_state:
    # Placeholder for the most recent schedule
    st.session_state.current_plan = None

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Step 3: Wire UI to Backend Logic

st.subheader("Owner & Time Budget")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value=st.session_state.owner.name, key="owner_name_input")
    st.session_state.owner.name = owner_name
with col2:
    # Use text_input for clean input without spinner buttons
    available_time = st.text_input(
        "Available time (minutes)",
        value=str(st.session_state.owner.available_time_minutes),
        key="time_input"
    )
    # Convert to integer and update session state
    try:
        time_value = int(available_time)
        if 10 <= time_value <= 480:
            st.session_state.owner.available_time_minutes = time_value
        else:
            st.warning("Please enter a time between 10 and 480 minutes")
    except ValueError:
        st.warning("Please enter a valid number")

st.divider()

# Add Pet Section
st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
    age = st.number_input("Age", min_value=0, max_value=30, value=3)
    submitted = st.form_submit_button("Add Pet")

    if submitted and pet_name:
        # Create a new Pet object
        new_pet = Pet(
            id=IDGenerator.next_id("pet"),
            name=pet_name,
            species=species,
            age=age
        )
        # Add it to the owner's collection
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added {pet_name} the {species}!")
        st.rerun()

# Display current pets with delete buttons
if st.session_state.owner.pets:
    st.write(f"**Current Pets ({len(st.session_state.owner.pets)}):**")
    for pet in st.session_state.owner.pets:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"- {pet.name} ({pet.species}, {pet.age} years old) - {len(pet.tasks)} tasks")
        with col2:
            if st.button("Delete", key=f"delete_pet_{pet.id}"):
                st.session_state.owner.remove_pet(pet.id)
                st.success(f"Deleted {pet.name}")
                st.rerun()
else:
    st.info("No pets yet. Add one above.")

st.divider()

# Add Task Section
st.subheader("Add a Task")
if not st.session_state.owner.pets:
    st.warning("Please add a pet first before adding tasks.")
else:
    with st.form("add_task_form"):
        pet_names = [pet.name for pet in st.session_state.owner.pets]
        selected_pet_name = st.selectbox("For which pet?", pet_names)

        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task name", value="Morning walk")
        with col2:
            category = st.selectbox("Category", ["Walk", "Feeding", "Medication", "Grooming", "Enrichment", "Training"])
        with col3:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)

        priority = st.selectbox("Priority", ["high", "medium", "low"])
        task_submitted = st.form_submit_button("Add Task")

        if task_submitted and task_title:
            # Find the selected pet
            selected_pet = None
            for pet in st.session_state.owner.pets:
                if pet.name == selected_pet_name:
                    selected_pet = pet
                    break

            if selected_pet:
                # Create new Task
                new_task = Task(
                    id=IDGenerator.next_id("task"),
                    name=task_title,
                    category=category,
                    duration_minutes=int(duration),
                    priority=priority,
                    pet_id=selected_pet.id
                )
                # Add task to pet
                selected_pet.add_task(new_task)
                st.success(f"Added '{task_title}' for {selected_pet.name}!")
                st.rerun()

# Display all tasks with delete buttons
all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.write(f"**All Tasks ({len(all_tasks)} total, {st.session_state.owner.get_total_task_time()} min):**")
    for task in all_tasks:
        pet = st.session_state.owner.get_pet_by_id(task.pet_id)
        pet_name = pet.name if pet else "Unknown"

        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"- [{task.priority.upper()}] {task.name} ({pet_name}) - {task.duration_minutes} min")
        with col2:
            if st.button("Delete", key=f"delete_task_{task.id}"):
                if pet:
                    pet.remove_task(task.id)
                    st.success(f"Deleted '{task.name}'")
                    st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Generate Schedule")
st.caption("Click below to generate today's optimized schedule based on priority and time constraints.")

if st.button("Generate Schedule", type="primary"):
    if not st.session_state.owner.pets:
        st.error("Please add at least one pet first.")
    elif not all_tasks:
        st.error("Please add at least one task first.")
    else:
        # Call the scheduler!
        plan = st.session_state.scheduler.generate_plan(st.session_state.owner)
        st.session_state.current_plan = plan
        st.success("Schedule generated!")
        st.rerun()

# Display the schedule if it exists
if st.session_state.current_plan:
    plan = st.session_state.current_plan

    st.divider()
    st.subheader("Today's Schedule")

    # Show summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Time Available", f"{plan.time_available} min")
    with col2:
        st.metric("Time Used", f"{plan.time_used} min")
    with col3:
        st.metric("Tasks Scheduled", plan.get_scheduled_count())

    # Show explanation
    st.info(plan.explanation)

    # Show scheduled tasks
    if plan.scheduled_tasks:
        st.markdown("### ✅ Scheduled Tasks")
        for i, task in enumerate(plan.scheduled_tasks, 1):
            pet = st.session_state.owner.get_pet_by_id(task.pet_id)
            pet_name = pet.name if pet else "Unknown"

            with st.container():
                col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
                with col1:
                    st.write(f"**{i}.**")
                with col2:
                    st.write(f"**{task.name}** ({pet_name})")
                with col3:
                    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                    st.write(f"{priority_emoji.get(task.priority, '')} {task.priority.capitalize()}")
                with col4:
                    st.write(f"{task.duration_minutes} min")

    # Show skipped tasks
    if plan.skipped_tasks:
        st.markdown("### ⏭️ Skipped Tasks (not enough time)")
        for task in plan.skipped_tasks:
            pet = st.session_state.owner.get_pet_by_id(task.pet_id)
            pet_name = pet.name if pet else "Unknown"
            st.write(f"- {task.name} ({pet_name}) - {task.duration_minutes} min [{task.priority}]")
