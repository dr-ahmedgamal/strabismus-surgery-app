# logic.py

def calculate_recession_length(muscle: str, pd: int) -> float:
    if muscle == "LR":
        base = 4
        increment = 1
    else:
        base = 3
        increment = 1
    if pd < 15:
        return base
    return min(base + ((pd - 15) / 5) * increment, 12)

def calculate_resection_length(muscle: str, pd: int) -> float:
    if muscle == "LR":
        base = 4
        increment = 0.5
    else:
        base = 3
        increment = 0.5
    if pd < 15:
        return base
    return min(base + ((pd - 15) / 5) * increment, 9)

def unilateral_plan(deviation_type: str, pd: int) -> dict:
    plan = {}
    if deviation_type == "exotropia":
        recession = calculate_recession_length("LR", pd)
        resection = calculate_resection_length("MR", pd)
        if recession > 12 or resection > 9:
            return {"status": "Not allowed", "reason": "Exceeds muscle limits"}
        plan = {
            "LR recession (same eye)": round(recession, 2),
            "MR resection (same eye)": round(resection, 2)
        }
    elif deviation_type == "esotropia":
        recession = calculate_recession_length("MR", pd)
        resection = calculate_resection_length("LR", pd)
        if recession > 12 or resection > 9:
            return {"status": "Not allowed", "reason": "Exceeds muscle limits"}
        plan = {
            "MR recession (same eye)": round(recession, 2),
            "LR resection (same eye)": round(resection, 2)
        }
    elif deviation_type == "hypertropia":
        sr_recession = calculate_recession_length("SR", pd)
        ir_resection = calculate_resection_length("IR", pd)
        if sr_recession > 12 or ir_resection > 9:
            return {"status": "Not allowed", "reason": "Exceeds muscle limits"}
        plan = {
            "SR recession (same eye)": round(sr_recession, 2),
            "IR resection (same eye)": round(ir_resection, 2)
        }
    elif deviation_type == "hypotropia":
        ir_recession = calculate_recession_length("IR", pd)
        sr_resection = calculate_resection_length("SR", pd)
        if ir_recession > 12 or sr_resection > 9:
            return {"status": "Not allowed", "reason": "Exceeds muscle limits"}
        plan = {
            "IR recession (same eye)": round(ir_recession, 2),
            "SR resection (same eye)": round(sr_resection, 2)
        }
    plan["status"] = "Allowed"
    return plan

def bilateral_plan(deviation_type: str, pd: int) -> dict:
    plan = {}
    if deviation_type == "exotropia":
        lr_recession = calculate_recession_length("LR", pd / 2)
        if lr_recession * 2 >= 12:
            plan["Bilateral LR recession"] = round(lr_recession, 2)
        else:
            max_correction = (12 - 4) * 5 + 15  # 55 PD by max LR recession
            if pd <= max_correction:
                plan["Bilateral LR recession"] = round(lr_recession, 2)
            else:
                residual = pd - max_correction
                resection = calculate_resection_length("MR", residual * 2)
                plan["Bilateral LR recession"] = 12
                plan["MR resection (one eye)"] = round(resection, 2)
    elif deviation_type == "esotropia":
        mr_recession = calculate_recession_length("MR", pd / 2)
        if mr_recession * 2 >= 12:
            plan["Bilateral MR recession"] = round(mr_recession, 2)
        else:
            max_correction = (12 - 3) * 5 + 15  # 60 PD by max MR recession
            if pd <= max_correction:
                plan["Bilateral MR recession"] = round(mr_recession, 2)
            else:
                residual = pd - max_correction
                resection = calculate_resection_length("LR", residual * 2)
                plan["Bilateral MR recession"] = 12
                plan["LR resection (one eye)"] = round(resection, 2)
    elif deviation_type == "hypertropia":
        sr_recession = calculate_recession_length("SR", pd)
        ir_recession = calculate_recession_length("IR", pd)
        plan["SR recession (affected eye)"] = round(sr_recession, 2)
        plan["IR recession (opposite eye)"] = round(ir_recession, 2)
    elif deviation_type == "hypotropia":
        ir_recession = calculate_recession_length("IR", pd)
        sr_recession = calculate_recession_length("SR", pd)
        plan["IR recession (affected eye)"] = round(ir_recession, 2)
        plan["SR recession (opposite eye)"] = round(sr_recession, 2)
    return plan
