def calculate_surgery(deviation_type, deviation_value, approach):
    plan = []

    def add_procedure(eye, muscle, action, amount):
        if amount > 0:
            plan.append(f"{eye} {muscle} {action} of {amount:.1f} mm")

    def split_bilateral(amount):
        half = round(amount / 2, 1)
        return half, half

    def handle_large_correction(primary_amount, muscle, action, opposite_muscle):
        if primary_amount <= 12:
            return [(muscle, action, primary_amount)], []
        else:
            # Split correction evenly between affected and other eye
            half = round(primary_amount / 2, 1)
            remainder = primary_amount - half
            # Both eyes get half (or near half), assign accordingly
            return [(muscle, action, half)], [(opposite_muscle, action, remainder)]

    if deviation_type == "Esotropia":
        mr_amount = round(deviation_value / 5.0, 1)
        lr_amount = round(deviation_value / 10.0, 1)
        
        if approach == "Unilateral":
            affected_corrections, other_corrections = handle_large_correction(mr_amount, "Medial Rectus", "recession", "Medial Rectus")
            for muscle, action, amt in affected_corrections:
                add_procedure("Affected Eye", muscle, action, amt)
            for muscle, action, amt in other_corrections:
                add_procedure("Other Eye", muscle, action, amt)
            add_procedure("Affected Eye", "Lateral Rectus", "resection", lr_amount)
        else:
            r_amt, l_amt = split_bilateral(mr_amount)
            add_procedure("Affected Eye", "Medial Rectus", "recession", r_amt)
            add_procedure("Other Eye", "Medial Rectus", "recession", l_amt)

    elif deviation_type == "Exotropia":
        lr_amount = round(deviation_value / 5.0, 1)
        mr_amount = round(deviation_value / 10.0, 1)

        if approach == "Unilateral":
            affected_corrections, other_corrections = handle_large_correction(lr_amount, "Lateral Rectus", "recession", "Lateral Rectus")
            for muscle, action, amt in affected_corrections:
                add_procedure("Affected Eye", muscle, action, amt)
            for muscle, action, amt in other_corrections:
                add_procedure("Other Eye", muscle, action, amt)
            add_procedure("Affected Eye", "Medial Rectus", "resection", mr_amount)
        else:
            r_amt, l_amt = split_bilateral(lr_amount)
            add_procedure("Affected Eye", "Lateral Rectus", "recession", r_amt)
            add_procedure("Other Eye", "Lateral Rectus", "recession", l_amt)

    elif deviation_type == "Hypertropia":
        amount = round(deviation_value / 5.0, 1)
        if approach == "Unilateral":
            add_procedure("Affected Eye", "Superior Rectus", "recession", amount)
            add_procedure("Affected Eye", "Inferior Rectus", "resection", amount)
        else:
            add_procedure("Affected Eye", "Superior Rectus", "recession", amount)
            add_procedure("Other Eye", "Inferior Rectus", "recession", amount)

    elif deviation_type == "Hypotropia":
        amount = round(deviation_value / 5.0, 1)
        if approach == "Unilateral":
            add_procedure("Affected Eye", "Inferior Rectus", "recession", amount)
            add_procedure("Affected Eye", "Superior Rectus", "resection", amount)
        else:
            add_procedure("Affected Eye", "Inferior Rectus", "recession", amount)
            add_procedure("Other Eye", "Superior Rectus", "recession", amount)

    return plan
