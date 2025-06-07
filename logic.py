def calculate_surgery(deviation_type, deviation_value, approach):
    plan = []

    def add_procedure(eye, muscle, action, amount):
        if amount > 0:
            plan.append((eye, f"{muscle} {action} of {amount:.1f} mm"))

    def split_bilateral(amount):
        half = round(amount / 2, 1)
        return half, half

    def handle_large_correction(amount, baseline, step_mm, muscle, action, opposite_muscle=None):
        # amount is the total mm calculated including baseline
        if amount <= 12:
            return [(muscle, action, amount)]
        else:
            # split equally but max 12 per eye (or muscle)
            half = amount / 2
            half = min(12, round(half, 1))
            remainder = round(amount - half, 1)
            corrections = [(muscle, action, half)]
            if opposite_muscle:
                corrections.append((opposite_muscle, action, half))
            else:
                corrections.append((muscle, action, remainder))
            return corrections

    # Helper to calculate steps over baseline of 15 PD
    def steps_over_15(pd):
        return max(0, (pd - 15) // 5)

    if deviation_type == "Esotropia":
        # Baseline 3 mm for MR recession and LR resection
        steps = steps_over_15(deviation_value)
        mr_recession = 3 + steps * 1.0
        lr_resection = 3 + steps * 1.0

        if approach == "Unilateral":
            # Handle large corrections by splitting if > 12
            mr_corr = handle_large_correction(mr_recession, 3, 1, "Medial Rectus", "recession")
            for muscle, action, amt in mr_corr:
                add_procedure("Affected Eye", muscle, action, amt)
            lr_corr = handle_large_correction(lr_resection, 3, 1, "Lateral Rectus", "resection")
            for muscle, action, amt in lr_corr:
                add_procedure("Affected Eye", muscle, action, amt)

        else:  # Bilateral MR recessions
            mr_corr = handle_large_correction(mr_recession, 3, 1, "Medial Rectus", "recession", opposite_muscle="Medial Rectus")
            # Split equally across eyes
            if len(mr_corr) == 1:
                # amount <= 12, split evenly
                half1, half2 = split_bilateral(mr_corr[0][2])
                add_procedure("Affected Eye", mr_corr[0][0], mr_corr[0][1], half1)
                add_procedure("Contralateral Eye", mr_corr[0][0], mr_corr[0][1], half2)
            else:
                # large correction split on two muscles (same muscle different eyes)
                for i, (muscle, action, amt) in enumerate(mr_corr):
                    eye = "Affected Eye" if i == 0 else "Contralateral Eye"
                    add_procedure(eye, muscle, action, amt)

    elif deviation_type == "Exotropia":
        steps = steps_over_15(deviation_value)
        lr_recession = 4 + steps * 1.0
        mr_resection = 3 + steps * 0.5

        if approach == "Unilateral":
            lr_corr = handle_large_correction(lr_recession, 4, 1, "Lateral Rectus", "recession")
            for muscle, action, amt in lr_corr:
                add_procedure("Affected Eye", muscle, action, amt)
            mr_corr = handle_large_correction(mr_resection, 3, 0.5, "Medial Rectus", "resection")
            for muscle, action, amt in mr_corr:
                add_procedure("Affected Eye", muscle, action, amt)

        else:  # Bilateral LR recessions
            lr_corr = handle_large_correction(lr_recession, 4, 1, "Lateral Rectus", "recession", opposite_muscle="Lateral Rectus")
            if len(lr_corr) == 1:
                half1, half2 = split_bilateral(lr_corr[0][2])
                add_procedure("Affected Eye", lr_corr[0][0], lr_corr[0][1], half1)
                add_procedure("Contralateral Eye", lr_corr[0][0], lr_corr[0][1], half2)
            else:
                for i, (muscle, action, amt) in enumerate(lr_corr):
                    eye = "Affected Eye" if i == 0 else "Contralateral Eye"
                    add_procedure(eye, muscle, action, amt)

    elif deviation_type == "Hypertropia":
        steps = steps_over_15(deviation_value)
        # Recession - baseline 3 + 1 mm per 5 PD step
        recession_amount = 3 + steps * 1.0
        # Resection - baseline 3 + 0.5 mm per 5 PD step
        resection_amount = 3 + steps * 0.5

        if approach == "Unilateral":
            # Affected Eye Superior Rectus recession
            add_procedure("Affected Eye", "Superior Rectus", "recession", recession_amount)
            # Affected Eye Inferior Rectus resection
            add_procedure("Affected Eye", "Inferior Rectus", "resection", resection_amount)
        else:
            # Bilateral recession of Superior Rectus and Inferior Rectus on contralateral
            add_procedure("Affected Eye", "Superior Rectus", "recession", recession_amount)
            add_procedure("Contralateral Eye", "Inferior Rectus", "recession", recession_amount)

    elif deviation_type == "Hypotropia":
        steps = steps_over_15(deviation_value)
        recession_amount = 3 + steps * 1.0
        resection_amount = 3 + steps * 0.5

        if approach == "Unilateral":
            add_procedure("Affected Eye", "Inferior Rectus", "recession", recession_amount)
            add_procedure("Affected Eye", "Superior Rectus", "resection", resection_amount)
        else:
            add_procedure("Affected Eye", "Inferior Rectus", "recession", recession_amount)
            add_procedure("Contralateral Eye", "Superior Rectus", "recession", recession_amount)

    return plan
