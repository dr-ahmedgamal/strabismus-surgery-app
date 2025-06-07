def calculate_recession(amount_pd, muscle_type):
    base = 4 if muscle_type == "LR" else 3
    increment = 1
    return base + ((amount_pd - 15) / 5) * increment

def calculate_resection(amount_pd, muscle_type):
    base = 4 if muscle_type == "LR" else 3
    increment = 0.5
    return base + ((amount_pd - 15) / 5) * increment

def plan_unilateral(deviation_type, amount_pd):
    MAX_REC = 12
    MAX_RES = 9

    if deviation_type == "Exotropia":
        rec = calculate_recession(amount_pd, "LR")
        res = calculate_resection(amount_pd, "MR")
        if rec > MAX_REC or res > MAX_RES:
            return plan_bilateral(deviation_type, amount_pd), True
        return {
            "Lateral Rectus recession (same eye)": round(rec, 2),
            "Medial Rectus resection (same eye)": round(res, 2)
        }, False

    elif deviation_type == "Esotropia":
        rec = calculate_recession(amount_pd, "MR")
        res = calculate_resection(amount_pd, "LR")
        if rec > MAX_REC or res > MAX_RES:
            return plan_bilateral(deviation_type, amount_pd), True
        return {
            "Medial Rectus recession (same eye)": round(rec, 2),
            "Lateral Rectus resection (same eye)": round(res, 2)
        }, False

    elif deviation_type == "Hypertropia":
        rec = calculate_recession(amount_pd, "SR")
        res = calculate_resection(amount_pd, "IR")
        if rec > MAX_REC or res > MAX_RES:
            return plan_bilateral(deviation_type, amount_pd), True
        return {
            "Superior Rectus recession (same eye)": round(rec, 2),
            "Inferior Rectus resection (same eye)": round(res, 2)
        }, False

    elif deviation_type == "Hypotropia":
        rec = calculate_recession(amount_pd, "IR")
        res = calculate_resection(amount_pd, "SR")
        if rec > MAX_REC or res > MAX_RES:
            return plan_bilateral(deviation_type, amount_pd), True
        return {
            "Inferior Rectus recession (same eye)": round(rec, 2),
            "Superior Rectus resection (same eye)": round(res, 2)
        }, False
