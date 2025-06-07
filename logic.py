def calculate_surgery(deviation_type, deviation_value, approach):
    plan = {"Affected Eye": [], "Other Eye": []}

    def add_procedure(target, muscle, action, amount):
        if amount > 0:
            plan[target].append(f"{muscle} {action} of {amount:.1f} mm")

    def calculate_amount(base, step_size, step_increment):
        if deviation_value <= 15:
            return base
        else:
            return base + ((deviation_value - 15) // step_size) * step_increment

    def split_bilateral(amount):
        return round(amount / 2, 1), round(amount / 2, 1)

    if deviation_type == "Esotropia":
        mr_amount = calculate_amount(3, 5, 1)
        lr_amount = calculate_amount(3, 5, 1)
        if approach == "Unilateral":
            add_procedure("Affected Eye", "Medial Rectus", "recession", min(mr_amount, 12))
            if mr_amount > 12:
                add_procedure("Other Eye", "Medial Rectus", "recession", round(mr_amount - 12, 1))
            add_procedure("Affected Eye", "Lateral Rectus", "resection", lr_amount)
        else:
            r, l = split_bilateral(mr_amount)
            add_procedure("Affected Eye", "Medial Rectus", "recession", r)
            add_procedure("Other Eye", "Medial Rectus", "recession", l)

    elif deviation_type == "Exotropia":
        lr_amount = calculate_amount(4, 5, 1)
        mr_amount = calculate_amount(3, 5, 0.5)
        if approach == "Unilateral":
            add_procedure("Affected Eye", "Lateral Rectus", "recession", min(lr_amount, 12))
            if lr_amount > 12:
                add_procedure("Other Eye", "Lateral Rectus", "recession", round(lr_amount - 12, 1))
            add_procedure("Affected Eye", "Medial Rectus", "resection", mr_amount)
        else:
            r, l = split_bilateral(lr_amount)
            add_procedure("Affected Eye", "Lateral Rectus", "recession", r)
            add_procedure("Other Eye", "Lateral Rectus", "recession", l)

    elif deviation_type == "Hypertropia":
        sr_amount = calculate_amount(3, 5, 1)
        ir_amount = calculate_amount(3, 5, 1)
        if approach == "Unilateral":
            add_procedure("Affected Eye", "Superior Rectus", "recession", min(sr_amount, 12))
            if sr_amount > 12:
                add_procedure("Other Eye", "Superior Rectus", "recession", round(sr_amount - 12, 1))
            add_procedure("Affected Eye", "Inferior Rectus", "resection", ir_amount)
        else:
            r, l = split_bilateral(sr_amount)
            add_procedure("Affected Eye", "Superior Rectus", "recession", r)
            add_procedure("Other Eye", "Inferior Rectus", "recession", l)

    elif deviation_type == "Hypotropia":
        ir_amount = calculate_amount(3, 5, 1)
        sr_amount = calculate_amount(3, 5, 1)
        if approach == "Unilateral":
            add_procedure("Affected Eye", "Inferior Rectus", "recession", min(ir_amount, 12))
            if ir_amount > 12:
                add_procedure("Other Eye", "Inferior Rectus", "recession", round(ir_amount - 12, 1))
            add_procedure("Affected Eye", "Superior Rectus", "resection", sr_amount)
        else:
            r, l = split_bilateral(ir_amount)
            add_procedure("Affected Eye", "Inferior Rectus", "recession", r)
            add_procedure("Other Eye", "Superior Rectus", "recession", l)

    return plan
