def calculate_recession(amount_pd, muscle_type):
    if muscle_type == "LR":
        base = 4
        increment = 1
    else:  # MR, SR, IR
        base = 3
        increment = 1
    value = base + ((amount_pd - 15) / 5) * increment
    return min(value, 12)

def calculate_resection(amount_pd, muscle_type):
    if muscle_type == "LR":
        base = 4
        increment = 0.5
    else:  # MR, SR, IR
        base = 3
        increment = 0.5
    value = base + ((amount_pd - 15) / 5) * increment
    return min(value, 9)

def unilateral_feasible(deviation_type, amount_pd):
    # Check if unilateral correction is possible within limits
    if deviation_type == "Exotropia":
        rec = calculate_recession(amount_pd, "LR")
        res = calculate_resection(amount_pd, "MR")
        return rec <= 12 and res <= 9
    elif deviation_type == "Esotropia":
        rec = calculate_recession(amount_pd, "MR")
        res = calculate_resection(amount_pd, "LR")
        return rec <= 12 and res <= 9
    elif deviation_type == "Hypertropia":
        rec = calculate_recession(amount_pd, "SR")
        # resection limit not mandatory for unilateral approach feasibility 
        # but consider resection limit 9 mm to be consistent
        res = calculate_resection(amount_pd, "IR")
        return rec <= 12 and res <= 9
    elif deviation_type == "Hypotropia":
        rec = calculate_recession(amount_pd, "IR")
        res = calculate_resection(amount_pd, "SR")
        return rec <= 12 and res <= 9
    return False

def plan_unilateral(deviation_type, amount_pd):
    # Return None if not feasible
    if not unilateral_feasible(deviation_type, amount_pd):
        return None

    result = {}
    if deviation_type == "Exotropia":
        rec = calculate_recession(amount_pd, "LR")
        res = calculate_resection(amount_pd, "MR")
        result["Lateral Rectus recession"] = round(rec, 2)
        result["Medial Rectus resection"] = round(res, 2)

    elif deviation_type == "Esotropia":
        rec = calculate_recession(amount_pd, "MR")
        res = calculate_resection(amount_pd, "LR")
        result["Medial Rectus recession"] = round(rec, 2)
        result["Lateral Rectus resection"] = round(res, 2)

    elif deviation_type == "Hypertropia":
        rec = calculate_recession(amount_pd, "SR")
        res = calculate_resection(amount_pd, "IR")
        result["Superior Rectus recession"] = round(rec, 2)
        result["Inferior Rectus resection"] = round(res, 2)

    elif deviation_type == "Hypotropia":
        rec = calculate_recession(amount_pd, "IR")
        res = calculate_resection(amount_pd, "SR")
        result["Inferior Rectus recession"] = round(rec, 2)
        result["Superior Rectus resection"] = round(res, 2)

    return result

def plan_bilateral(deviation_type, amount_pd):
    result = {}

    if deviation_type == "Exotropia":
        rec = calculate_recession(amount_pd, "LR")
        if rec <= 12:
            # Bilateral recession only
            result["Lateral Rectus recession (each eye)"] = round(rec, 2)
        else:
            # Max bilateral recession
            result["Lateral Rectus recession (each eye)"] = 12
            # Calculate remaining PD beyond max bilateral recession
            max_pd_corrected = 15 + (12 - 4) * 5
            remaining_pd = amount_pd - max_pd_corrected
            if remaining_pd > 0:
                res = calculate_resection(remaining_pd * 2, "MR")
                result["Medial Rectus resection (affected eye)"] = round(res, 2)

    elif deviation_type == "Esotropia":
        rec = calculate_recession(amount_pd, "MR")
        if rec <= 12:
            result["Medial Rectus recession (each eye)"] = round(rec, 2)
        else:
            result["Medial Rectus recession (each eye)"] = 12
            max_pd_corrected = 15 + (12 - 3) * 5
            remaining_pd = amount_pd - max_pd_corrected
            if remaining_pd > 0:
                res = calculate_resection(remaining_pd * 2, "LR")
                result["Lateral Rectus resection (affected eye)"] = round(res, 2)

    elif deviation_type == "Hypertropia":
        rec_sr = calculate_recession(amount_pd, "SR")
        rec_ir = calculate_recession(amount_pd, "IR")

        # Both eyes get recession only, capped at 12 mm
        result["Superior Rectus recession (affected eye)"] = round(min(rec_sr, 12), 2)
        result["Inferior Rectus recession (opposite eye)"] = round(min(rec_ir, 12), 2)

        # If max recession on affected eye exceeded, calculate resection for remaining PD
        if rec_sr > 12:
            max_pd_corrected = 15 + (12 - 3) * 5
            remaining_pd = amount_pd - max_pd_corrected
            if remaining_pd > 0:
                res = calculate_resection(remaining_pd * 2, "IR")
                result["Inferior Rectus resection (affected eye)"] = round(res, 2)

    elif deviation_type == "Hypotropia":
        rec_ir = calculate_recession(amount_pd, "IR")
        rec_sr = calculate_recession(amount_pd, "SR")

        result["Inferior Rectus recession (affected eye)"] = round(min(rec_ir, 12), 2)
        result["Superior Rectus recession (opposite eye)"] = round(min(rec_sr, 12), 2)

        if rec_ir > 12:
            max_pd_corrected = 15 + (12 - 3) * 5
            remaining_pd = amount_pd - max_pd_corrected
            if remaining_pd > 0:
                res = calculate_resection(remaining_pd * 2, "SR")
                result["Superior Rectus resection (affected eye)"] = round(res, 2)

    return result
