# logic.py

# Constants for maximum muscle lengths
MAX_RECESSION = 12  # mm max recession length per muscle
MAX_RESECTION = 9   # mm max resection length per muscle

def recession_length(muscle: str, PD: float) -> float:
    """
    Calculate recession length for given muscle and PD.
    """
    if muscle.lower() == 'lr':
        base = 4
        increment = 1
    elif muscle.lower() in ['mr', 'sr', 'ir']:
        base = 3
        increment = 1
    else:
        raise ValueError(f"Unknown muscle: {muscle}")
    
    length = base + ((PD - 15) / 5) * increment
    return min(length, MAX_RECESSION)

def resection_length(muscle: str, PD: float) -> float:
    """
    Calculate resection length for given muscle and PD.
    """
    if muscle.lower() == 'lr':
        base = 4
        increment = 0.5
    elif muscle.lower() in ['mr', 'sr', 'ir']:
        base = 3
        increment = 0.5
    else:
        raise ValueError(f"Unknown muscle: {muscle}")
    
    length = base + ((PD - 15) / 5) * increment
    return min(length, MAX_RESECTION)

def unilateral_approach(deviation_type: str, PD: float) -> dict:
    """
    Calculate unilateral approach surgery plan.
    Two muscles (agonist + antagonist) operated in the same eye.
    Use full PD as-is in formulas, no halving or doubling.
    Return dict with muscle names and lengths.
    """
    if deviation_type.lower() == 'esotropia':
        # MR recession + LR resection
        recession_muscle = 'mr'
        resection_muscle = 'lr'
    elif deviation_type.lower() == 'exotropia':
        # LR recession + MR resection
        recession_muscle = 'lr'
        resection_muscle = 'mr'
    elif deviation_type.lower() == 'hypertropia':
        # SR recession + IR resection (same eye)
        recession_muscle = 'sr'
        resection_muscle = 'ir'
    elif deviation_type.lower() == 'hypotropia':
        # IR recession + SR resection (same eye)
        recession_muscle = 'ir'
        resection_muscle = 'sr'
    else:
        raise ValueError("Unsupported deviation type for unilateral approach")
    
    recess_len = recession_length(recession_muscle, PD)
    resect_len = resection_length(resection_muscle, PD)

    # Check if either exceeds max length, if yes, unilateral approach not feasible
    if recess_len >= MAX_RECESSION or resect_len >= MAX_RESECTION:
        return {"error": "Unilateral approach not feasible for this PD due to muscle length limits."}

    return {
        f"{recession_muscle}_recession_mm": round(recess_len, 2),
        f"{resection_muscle}_resection_mm": round(resect_len, 2)
    }

def bilateral_approach(deviation_type: str, PD: float) -> dict:
    """
    Calculate bilateral approach surgery plan.
    Both eyes operated.
    Usually bilateral recessions only.
    If PD > maximum correction by recessions, add resection in affected eye for residual PD doubled.
    Return dict with muscle names and lengths.
    """
    if deviation_type.lower() in ['esotropia', 'exotropia']:
        if deviation_type.lower() == 'esotropia':
            recess_muscle = 'mr'
            resect_muscle = 'lr'
        else:
            recess_muscle = 'lr'
            resect_muscle = 'mr'

        # Maximum PD correctable by bilateral recession (pair of muscles)
        max_recession_PD = 15 + 5 * (MAX_RECESSION - (4 if recess_muscle=='lr' else 3))

        if PD <= max_recession_PD:
            # Recession alone bilaterally (both eyes)
            recess_len = recession_length(recess_muscle, PD)
            return {
                f"{recess_muscle}_recession_mm_each_eye": round(recess_len, 2),
                f"resection": "Not needed"
            }
        else:
            # Recession maxed bilaterally + resection on affected eye for doubled residual PD
            recess_len = MAX_RECESSION
            residual_PD = PD - max_recession_PD
            doubled_residual = residual_PD * 2
            resect_len = resection_length(resect_muscle, doubled_residual)
            return {
                f"{recess_muscle}_recession_mm_each_eye": recess_len,
                f"{resect_muscle}_resection_mm_affected_eye": round(resect_len, 2)
            }
    elif deviation_type.lower() in ['hypertropia', 'hypotropia']:
        # Vertical muscles: SR and IR in opposite eyes
        if deviation_type.lower() == 'hypertropia':
            recess_muscle_1 = 'sr'  # affected eye recession
            recess_muscle_2 = 'ir'  # opposite eye recession
        else:
            recess_muscle_1 = 'ir'  # affected eye recession
            recess_muscle_2 = 'sr'  # opposite eye recession

        # Calculate recessions individually (vertical deviations do not require resection in bilateral)
        recess_len_1 = recession_length(recess_muscle_1, PD)
        recess_len_2 = recession_length(recess_muscle_2, PD)

        # Check if either muscle recession exceeds max length
        if recess_len_1 >= MAX_RECESSION or recess_len_2 >= MAX_RECESSION:
            return {"error": "Bilateral recession not feasible for this PD due to muscle length limits."}

        return {
            f"{recess_muscle_1}_recession_mm_affected_eye": round(recess_len_1, 2),
            f"{recess_muscle_2}_recession_mm_opposite_eye": round(recess_len_2, 2),
            "resection": "Not needed"
        }
    else:
        raise ValueError("Unsupported deviation type for bilateral approach")
