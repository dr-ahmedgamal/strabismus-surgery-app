def calculate_surgery(deviation_type, deviation_value, approach):
    plan = {"affected_eye": [], "other_eye": []}

    def calculate_amount(baseline, per_5_pd, deviation):
        # Calculate steps above baseline 15 PD
        steps = max((deviation - 15) // 5, 0)
        amount = baseline + steps * per_5_pd
        # Cap the maximum correction per muscle at 12 mm
        return min(amount, 12)

    def format_amt(x):
        return round(x, 1)

    def split_correction(amount):
        # If amount >12, split equally over two eyes (max 12 mm each)
        if amount > 12:
            half = amount / 2
            return format_amt(half), format_amt(half)
        else:
            return format_amt(amount), 0

    if deviation_type == "Esotropia":
        mr_total = 3 + max((deviation_value - 15) // 5, 0) * 1    # Medial Rectus baseline 3 mm + 1mm/5PD
        lr_total = 3 + max((deviation_value - 15) // 5, 0) * 1    # Lateral Rectus baseline 3 mm + 1mm/5PD

        if approach == "Unilateral":
            mr_amt, mr_other = split_correction(mr_total)
            lr_amt, lr_other = split_correction(lr_total)
            plan["affected_eye"].append(f"Medial Rectus recession of {mr_amt} mm")
            plan["affected_eye"].append(f"Lateral Rectus resection of {lr_amt} mm")
            if mr_other > 0 or lr_other > 0:
                plan["other_eye"].append(f"Medial Rectus recession of {mr_other} mm")
                plan["other_eye"].append(f"Lateral Rectus resection of {lr_other} mm")
        else:  # Bilateral approach
            mr_bi = format_amt(mr_total / 2)
            lr_bi = format_amt(lr_total / 2)
            plan["affected_eye"].append(f"Medial Rectus recession of {mr_bi} mm")
            plan["affected_eye"].append(f"Lateral Rectus resection of {lr_bi} mm")
            plan["other_eye"].append(f"Medial Rectus recession of {mr_bi} mm")
            plan["other_eye"].append(f"Lateral Rectus resection of {lr_bi} mm")

    elif deviation_type == "Exotropia":
        lr_total = 4 + max((deviation_value - 15) // 5, 0) * 1       # Lateral Rectus baseline 4 mm + 1mm/5PD
        mr_total = 3 + max((deviation_value - 15) // 5, 0) * 0.5     # Medial Rectus baseline 3 mm + 0.5mm/5PD

        if approach == "Unilateral":
            lr_amt, lr_other = split_correction(lr_total)
            mr_amt, mr_other = split_correction(mr_total)
            plan["affected_eye"].append(f"Lateral Rectus recession of {lr_amt} mm")
            plan["affected_eye"].append(f"Medial Rectus resection of {mr_amt} mm")
            if lr_other > 0 or mr_other > 0:
                if lr_other > 0:
                    plan["other_eye"].append(f"Lateral Rectus recession of {lr_other} mm")
                if mr_other > 0:
                    plan["other_eye"].append(f"Medial Rectus resection of {mr_other} mm")
        else:  # Bilateral approach
            lr_bi = format_amt(lr_total / 2)
            plan["affected_eye"].append(f"Lateral Rectus recession of {lr_bi} mm")
            plan["other_eye"].append(f"Lateral Rectus recession of {lr_bi} mm")

    elif deviation_type in ["Hypertropia", "Hypotropia"]:
        # Vertical deviations: same nomogram as medial rectus (3 mm baseline + 1 mm/5PD)
        amount_total = 3 + max((deviation_value - 15) // 5, 0) * 1
        if approach == "Unilateral":
            half = format_amt(amount_total)
            if deviation_type == "Hypertropia":
                plan["affected_eye"].append(f"Superior Rectus recession of {half} mm")
                plan["affected_eye"].append(f"Inferior Rectus resection of {half} mm")
            else:  # Hypotropia
                plan["affected_eye"].append(f"Inferior Rectus recession of {half} mm")
                plan["affected_eye"].append(f"Superior Rectus resection of {half} mm")
        else:
            half_bi = format_amt(amount_total / 2)
            if deviation_type == "Hypertropia":
                plan["affected_eye"].append(f"Superior Rectus recession of {half_bi} mm")
                plan["other_eye"].append(f"Inferior Rectus recession of {half_bi} mm")
            else:  # Hypotropia
                plan["affected_eye"].append(f"Inferior Rectus recession of {half_bi} mm")
                plan["other_eye"].append(f"Superior Rectus recession of {half_bi} mm")

    return plan
