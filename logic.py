# logic.py

def calculate_muscle_mm(deviation_pd, muscle_type, surgery_type):
    """
    Calculate muscle recession or resection in mm based on deviation PD, muscle type, and surgery type.
    
    muscle_type: 'MR', 'LR', 'SR', 'IR'
    surgery_type: 'recession' or 'resection'
    
    Rules:
    - MR/SR/IR recession start 3 mm at 15 PD, +1 mm per 5 PD
    - MR/SR/IR resection start 3 mm at 15 PD, +0.5 mm per 5 PD
    - LR recession start 4 mm at 15 PD, +1 mm per 5 PD
    - LR resection start 4 mm at 15 PD, +0.5 mm per 5 PD
    - max limit 12 mm
    
    deviation_pd: amount of PD to correct by this muscle
    
    Returns the muscle measurement in mm (float).
    """
    if muscle_type in ['MR', 'SR', 'IR']:
        base_mm = 3 if surgery_type == 'recession' else 3
        base_pd = 15
        step_mm = 1 if surgery_type == 'recession' else 0.5
    elif muscle_type == 'LR':
        base_mm = 4 if surgery_type == 'recession' else 4
        base_pd = 15
        step_mm = 1 if surgery_type == 'recession' else 0.5
    else:
        raise ValueError(f"Invalid muscle type: {muscle_type}")
    
    # If deviation <= base_pd, return base_mm
    if deviation_pd <= base_pd:
        mm = base_mm
    else:
        steps = (deviation_pd - base_pd) / 5
        mm = base_mm + step_mm * steps
    
    # Limit max mm to 12
    if mm > 12:
        mm = 12
    
    return round(mm, 2)


def max_recession_pd(muscle_type):
    """
    Returns the maximum PD that can be corrected by maximal recession (12 mm) on given muscle.
    Calculated by inverting the formula:
    For MR/SR/IR recession: 3 mm at 15 PD + 1 mm per 5 PD step up to 12 mm max.
    So max PD = 15 + ((12 - 3) / 1) * 5 = 15 + 9*5 = 60 PD
    
    For LR recession similarly:
    base 4 mm at 15 PD, step 1 mm per 5 PD,
    max mm 12 mm:
    max PD = 15 + ((12 - 4)/1)*5 = 15 + 8*5 = 55 PD
    """
    if muscle_type in ['MR', 'SR', 'IR']:
        return 60
    elif muscle_type == 'LR':
        return 55
    else:
        raise ValueError(f"Invalid muscle type: {muscle_type}")


def calculate_plan(deviation_pd, deviation_type, approach):
    """
    Calculate the surgical plan based on deviation PD, deviation type, and approach.
    
    deviation_type: 'esotropia', 'exotropia', 'hypertropia', 'hypotropia'
    approach: 'unilateral' or 'bilateral'
    
    Returns a dict with muscle names as keys and their recession/resection mm as values.
    """
    plan = {}

    # Define involved muscles by deviation type
    # For horizontal:
    #   esotropia: MR affected (recession), LR affected (resection)
    #   exotropia: LR affected (recession), MR affected (resection)
    # For vertical:
    #   hypertropia: SR affected (recession), IR contralateral (recession)
    #   hypotropia: IR affected (recession), SR contralateral (recession)
    
    if deviation_type == 'esotropia':
        rec_muscle = 'MR'
        res_muscle = 'LR'
    elif deviation_type == 'exotropia':
        rec_muscle = 'LR'
        res_muscle = 'MR'
    elif deviation_type == 'hypertropia':
        rec_muscle_affected = 'SR'
        rec_muscle_contra = 'IR'
    elif deviation_type == 'hypotropia':
        rec_muscle_affected = 'IR'
        rec_muscle_contra = 'SR'
    else:
        raise ValueError(f"Invalid deviation type: {deviation_type}")
    
    # Helper function for large deviation correction
    def resection_amount(remaining_pd, approach_type, muscle_type):
        # For bilateral recessions max limit exceeded, remaining PD corrected by resection on affected side doubled
        # For unilateral approach no doubling of resection needed
        if approach_type == 'bilateral':
            return (remaining_pd * 2)
        else:
            return remaining_pd

    # Horizontal deviations
    if deviation_type in ['esotropia', 'exotropia']:
        max_rec_pd = max_recession_pd(rec_muscle)
        
        if approach == 'bilateral':
            # Both muscles recess 12 mm max for correction
            max_total_rec_pd = 2 * max_rec_pd
            
            if deviation_pd <= max_total_rec_pd:
                # Divide deviation equally for bilateral recessions
                per_muscle_pd = deviation_pd / 2
                rec_mm = calculate_muscle_mm(per_muscle_pd, rec_muscle, 'recession')
                plan[f"{rec_muscle} recession (eye 1)"] = rec_mm
                plan[f"{rec_muscle} recession (eye 2)"] = rec_mm
                # no resection needed
            else:
                # Max recessions done bilaterally
                plan[f"{rec_muscle} recession (eye 1)"] = 12
                plan[f"{rec_muscle} recession (eye 2)"] = 12
                remaining_pd = deviation_pd - max_total_rec_pd
                # resection on affected side, doubled PD correction
                res_pd = resection_amount(remaining_pd, approach, res_muscle)
                res_mm = calculate_muscle_mm(res_pd, res_muscle, 'resection')
                plan[f"{res_muscle} resection (affected eye)"] = res_mm
                
        else:  # unilateral
            max_rec_pd_unilateral = max_rec_pd
            if deviation_pd <= max_rec_pd_unilateral:
                rec_mm = calculate_muscle_mm(deviation_pd, rec_muscle, 'recession')
                plan[f"{rec_muscle} recession (affected eye)"] = rec_mm
                # no resection
            else:
                plan[f"{rec_muscle} recession (affected eye)"] = 12
                remaining_pd = deviation_pd - max_rec_pd_unilateral
                res_mm = calculate_muscle_mm(remaining_pd, res_muscle, 'resection')
                plan[f"{res_muscle} resection (affected eye)"] = res_mm

    # Vertical deviations
    else:
        max_rec_pd_affected = max_recession_pd(rec_muscle_affected)
        max_rec_pd_contra = max_recession_pd(rec_muscle_contra)
        
        if approach == 'bilateral':
            max_total_rec_pd = max_rec_pd_affected + max_rec_pd_contra
            if deviation_pd <= max_total_rec_pd:
                # Bilateral recessions on affected and contralateral eye
                # Assign PDs proportional to each muscle's max correction capacity (optional: here equal split)
                # To simplify, split deviation equally (can be customized)
                per_muscle_pd_affected = deviation_pd / 2
                per_muscle_pd_contra = deviation_pd / 2
                rec_mm_affected = calculate_muscle_mm(per_muscle_pd_affected, rec_muscle_affected, 'recession')
                rec_mm_contra = calculate_muscle_mm(per_muscle_pd_contra, rec_muscle_contra, 'recession')
                plan[f"{rec_muscle_affected} recession (affected eye)"] = rec_mm_affected
                plan[f"{rec_muscle_contra} recession (contralateral eye)"] = rec_mm_contra
            else:
                plan[f"{rec_muscle_affected} recession (affected eye)"] = 12
                plan[f"{rec_muscle_contra} recession (contralateral eye)"] = 12
                remaining_pd = deviation_pd - max_total_rec_pd
                # Remaining corrected by resection on affected side doubled
                res_pd = resection_amount(remaining_pd, approach, rec_muscle_affected)
                res_mm = calculate_muscle_mm(res_pd, rec_muscle_affected, 'resection')
                plan[f"{rec_muscle_affected} resection (affected eye)"] = res_mm
        
        else:  # unilateral
            if deviation_pd <= max_rec_pd_affected:
                rec_mm = calculate_muscle_mm(deviation_pd, rec_muscle_affected, 'recession')
                plan[f"{rec_muscle_affected} recession (affected eye)"] = rec_mm
            else:
                plan[f"{rec_muscle_affected} recession (affected eye)"] = 12
                remaining_pd = deviation_pd - max_rec_pd_affected
                res_mm = calculate_muscle_mm(remaining_pd, rec_muscle_affected, 'resection')
                plan[f"{rec_muscle_affected} resection (affected eye)"] = res_mm
                
    return plan
