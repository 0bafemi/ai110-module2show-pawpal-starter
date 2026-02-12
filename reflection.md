# PawPal+ Project Reflection

## 1. System Design

A user can add and manage information about their pet
A user can add pet care tasks such as walks, feeding, or medication
A user can view a daily plan showing which tasks should be completed today and why

**a. Initial design**

- **Initial UML design**
    The UML models PawPal+ as a small, object-oriented system that separates data storage (Owner, Pet, Task), planning logic (Scheduler), and planning output (SchedulePlan). Owners contain pets, pets contain tasks, and the Scheduler uses this data to generate a daily plan based on task priority and available time.

- **Classes and responsibilities**
    Owner: Stores owner info and daily available time; manages pets and aggregates all tasks across pets.
    Pet: Stores pet details; manages that pet’s tasks and computes total task time.
    Task: Represents a single care task with duration, category, and priority; converts priority into a numeric value for scheduling.
    Scheduler: Contains the scheduling logic; sorts tasks by priority, fits them into available time, and generates a plan.
    SchedulePlan: Holds the result of scheduling, including scheduled tasks, skipped tasks, time usage, and a short explanation.

**b. Design changes**

- Yes

- Added Methods:
    Owner.get_pet_by_id(pet_id)
    Allows looking up a specific pet by ID instead of iterating through the list manually
    Needed for: UI display, remove operations, and Task→Pet navigation

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
