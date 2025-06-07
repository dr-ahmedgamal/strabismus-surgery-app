def calculate_recession(amount_pd, muscle_type):
    base = 4 if muscle_type == "LR" else 3
    increment = 1
    return min(base + ((amount_pd - 15) / 5) * increment, 12)

def calculate_resection(amount_pd, muscle_type):
    base = 4 if muscle_type == "LR" else 3
    increment = 0.5
    return min(base + ((amount_pd - 15) / 5) * increment, 9)

def plan_unilateral(deviation_type, amount_pd):
    result = {}
    converted = False

    if deviation_type == "Exotropia":
        rec = calculate_recession(amount_pd, "LR")
        res = calculate_resection(amount_pd, "MR")
        if rec > 12 or res > 9:
            return plan_bilateral(deviation_type, amount_pd), True
        result["Lateral Rectus recession (same eye)"] = round(rec, 2)
        result["Medial Rectus resection (same eye)"] = round(res, 2)

    elif deviation_type == "Esotropia":
        rec = calculate_recession(amount_pd, "MR")
        res = calculate_resection(amount_pd, "LR")
        if rec > 12 or res > 9:
            return plan_bilateral(deviation_type, amount_pd), True
        result["Medial Rectus recession (same eye)"] = round(rec, 2)
        result["Lateral Rectus resection (same eye)"] = round(res, 2)

    elif deviation_type == "Hypertropia":
        rec = calculate_recession(amount_pd, "SR")
        res = calculate_resection(amount_pd, "IR")
        if rec > 12 or res > 9:
            return plan_bilateral(deviation_type, amount_pd), True
        result["Superior Rectus recession (same eye)"] = round(rec, 2)
        result["Inferior Rectus resection (same eye)"] = round(res, 2)

    elif deviation_type == "Hypotropia":
        rec = calculate_recession(amount_pd, "IR")
        res = calculate_resection(amount_pd, "SR")
        if rec > 12 or res > 9:
            return plan_bilateral(deviation_type, amount_pd), True
        result["Inferior Rectus recession (same eye)"] = round(rec, 2)
        result["Superior Rectus resection (same eye)"] = round(res, 2)

    return result, False

def plan_bilateral(deviation_type, amount_pd):
    result = {}

    if deviation_type == "Exotropia":
        max_pd = 15 + (12 - 4) * 5  # 55 PD max by recession
        if amount_pd <= max_pd:
            rec = calculate_recession(amount_pd, "LR")
            result["Lateral Rectus recession (each eye)"] = round(rec, 2)
        else:
            result["Lateral Rectus recession (each eye)"] = 12
            remaining_pd = amount_pd - max_pd
            res = calculate_resection(remaining_pd * 2, "MR")
            result["Medial Rectus resection (one eye)"] = round(res, 2)

    elif deviation_type == "Esotropia":
        max_pd = 15 + (12 - 3) * 5  # 60 PD max by recession
        if amount_pd <= max_pd:
            rec = calculate_recession(amount_pd, "MR")
            result["Medial Rectus recession (each eye)"] = round(rec, 2)
        else:
            result["Medial Rectus recession (each eye)"] = 12
            remaining_pd = amount_pd - max_pd
            res = calculate_resection(remaining_pd * 2, "LR")
            result["Lateral Rectus resection (one eye)"] = round(res, 2)

    elif deviation_type == "Hypertropia":
        max_pd = 15 + (12 - 3) * 5  # 60 PD
        sr_rec = calculate_recession(min(amount_pd, max_pd), "SR")
        ir_rec = calculate_recession(min(amount_pd, max_pd), "IR")
        result["Superior Rectus recession (affected eye)"] = round(sr_rec, 2)
        result["Inferior Rectus recession (opposite eye)"] = round(ir_rec, 2)
        if amount_pd > max_pd:
            remaining_pd = amount_pd - max_pd
            res = calculate_resection(remaining_pd * 2, "IR")
            result["Inferior Rectus resection (affected eye)"] = round(res, 2)

    elif deviation_type == "Hypotropia":
        max_pd = 15 + (12 - 3) * 5
        ir_rec = calculate_recession(min(amount_pd, max_pd), "IR")
        sr_rec = calculate_recession(min(amount_pd, max_pd), "SR")
        result["Inferior Rectus recession (affected eye)"] = round(ir_rec, 2)
        result["Superior Rectus recession (opposite eye)"] = round(sr_rec, 2)
        if amount_pd > max_pd:
            remaining_pd = amount_pd - max_pd
            res = calculate_resection(remaining_pd * 2, "SR")
            result["Superior Rectus resection (affected eye)"] = round(res, 2)

    return result
