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

def max_pd_recession(muscle_type):
    if muscle_type == "LR":
        base = 4
        increment = 1
    else:
        base = 3
        increment = 1
    return 15 + ((12 - base) / increment) * 5

def max_pd_resection(muscle_type):
    if muscle_type == "LR":
        base = 4
        increment = 0.5
    else:
        base = 3
        increment = 0.5
    return 15 + ((9 - base) / increment) * 5

def unilateral_feasible(deviation_type, amount_pd):
    if deviation_type == "Exotropia":
        max_rec_pd = max_pd_recession("LR")
        max_res_pd = max_pd_resection("MR")
    elif deviation_type == "Esotropia":
        max_rec_pd = max_pd_recession("MR")
        max_res_pd = max_pd_resection("LR")
    elif deviation_type == "Hypertropia":
        max_rec_pd = max_pd_recession("SR")
        max_res_pd = max_pd_resection("IR")
    elif deviation_type == "Hypotropia":
        max_rec_pd = max_pd_recession("IR")
        max_res_pd = max_pd_resection("SR")
    else:
        return False

    max_unilateral_pd = max_rec_pd + max_res_pd
    return amount_pd <= max_unilateral_pd

def plan_unilateral(deviation_type, amount_pd):
    if not unilateral_feasible(deviation_type, amount_pd):
        return None  # Indicates unilateral NOT feasible

    result = {}
    if deviation_type == "Exotropia":
        recession = calculate_recession(amount_pd, "LR")
        resection = calculate_resection(amount_pd, "MR")
        result["Lateral Rectus Recession (affected eye)"] = round(recession, 2)
        result["Medial Rectus Resection (affected eye)"] = round(resection, 2)
    elif deviation_type == "Esotropia":
        recession = calculate_recession(amount_pd, "MR")
        resection = calculate_resection(amount_pd, "LR")
        result["Medial Rectus Recession (affected eye)"] = round(recession, 2)
        result["Lateral Rectus Resection (affected eye)"] = round(resection, 2)
    elif deviation_type == "Hypertropia":
        recession = calculate_recession(amount_pd, "SR")
        resection = calculate_resection(amount_pd, "IR")
        result["Superior Rectus Recession (affected eye)"] = round(recession, 2)
        result["Inferior Rectus Resection (affected eye)"] = round(resection, 2)
    elif deviation_type == "Hypotropia":
        recession = calculate_recession(amount_pd, "IR")
        resection = calculate_resection(amount_pd, "SR")
        result["Inferior Rectus Recession (affected eye)"] = round(recession, 2)
        result["Superior Rectus Resection (affected eye)"] = round(resection, 2)
    return result

def plan_bilateral(deviation_type, amount_pd):
    result = {}
    if deviation_type == "Exotropia":
        recession = calculate_recession(amount_pd, "LR")
        if recession <= 12:
            result["Lateral Rectus Recession (each eye)"] = round(recession, 2)
        else:
            result["Lateral Rectus Recession (each eye)"] = 12
            remaining_pd = amount_pd - (15 + (12 - 4) * 5)
            if remaining_pd > 0:
                resection = calculate_resection(remaining_pd * 2, "MR")
                if resection > 0:
                    result["Medial Rectus Resection (affected eye)"] = round(resection, 2)
    elif deviation_type == "Esotropia":
        recession = calculate_recession(amount_pd, "MR")
        if recession <= 12:
            result["Medial Rectus Recession (each eye)"] = round(recession, 2)
        else:
            result["Medial Rectus Recession (each eye)"] = 12
            remaining_pd = amount_pd - (15 + (12 - 3) * 5)
            if remaining_pd > 0:
                resection = calculate_resection(remaining_pd * 2, "LR")
                if resection > 0:
                    result["Lateral Rectus Resection (affected eye)"] = round(resection, 2)
    elif deviation_type == "Hypertropia":
        recession_sr = calculate_recession(amount_pd, "SR")
        recession_ir = calculate_recession(amount_pd, "IR")
        result["Superior Rectus Recession (affected eye)"] = round(min(recession_sr, 12), 2)
        result["Inferior Rectus Recession (opposite eye)"] = round(min(recession_ir, 12), 2)
        if recession_sr > 12:
            remaining_pd = amount_pd - (15 + (12 - 3) * 5)
            if remaining_pd > 0:
                resection = calculate_resection(remaining_pd * 2, "IR")
                if resection > 0:
                    result["Inferior Rectus Resection (affected eye)"] = round(resection, 2)
    elif deviation_type == "Hypotropia":
        recession_ir = calculate_recession(amount_pd, "IR")
        recession_sr = calculate_recession(amount_pd, "SR")
        result["Inferior Rectus Recession (affected eye)"] = round(min(recession_ir, 12), 2)
        result["Superior Rectus Recession (opposite eye)"] = round(min(recession_sr, 12), 2)
        if recession_ir > 12:
            remaining_pd = amount_pd - (15 + (12 - 3) * 5)
            if remaining_pd > 0:
                resection = calculate_resection(remaining_pd * 2, "SR")
                if resection > 0:
                    result["Superior Rectus Resection (affected eye)"] = round(resection, 2)
    return result
