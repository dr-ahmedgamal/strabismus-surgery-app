def calculate_correction_amounts(deviation_type, deviation_pd, approach):
    """
    Calculate muscle corrections based on deviation type, amount, and surgical approach.
    Formulas:

    Esotropia:
      - Medial rectus recession = 3 mm baseline + 1 mm per 5 PD step above 15 PD
      - Lateral rectus resection = 3 mm baseline + 1 mm per 5 PD step above 15 PD

    Exotropia:
      - Lateral rectus recession = 4 mm baseline + 1 mm per 5 PD step above 15 PD
      - Medial rectus resection = 3 mm baseline + 0.5 mm per 5 PD step above 15 PD

    Vertical deviations (Hypertropia/Hypotropia):
      - Use medial rectus nomogram (same as esotropia medial rectus)
    
    If total correction on any muscle > 12 mm, split equally bilaterally.

    Returns:
      dict with keys:
        'affected_eye': list of tuples (muscle, amount)
        'other_eye': list of tuples (muscle, amount)
    """
    # Helper function to calculate correction amount based on steps above 15 PD
    def steps_above_15(pd):
        if pd <= 15:
            return 0
        return (pd - 15) / 5  # steps in units of 5 PD

    steps = steps_above_15(deviation_pd)
    
    # Initialize muscle amounts
    affected = []
    other = []

    # Define baseline and increments for each muscle depending on deviation type
    if deviation_type.lower() == "esotropia":
        # Medial rectus recession (affected eye)
        mr_base = 3
        mr_inc = 1
        # Lateral rectus resection (affected eye)
        lr_base = 3
        lr_inc = 1

        mr_amount = mr_base + mr_inc * steps
        lr_amount = lr_base + lr_inc * steps

        # Check for max 12 mm limit and split if exceeded
        # Medial rectus recession
        if mr_amount > 12:
            mr_affected = 12
            mr_other = mr_amount - 12
            mr_affected, mr_other = mr_amount / 2, mr_amount / 2  # equal split
        else:
            mr_affected = mr_amount
            mr_other = 0

        # Lateral rectus resection
        if lr_amount > 12:
            lr_affected = 12
            lr_other = lr_amount - 12
            lr_affected, lr_other = lr_amount / 2, lr_amount / 2  # equal split
        else:
            lr_affected = lr_amount
            lr_other = 0

        if approach.lower() == "unilateral":
            affected = [("Medial Rectus recession", round(mr_affected, 1)),
                        ("Lateral Rectus resection", round(lr_affected, 1))]
            other = []
            if mr_other > 0 or lr_other > 0:
                # Add other eye corrections if split
                if mr_other > 0:
                    other.append(("Medial Rectus recession", round(mr_other,1)))
                if lr_other > 0:
                    other.append(("Lateral Rectus resection", round(lr_other,1)))
        else:  # bilateral approach
            # Bilateral medial rectus recessions split equally
            mr_total = mr_amount
            mr_each = round(mr_total / 2, 1)
            affected = [("Medial Rectus recession", mr_each)]
            other = [("Medial Rectus recession", mr_each)]

    elif deviation_type.lower() == "exotropia":
        # Lateral rectus recession (affected eye)
        lr_base = 4
        lr_inc = 1
        # Medial rectus resection (affected eye)
        mr_base = 3
        mr_inc = 0.5

        lr_amount = lr_base + lr_inc * steps
        mr_amount = mr_base + mr_inc * steps

        # Check max 12 mm limits and split if exceeded
        if lr_amount > 12:
            lr_affected, lr_other = lr_amount / 2, lr_amount / 2
        else:
            lr_affected, lr_other = lr_amount, 0

        if mr_amount > 12:
            mr_affected, mr_other = mr_amount / 2, mr_amount / 2
        else:
            mr_affected, mr_other = mr_amount, 0

        if approach.lower() == "unilateral":
            affected = [("Lateral Rectus recession", round(lr_affected,1)),
                        ("Medial Rectus resection", round(mr_affected,1))]
            other = []
            if lr_other > 0:
                other.append(("Lateral Rectus recession", round(lr_other,1)))
            if mr_other > 0:
                other.append(("Medial Rectus resection", round(mr_other,1)))
        else:  # bilateral approach
            # Bilateral lateral rectus recessions split equally
            lr_total = lr_amount
            lr_each = round(lr_total / 2, 1)
            affected = [("Lateral Rectus recession", lr_each)]
            other = [("Lateral Rectus recession", lr_each)]

    elif deviation_type.lower() in ["hypertropia", "hypotropia"]:
        # Use same nomogram as medial rectus for vertical deviations
        mr_base = 3
        mr_inc = 1
        mr_amount = mr_base + mr_inc * steps

        if mr_amount > 12:
            mr_affected, mr_other = mr_amount / 2, mr_amount / 2
        else:
            mr_affected, mr_other = mr_amount, 0

        if approach.lower() == "unilateral":
            affected = [("Medial Rectus recession", round(mr_affected,1))]
            other = []
            if mr_other > 0:
                other = [("Medial Rectus recession", round(mr_other,1))]
        else:  # bilateral approach
            mr_each = round(mr_amount / 2, 1)
            affected = [("Medial Rectus recession", mr_each)]
            other = [("Medial Rectus recession", mr_each)]

    else:
        raise ValueError("Unknown deviation type. Allowed: Esotropia, Exotropia, Hypertropia, Hypotropia.")

    return {
        "affected_eye": affected,
        "other_eye": other
    }
