def calculate_recession(amount_pd, muscle_type):
    """
    Calculate recession mm for given PD and muscle.
    Max recession = 12 mm.
    """
    if muscle_type == "LR":
        base = 4
        increment = 1
    else:  # MR, SR, IR
        base = 3
        increment = 1

    recession = base + ((amount_pd - 15) / 5) * increment
    return min(round(recession, 2), 12)


def calculate_resection(amount_pd, muscle_type):
    """
    Calculate resection mm for given PD and muscle.
    Max resection = 9 mm.
    """
    if muscle_type == "LR":
        base = 4
        increment = 0.5
    else:  # MR, SR, IR
        base = 3
        increment = 0.5

    resection = base + ((amount_pd - 15) / 5) * increment
    return min(round(resection, 2), 9)


def max_recession_pd(muscle_type):
    """
    Returns the max PD that can be corrected by recession alone for given muscle.
    """
    if muscle_type == "LR":
        base = 4
        increment = 1
        max_mm = 12
    else:
        base = 3
        increment = 1
        max_mm = 12

    max_pd = 15 + ((max_mm - base) / increment) * 5
    return max_pd


def max_resection_pd(muscle_type):
    """
    Returns the max PD that can be corrected by resection alone for given muscle.
    """
    if muscle_type == "LR":
        base = 4
        increment = 0.5
        max_mm = 9
    else:
        base = 3
        increment = 0.5
        max_mm = 9

    max_pd = 15 + ((max_mm - base) / increment) * 5
    return max_pd


def unilateral_feasible(deviation_type, amount_pd):
    """
    Returns True if unilateral correction can fully correct the deviation.
    """
    if deviation_type == "Exotropia":
        max_rec_pd = max_recession_pd("LR")
        max_res_pd = max_resection_pd("MR")
    elif deviation_type == "Esotropia":
        max_rec_pd = max_recession_pd("MR")
        max_res_pd = max_resection_pd("LR")
    elif deviation_type == "Hypertropia":
        max_rec_pd = max_recession_pd("SR")
        max_res_pd = max_resection_pd("IR")
    elif deviation_type == "Hypotropia":
        max_rec_pd = max_recession_pd("IR")
        max_res_pd = max_resection_pd("SR")
    else:
        return False

    max_total_pd = max_rec_pd + max_res_pd
    return amount_pd <= max_total_pd


def plan_unilateral(deviation_type, amount_pd):
    """
    Returns unilateral surgical plan dict or None if not feasible.
    """
    if not unilateral_feasible(deviation_type, amount_pd):
        return None

    plan = {}

    if deviation_type == "Exotropia":
        plan["Lateral Rectus Recession (affected eye)"] = calculate_recession(amount_pd, "LR")
        plan["Medial Rectus Resection (affected eye)"] = calculate_resection(amount_pd, "MR")

    elif deviation_type == "Esotropia":
        plan["Medial Rectus Recession (affected eye)"] = calculate_recession(amount_pd, "MR")
        plan["Lateral Rectus Resection (affected eye)"] = calculate_resection(amount_pd, "LR")

    elif deviation_type == "Hypertropia":
        plan["Superior Rectus Recession (affected eye)"] = calculate_recession(amount_pd, "SR")
        plan["Inferior Rectus Resection (affected eye)"] = calculate_resection(amount_pd, "IR")

    elif deviation_type == "Hypotropia":
        plan["Inferior Rectus Recession (affected eye)"] = calculate_recession(amount_pd, "IR")
        plan["Superior Rectus Resection (affected eye)"] = calculate_resection(amount_pd, "SR")

    return plan


def plan_bilateral(deviation_type, amount_pd):
    """
    Returns bilateral surgical plan dict.
    Includes bilateral recessions (both eyes), and resection of affected eye if needed.
    """

    plan = {}

    # Get muscle types for recession and resection depending on deviation
    if deviation_type == "Exotropia":
        rec_muscle = "LR"
        res_muscle = "MR"
        rec_name = "Lateral Rectus Recession (each eye)"
        res_name = "Medial Rectus Resection (affected eye)"
    elif deviation_type == "Esotropia":
        rec_muscle = "MR"
        res_muscle = "LR"
        rec_name = "Medial Rectus Recession (each eye)"
        res_name = "Lateral Rectus Resection (affected eye)"
    elif deviation_type == "Hypertropia":
        rec_muscle = "SR"
        res_muscle = "IR"
        rec_name_affected = "Superior Rectus Recession (affected eye)"
        rec_name_opposite = "Inferior Rectus Recession (opposite eye)"
        res_name = "Inferior Rectus Resection (affected eye)"
    elif deviation_type == "Hypotropia":
        rec_muscle = "IR"
        res_muscle = "SR"
        rec_name_affected = "Inferior Rectus Recession (affected eye)"
        rec_name_opposite = "Superior Rectus Recession (opposite eye)"
        res_name = "Superior Rectus Resection (affected eye)"
    else:
        return plan

    # Bilateral recessions correct up to max recession PD x 2 (both eyes)
    max_rec_pd = max_recession_pd(rec_muscle) * 2

    if deviation_type in ["Exotropia", "Esotropia"]:
        # Bilateral recession PD to half for each eye
        if amount_pd <= max_rec_pd:
            # Equal recession both eyes
            recession_per_eye = calculate_recession(amount_pd / 2, rec_muscle)
            plan[rec_name] = recession_per_eye
        else:
            # Max recession bilateral
            plan[rec_name] = 12  # max recession mm per eye

            # Residual PD after max bilateral recession
            residual_pd = amount_pd - max_rec_pd
            # Resection uses residual PD doubled (unilateral resection effect)
            resection_mm = calculate_resection(residual_pd * 2, res_muscle)
            if resection_mm > 0:
                plan[res_name] = resection_mm

    else:  # vertical deviations handled differently
        # Superior and Inferior Rectus recessions in opposite eyes
        # Both recessions max 12 mm each
        recession_affected = calculate_recession(amount_pd, rec_muscle)
        recession_opposite = calculate_recession(amount_pd, res_muscle)  # opposite muscle is other rectus

        plan[rec_name_affected] = recession_affected
        plan[rec_name_opposite] = recession_opposite

        # If affected recession hits max 12 mm, residual PD corrected by resection in affected eye
        if recession_affected >= 12:
            max_rec_pd_vert = max_recession_pd(rec_muscle)
            residual_pd = amount_pd - max_rec_pd_vert
            if residual_pd > 0:
                resection_mm = calculate_resection(residual_pd * 2, res_muscle)
                if resection_mm > 0:
                    plan[res_name] = resection_mm

    return plan
