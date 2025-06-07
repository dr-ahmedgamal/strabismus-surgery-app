def calculate_surgery(deviation_type, deviation_value, approach):
    plan = []

    def add_procedure(eye, muscle, action, amount):
        if amount > 0:
            plan.append(f"{eye} {muscle} {action} of {amount:.1f} mm")

    def split_bilateral(amount):
        return round(amount / 2, 1), round(amount / 2, 1)

    def handle_large_correction(primary_amount, muscle, action, opposite_eye):
        if primary_amount <= 12:
            return [(muscle, action, primary_amount, "Right Eye")]
        else:
            return [
                (muscle, action, 12, "Right Eye"),
                (muscle, action, round(primary_amount - 12, 1), opposite_eye)
            ]

    if deviation_type == "Esotropia":
        mr_amount = round(deviation_value / 5.0, 1)
        lr_amount = round(deviation_value / 10.0, 1)

        if approach == "Unilateral":
            corrections = handle_large_correction(mr_amount, "Medial Rectus", "recession", "Left Eye")
            for muscle, action, amt, eye in corrections:
                add_procedure(eye, muscle, action, amt)
            add_procedure("Right Eye", "Lateral Rectus", "resection", lr_amount)
        else:
            r_amt, l_amt = split_bilateral(mr_amount)
            add_procedure("Right Eye", "Medial Rectus", "recession", r_amt)
            add_procedure("Left Eye", "Medial Rectus", "recession", l_amt)

    elif deviation_type == "Exotropia":
        lr_amount = round(deviation_value / 5.0, 1)
        mr_amount = round(deviation_value / 10.0, 1)

        if approach == "Unilateral":
            corrections = handle_large_correction(lr_amount, "Lateral Rectus", "recession", "Left Eye")
            for muscle, action, amt, eye in corrections:
                add_procedure(eye, muscle, action, amt)
            add_procedure("Right Eye", "Medial Rectus", "resection", mr_amount)
        else:
            r_amt, l_amt = split_bilateral(lr_amount)
            add_procedure("Right Eye", "Lateral Rectus", "recession", r_amt)
            add_procedure("Left Eye", "Lateral Rectus", "recession", l_amt)

    elif deviation_type == "Hypertropia":
        amount = round(deviation_value / 5.0, 1)
        if approach == "Unilateral":
            add_procedure("Right Eye", "Superior Rectus", "recession", amount)
            add_procedure("Right Eye", "Inferior Rectus", "resection", amount)
        else:
            add_procedure("Right Eye", "Superior Rectus", "recession", amount)
            add_procedure("Left Eye", "Inferior Rectus", "recession", amount)

    elif deviation_type == "Hypotropia":
        amount = round(deviation_value / 5.0, 1)
        if approach == "Unilateral":
            add_procedure("Right Eye", "Inferior Rectus", "recession", amount)
            add_procedure("Right Eye", "Superior Rectus", "resection", amount)
        else:
            add_procedure("Right Eye", "Inferior Rectus", "recession", amount)
            add_procedure("Left Eye", "Superior Rectus", "recession", amount)

    return plan
