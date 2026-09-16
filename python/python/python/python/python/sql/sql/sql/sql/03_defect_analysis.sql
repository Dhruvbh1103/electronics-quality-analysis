-- Defect Type Distribution

SELECT
    defect_type,
    COUNT(*) AS defect_count,
    ROUND(
        100.0 * COUNT(*) /
        SUM(COUNT(*)) OVER (),
        2
    ) AS percentage_of_defects
FROM manufacturing_quality
WHERE defect = 1
GROUP BY defect_type
ORDER BY defect_count DESC;


-- Temperature Band Analysis

SELECT
    CASE
        WHEN temperature < 25 THEN 'Below 25'
        WHEN temperature < 30 THEN '25-30'
        WHEN temperature < 35 THEN '30-35'
        ELSE '35+'
    END AS temperature_band,

    COUNT(*) AS total_units,

    SUM(defect) AS defective_units,

    ROUND(
        100.0 * SUM(defect) / COUNT(*),
        2
    ) AS defect_rate

FROM manufacturing_quality

GROUP BY
    CASE
        WHEN temperature < 25 THEN 'Below 25'
        WHEN temperature < 30 THEN '25-30'
        WHEN temperature < 35 THEN '30-35'
        ELSE '35+'
    END

ORDER BY defect_rate DESC;


-- Inspection Score Analysis

SELECT
    CASE
        WHEN inspection_score < 70 THEN 'Below 70'
        WHEN inspection_score < 80 THEN '70-80'
        WHEN inspection_score < 90 THEN '80-90'
        ELSE '90+'
    END AS inspection_band,

    COUNT(*) AS total_units,

    SUM(defect) AS defective_units,

    ROUND(
        100.0 * SUM(defect) / COUNT(*),
        2
    ) AS defect_rate

FROM manufacturing_quality

GROUP BY
    CASE
        WHEN inspection_score < 70 THEN 'Below 70'
        WHEN inspection_score < 80 THEN '70-80'
        WHEN inspection_score < 90 THEN '80-90'
        ELSE '90+'
    END

ORDER BY defect_rate DESC;
