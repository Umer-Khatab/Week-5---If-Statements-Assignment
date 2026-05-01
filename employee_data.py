"""
Week 5 - If Statements Assignment
Author: Umer Khatab

Processes a messy list of employee data exported from a spreadsheet,
deduplicates it, sorts it into dictionary records, and computes:
  - total hourly rate (wage + 30% benefits)
  - a list of underpaid employees (total rate between 28.15 and 30.65)
  - a list of raises by employee, based on tiered hourly-rate rules
"""

# ---------------------------------------------------------------------------
# Requirement 1: Create the single list with the messy raw data, in order.
# ---------------------------------------------------------------------------
raw_data = [
    1121, "Jackie Grainger", 22.22,
    1122, "Jignesh Thrakkar", 25.25,
    1127, "Dion Green", 28.75, False,
    24.32, 1132, "Jacob Gerber",
    "Sarah Sanderson", 23.45, 1137, True,
    "Brandon Heck", 1138, 25.84, True,
    1152, "David Toma", 22.65,
    23.75, 1157, "Charles King", False,
    "Jackie Grainger", 1121, 22.22, False,
    22.65, 1152, "David Toma",
]

# ---------------------------------------------------------------------------
# Requirement 2: Programmatically sort the messy list into a list of dicts.
#
# Strategy: walk through the raw list and, for every int we find, look at the
# small group of items around it to pull out the matching string (name) and
# float (hourly wage). The bool values are the "extra column" that should be
# ignored. This works regardless of the order the three useful values appear
# in within a record.
# ---------------------------------------------------------------------------
employees = []

# Track which indices we've already consumed so we don't reuse a value.
used = set()

for i, value in enumerate(raw_data):
    # Anchor on the employee ID (an int, but NOT a bool — bool is a subclass
    # of int in Python, so we must rule it out explicitly).
    if isinstance(value, bool):
        continue
    if not isinstance(value, int):
        continue
    if i in used:
        continue

    emp_id = value
    name = None
    wage = None
    name_idx = None
    wage_idx = None

    # Look in a small window around the ID for the matching name and wage.
    # Window of +/- 3 is enough given the data layout.
    for j in range(max(0, i - 3), min(len(raw_data), i + 4)):
        if j == i or j in used:
            continue
        item = raw_data[j]
        if name is None and isinstance(item, str):
            name = item
            name_idx = j
        elif wage is None and isinstance(item, float):
            wage = item
            wage_idx = j
        if name is not None and wage is not None:
            break

    # Only build a record if we found all three pieces.
    if name is not None and wage is not None:
        employees.append({
            "employee_id": emp_id,
            "name": name,
            "hourly_wage": wage,
        })
        used.add(i)
        used.add(name_idx)
        used.add(wage_idx)

# ---------------------------------------------------------------------------
# Requirement 3: No duplicate data should make it into the list of dicts.
# A duplicate is a record with the same employee_id, name, and hourly_wage.
# ---------------------------------------------------------------------------
unique_employees = []
seen = set()
for emp in employees:
    signature = (emp["employee_id"], emp["name"], emp["hourly_wage"])
    if signature not in seen:
        seen.add(signature)
        unique_employees.append(emp)

employees = unique_employees

# ---------------------------------------------------------------------------
# Requirement 4: Multiply each hourly_wage by 1.3 and store as total_hourly_rate.
# ---------------------------------------------------------------------------
for emp in employees:
    emp["total_hourly_rate"] = round(emp["hourly_wage"] * 1.3, 4)

# ---------------------------------------------------------------------------
# Requirement 5: Build underpaid_salaries — anyone whose total_hourly_rate
# is between 28.15 and 30.65 (inclusive on both ends).
# ---------------------------------------------------------------------------
underpaid_salaries = []
for emp in employees:
    if 28.15 <= emp["total_hourly_rate"] <= 30.65:
        underpaid_salaries.append(emp)

# ---------------------------------------------------------------------------
# Requirement 6: Calculate a raise per employee based on hourly_wage tiers.
#   $22 - $24/hr -> 5% raise
#   $24 - $26/hr -> 4% raise
#   $26 - $28/hr -> 3% raise
#   anything else -> 2% raise
# Store {name, raise} dicts in company_raises.
#
# Style note: the assignment asks us to apply the if-statement styling
# guidelines, so we use a clean if/elif/else chain (no nested ifs, no
# redundant comparisons) and operate on the *current hourly rate*, not the
# total_hourly_rate.
# ---------------------------------------------------------------------------
company_raises = []
for emp in employees:
    wage = emp["hourly_wage"]

    if 22 <= wage < 24:
        raise_pct = 0.05
    elif 24 <= wage < 26:
        raise_pct = 0.04
    elif 26 <= wage < 28:
        raise_pct = 0.03
    else:
        raise_pct = 0.02

    raise_amount = round(wage * raise_pct, 2)
    company_raises.append({
        "name": emp["name"],
        "raise": raise_amount,
    })

# ---------------------------------------------------------------------------
# Requirement 7: Print out all three lists.
# ---------------------------------------------------------------------------
print("=" * 60)
print("EMPLOYEES (cleaned, deduplicated, with total_hourly_rate)")
print("=" * 60)
for emp in employees:
    print(emp)

print()
print("=" * 60)
print("UNDERPAID SALARIES (total_hourly_rate between $28.15 and $30.65)")
print("=" * 60)
for emp in underpaid_salaries:
    print(emp)

print()
print("=" * 60)
print("COMPANY RAISES")
print("=" * 60)
for entry in company_raises:
    print(entry)
