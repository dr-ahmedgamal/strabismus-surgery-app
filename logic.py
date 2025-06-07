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
    result = {}
    if deviation_type == "Exotropia":
        recession = calculate_recession(amount_pd, "LR")
        resection = calculate_resection(amount_pd, "MR")
        if recession > 12 or resection > 9:
            return plan_bilateral(deviation_type, amount_pd)
        result["Lateral Rectus recession"] = round(recession, 2)
        result["Medial Rectus resection"] = round(resection, 2)
    elif deviation_type == "Esotropia":
        recession = calculate_recession(amount_pd, "MR")
        resection = calculate_resection(amount_pd, "LR")
        if recession > 12 or resection > 9:
            return plan_bilateral(deviation_type, amount_pd)
        result["Medial Rectus recession"] = round(recession, 2)
        result["Lateral Rectus resection"] = round(resection, 2)
    elif deviation_type == "Hypertropia":
        recession = calculate_recession(amount_pd, "SR")
        resection = calculate_resection(amount_pd, "IR")
        if recession > 12 or resection > 9:
            return plan_bilateral(deviation_type, amount_pd)
        result["Superior Rectus recession"] = round(recession, 2)
        result["Inferior Rectus resection"] = round(resection, 2)
    elif deviation_type == "Hypotropia":
        recession = calculate_recession(amount_pd, "IR")
        resection = calculate_resection(amount_pd, "SR")
        if recession > 12 or resection > 9:
            return plan_bilateral(deviation_type, amount_pd)
        result["Inferior Rectus recession"] = round(recession, 2)
        result["Superior Rectus resection"] = round(resection, 2)
    return result

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
