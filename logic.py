import pandas as pd

def get_recommendation(strabismus_type, deviation, approach, nomogram_df):
    recommendations = []

    def limit_correction(value):
        """Return (primary, contralateral) values based on 12 mm cap."""
        if value <= 12:
            return round(value, 1), 0.0
        else:
            return 12.0, round(value - 12, 1)

    if strabismus_type in ['Esotropia', 'Exotropia']:
        horizontal = True
        vertical = False
    elif strabismus_type in ['Hypertropia', 'Hypotropia']:
        vertical = True
        horizontal = False
    else:
        return ["Unknown strabismus type."]

    if horizontal:
        if strabismus_type == 'Esotropia':
            rec_mr = round((deviation / 5) * 1.0, 1)  # MR recession 1mm per 5 PD
            res_lr = round((deviation / 5) * 0.5, 1)  # LR resection 0.5mm per 5 PD

            if approach == 'Unilateral':
                mr_primary, mr_contra = limit_correction(rec_mr)
                lr_primary = res_lr

                if mr_contra > 0:
                    recommendations.append(f"Right Medial Rectus recession: {mr_primary} mm")
                    recommendations.append(f"Right Lateral Rectus resection: {lr_primary} mm")
                    recommendations.append(f"Left Medial Rectus recession: {mr_contra} mm")
                else:
                    recommendations.append(f"Medial Rectus recession: {mr_primary} mm")
                    recommendations.append(f"Lateral Rectus resection: {lr_primary} mm")

            elif approach == 'Bilateral':
                rec_mr_each = rec_mr / 2
                mr_primary, mr_contra = limit_correction(rec_mr_each)

                recommendations.append(f"Right Medial Rectus recession: {mr_primary} mm")
                recommendations.append(f"Left Medial Rectus recession: {mr_primary + mr_contra} mm" if mr_contra else f"Left Medial Rectus recession: {mr_primary} mm")

        elif strabismus_type == 'Exotropia':
            rec_lr = round((deviation / 5) * 1.0, 1)  # LR recession 1mm per 5 PD
            res_mr = round((deviation / 5) * 0.5, 1)  # MR resection 0.5mm per 5 PD

            if approach == 'Unilateral':
                lr_primary, lr_contra = limit_correction(rec_lr)
                mr_primary = res_mr

                if lr_contra > 0:
                    recommendations.append(f"Right Lateral Rectus recession: {lr_primary} mm")
                    recommendations.append(f"Right Medial Rectus resection: {mr_primary} mm")
                    recommendations.append(f"Left Lateral Rectus recession: {lr_contra} mm")
                else:
                    recommendations.append(f"Lateral Rectus recession: {lr_primary} mm")
                    recommendations.append(f"Medial Rectus resection: {mr_primary} mm")

            elif approach == 'Bilateral':
                rec_lr_each = rec_lr / 2
                lr_primary, lr_contra = limit_correction(rec_lr_each)

                recommendations.append(f"Right Lateral Rectus recession: {lr_primary} mm")
                recommendations.append(f"Left Lateral Rectus recession: {lr_primary + lr_contra} mm" if lr_contra else f"Left Lateral Rectus recession: {lr_primary} mm")

    if vertical:
        rec_value = round((deviation / 5) * 1.0, 1)
        res_value = round((deviation / 5) * 0.5, 1)

        if strabismus_type == 'Hypertropia':
            if approach == 'Unilateral':
                recommendations.append(f"Superior Rectus recession: {rec_value} mm")
                recommendations.append(f"Inferior Rectus resection: {res_value} mm")
            elif approach == 'Bilateral':
                rec_half, rec_contra = limit_correction(rec_value / 2)
                recommendations.append(f"Superior Rectus recession (Right Eye): {rec_half} mm")
                recommendations.append(f"Inferior Rectus recession (Left Eye): {rec_half + rec_contra} mm" if rec_contra else f"Inferior Rectus recession (Left Eye): {rec_half} mm")

        elif strabismus_type == 'Hypotropia':
            if approach == 'Unilateral':
                recommendations.append(f"Inferior Rectus recession: {rec_value} mm")
                recommendations.append(f"Superior Rectus resection: {res_value} mm")
            elif approach == 'Bilateral':
                rec_half, rec_contra = limit_correction(rec_value / 2)
                recommendations.append(f"Inferior Rectus recession (Right Eye): {rec_half} mm")
                recommendations.append(f"Superior Rectus recession (Left Eye): {rec_half + rec_contra} mm" if rec_contra else f"Superior Rectus recession (Left Eye): {rec_half} mm")

    # Filter out 0 mm entries
    filtered = [r for r in recommendations if "0.0 mm" not in r]
    return filtered
