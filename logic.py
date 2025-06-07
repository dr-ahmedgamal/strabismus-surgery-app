def calculate_surgery(deviation_type, deviation_value, approach):
    plan = []

    def add_procedure(eye, muscle, action, amount):
        if amount > 0:
            plan.append(f"{eye} {muscle} {action} of {amount:.1f} mm")

    def split_bilateral(amount):
        half = round(amount / 2, 1)
        return half, half

    def handle_large_correction_even_split(amount, muscle, action):
        if amount <= 12:
            return [(muscle, action, amount, "Affected Eye")]
        else:
            half1, half2 = split_bilateral(amount)
            return [
                (muscle, action, half1, "Affected Eye"),
                (muscle, action, half2, "Contralateral Eye")
            ]

    if deviation_type == "Esotropia":
        mr_amount = round(deviation_value / 5.0, 1)
        lr_amount = round(deviation_value / 10.0, 1)

        if approach == "Unilateral":
            corrections = handle_large_correction_even_split(mr_amount, "Medial Rectus", "recession")
            for muscle, action, amt, eye in corrections:
                add_procedure(eye, muscle, action, amt)
            add_procedure("Affected Eye", "Lateral Rectus", "resection", lr_amount)
        else:
            half1, half2 = split_bilateral(mr_amount)
            add_procedure("Affected Eye", "Medial Rectus", "recession", half1)
            add_procedure("Contralateral Eye", "Medial Rectus", "recession", half2)

    elif deviation_type == "Exotropia":
        lr_amount = round(deviation_value / 5.0, 1)
        mr_amount = round(deviation_value / 10.0, 1)

        if approach == "Unilateral":
            corrections = handle_large_correction_even_split(lr_amount, "Lateral Rectus", "recession")
            for muscle, action, amt, eye in corrections:
                add_procedure(eye, muscle, action, amt)
            add_procedure("Affected Eye", "Medial Rectus", "resection", mr_amount)
        else:
            half1, half2 = split_bilateral(lr_amount)
            add_procedure("Affected Eye", "Lateral Rectus", "recession", half1)
            add_procedure("Contralateral Eye", "Lateral Rectus", "recession", half2)

    elif deviation_type == "Hypertropia":
        amount = round(deviation_value / 5.0, 1)
        if approach == "Unilateral":
            add_procedure("Affected Eye", "Superior Rectus", "recession", amount)
            add_procedure("Affected Eye", "Inferior Rectus", "resection", amount)
        else:
            add_procedure("Affected Eye", "Superior Rectus", "recession", amount)
            add_procedure("Contralateral Eye", "Inferior Rectus", "recession", amount)

    elif deviation_type == "Hypotropia":
        amount = round(deviation_value / 5.0, 1)
        if approach == "Unilateral":
            add_procedure("Affected Eye", "Inferior Rectus", "recession", amount)
            add_procedure("Affected Eye", "Superior Rectus", "resection", amount)
        else:
            add_procedure("Affected Eye", "Inferior Rectus", "recession", amount)
            add_procedure("Contralateral Eye", "Superior Rectus", "recession", amount)

    return plan
