def calculate_recession(amount_pd, muscle_type):
    if muscle_type == "LR":
        base = 4
        increment = 1
    else:  # MR, SR, IR
        base = 3
        increment = 1
    return min(base + ((amount_pd - 15) / 5) * increment, 12)

def calculate_resection(amount_pd, muscle_type):
    if muscle_type == "LR":
        base = 4
        increment = 0.5
    else:  # MR, SR, IR
        base = 3
        increment = 0.5
    return min(base + ((amount_pd - 15) / 5) * increment, 9)

def plan_unilateral(deviation_type, amount_pd):
    # Returns (plan_dict, converted_flag)
    # converted_flag True means unilateral NOT feasible and plan is bilateral
    if deviation_type == "Exotropia":
        rec = calculate_recession(amount_pd, "LR")
        res = calculate_resection(amount_pd, "MR")
        if rec > 12 or res > 9:
            return plan_bilateral(deviation_type, amount_pd), True
        return {
            "Lateral Rectus recession (same eye)": round(rec, 2),
            "Medial Rectus resection (same eye)": round(res, 2)
        }, False

    elif deviation_type == "Esotropia":
        rec = calculate_recession(amount_pd, "MR")
        res = calculate_resection(amount_pd, "LR")
        if rec > 12 or res > 9:
            return plan_bilateral(deviation_type, amount_pd), True
        return {
            "Medial Rectus recession (same eye)": round(rec, 2),
            "Lateral Rectus resection (same eye)": round(res, 2)
        }, False

    elif deviation_type == "Hypertropia":
        rec = calculate_recession(amount_pd, "SR")
        res = calculate_resection(amount_pd, "IR")
        if rec > 12 or res > 9:
            return plan_bilateral(deviation_type, amount_pd), True
        return {
            "Superior Rectus recession (same eye)": round(rec, 2),
            "Inferior Rectus resection (same eye)": round(res, 2)
        }, False

    elif deviation_type == "Hypotropia":
        rec = calculate_recession(amount_pd, "IR")
        res = calculate_resection(amount_pd, "SR")
        if rec > 12 or res > 9:
            return plan_bilateral(deviation_type, amount_pd), True
        return {
            "Inferior Rectus recession (same eye)": round(rec, 2),
            "Superior Rectus resection (same eye)": round(res, 2)
        }, False

def plan_bilateral(deviation_type, amount_pd):
    result = {}
    if deviation_type == "Exotropia":
        recession = calculate_recession(amount_pd, "LR")
        if recession <= 12:
            result["Lateral Rectus recession (each eye)"] = round(recession, 2)
        else:
            result["Lateral Rectus recession (each eye)"] = 12
            remaining_pd = amount_pd - (15 + (12 - 4) * 5)
            if remaining_pd > 0:
                resection = calculate_resection(remaining_pd * 2, "MR")
                result["Medial Rectus resection (affected eye)"] = round(resection, 2)

    elif deviation_type == "Esotropia":
        recession = calculate_recession(amount_pd, "MR")
        if recession <= 12:
            result["Medial Rectus recession (each eye)"] = round(recession, 2)
        else:
            result["Medial Rectus recession (each eye)"] = 12
            remaining_pd = amount_pd - (15 + (12 - 3) * 5)
            if remaining_pd > 0:
                resection = calculate_resection(remaining_pd * 2, "LR")
                result["Lateral Rectus resection (affected eye)"] = round(resection, 2)

    elif deviation_type == "Hypertropia":
        recession_sr = calculate_recession(amount_pd, "SR")
        recession_ir = calculate_recession(amount_pd, "IR")
        result["Superior Rectus recession (affected eye)"] = round(min(recession_sr, 12), 2)
        result["Inferior Rectus recession (opposite eye)"] = round(min(recession_ir, 12), 2)
        if recession_sr > 12:
            remaining_pd = amount_pd - (15 + (12 - 3) * 5)
            if remaining_pd > 0:
                resection = calculate_resection(remaining_pd * 2, "IR")
                result["Inferior Rectus resection (affected eye)"] = round(resection, 2)

    elif deviation_type == "Hypotropia":
        recession_ir = calculate_recession(amount_pd, "IR")
        recession_sr = calculate_recession(amount_pd, "SR")
        result["Inferior Rectus recession (affected eye)"] = round(min(recession_ir, 12), 2)
        result["Superior Rectus recession (opposite eye)"] = round(min(recession_sr, 12), 2)
        if recession_ir > 12:
            remaining_pd = amount_pd - (15 + (12 - 3) * 5)
            if remaining_pd > 0:
                resection = calculate_resection(remaining_pd * 2, "SR")
                result["Superior Rectus resection (affected eye)"] = round(resection, 2)

    return result
