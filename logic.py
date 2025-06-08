def calculate_recession(amount_pd, muscle_type):
    base = 4 if muscle_type == "LR" else 3
    increment = 1
    return base + ((amount_pd - 15) / 5) * increment

def calculate_resection(amount_pd, muscle_type):
    base = 4 if muscle_type == "LR" else 3
    increment = 0.5
    return base + ((amount_pd - 15) / 5) * increment

def is_within_limits(recession, resection):
    return recession <= 12 and resection <= 9

def plan_unilateral(deviation_type, amount_pd):
    result = {"approach": "Unilateral"}
    
    if deviation_type == "Exotropia":
        rec = calculate_recession(amount_pd, "LR")
        res = calculate_resection(amount_pd, "MR")
        if not is_within_limits(rec, res):
            return plan_bilateral(deviation_type, amount_pd)
        result["Lateral Rectus recession"] = round(rec, 2)
        result["Medial Rectus resection"] = round(res, 2)

    elif deviation_type == "Esotropia":
        rec = calculate_recession(amount_pd, "MR")
        res = calculate_resection(amount_pd, "LR")
        if not is_within_limits(rec, res):
            return plan_bilateral(deviation_type, amount_pd)
        result["Medial Rectus recession"] = round(rec, 2)
        result["Lateral Rectus resection"] = round(res, 2)

    elif deviation_type == "Hypertropia":
        rec = calculate_recession(amount_pd, "SR")
        res = calculate_resection(amount_pd, "IR")
        if not is_within_limits(rec, res):
            return plan_bilateral(deviation_type, amount_pd)
        result["Superior Rectus recession"] = round(rec, 2)
        result["Inferior Rectus resection"] = round(res, 2)

    elif deviation_type == "Hypotropia":
        rec = calculate_recession(amount_pd, "IR")
        res = calculate_resection(amount_pd, "SR")
        if not is_within_limits(rec, res):
            return plan_bilateral(deviation_type, amount_pd)
        result["Inferior Rectus recession"] = round(rec, 2)
        result["Superior Rectus resection"] = round(res, 2)

    return result

def plan_bilateral(deviation_type, amount_pd):
    result = {"approach": "Bilateral"}

    if deviation_type == "Exotropia":
        rec = calculate_recession(amount_pd, "LR")
        if rec <= 12:
            result["Lateral Rectus recession (each eye)"] = round(rec, 2)
        else:
            result["Lateral Rectus recession (each eye)"] = 12
            corrected = 15 + (12 - 4) * 5
            remaining = amount_pd - corrected
            if remaining > 0:
                res = calculate_resection(remaining * 2, "MR")
                result["Medial Rectus resection (affected eye)"] = round(res, 2)

    elif deviation_type == "Esotropia":
        rec = calculate_recession(amount_pd, "MR")
        if rec <= 12:
            result["Medial Rectus recession (each eye)"] = round(rec, 2)
        else:
            result["Medial Rectus recession (each eye)"] = 12
            corrected = 15 + (12 - 3) * 5
            remaining = amount_pd - corrected
            if remaining > 0:
                res = calculate_resection(remaining * 2, "LR")
                result["Lateral Rectus resection (affected eye)"] = round(res, 2)

    elif deviation_type == "Hypertropia":
        rec_sr = calculate_recession(amount_pd, "SR")
        rec_ir = calculate_recession(amount_pd, "IR")
        if rec_sr <= 12:
            result["Superior Rectus recession (affected eye)"] = round(rec_sr, 2)
        else:
            result["Superior Rectus recession (affected eye)"] = 12
            corrected = 15 + (12 - 3) * 5
            remaining = amount_pd - corrected
            if remaining > 0:
                res = calculate_resection(remaining * 2, "IR")
                result["Inferior Rectus resection (affected eye)"] = round(res, 2)
        result["Inferior Rectus recession (opposite eye)"] = round(min(rec_ir, 12), 2)

    elif deviation_type == "Hypotropia":
        rec_ir = calculate_recession(amount_pd, "IR")
        rec_sr = calculate_recession(amount_pd, "SR")
        if rec_ir <= 12:
            result["Inferior Rectus recession (affected eye)"] = round(rec_ir, 2)
        else:
            result["Inferior Rectus recession (affected eye)"] = 12
            corrected = 15 + (12 - 3) * 5
            remaining = amount_pd - corrected
            if remaining > 0:
                res = calculate_resection(remaining * 2, "SR")
                result["Superior Rectus resection (affected eye)"] = round(res, 2)
        result["Superior Rectus recession (opposite eye)"] = round(min(rec_sr, 12), 2)

    return result
