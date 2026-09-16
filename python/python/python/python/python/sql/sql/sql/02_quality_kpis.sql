-- Overall Quality KPIs

SELECT
    COUNT(*) AS total_units,
    SUM(defect) AS defective_units,
    ROUND(
        100.0 * SUM(defect) / COUNT(*),
        2
    ) AS defect_rate,
    ROUND(
        AVG(inspection_score),
        2
    ) AS average_inspection_score,
    ROUND(
        SUM(downtime),
        2
    ) AS total_downtime
FROM manufacturing_quality;


-- Defect Rate by Production Line

SELECT
    production_line,
    COUNT(*) AS total_units,
    SUM(defect) AS defective_units,
    ROUND(
        100.0 * SUM(defect) / COUNT(*),
        2
    ) AS defect_rate
FROM manufacturing_quality
GROUP BY production_line
ORDER BY defect_rate DESC;


-- Defect Rate by Component

SELECT
    component_type,
    COUNT(*) AS total_units,
    SUM(defect) AS defective_units,
    ROUND(
        100.0 * SUM(defect) / COUNT(*),
        2
    ) AS defect_rate
FROM manufacturing_quality
GROUP BY component_type
ORDER BY defect_rate DESC;


-- Defect Rate by Shift

SELECT
    shift,
    COUNT(*) AS total_units,
    SUM(defect) AS defective_units,
    ROUND(
        100.0 * SUM(defect) / COUNT(*),
        2
    ) AS defect_rate
FROM manufacturing_quality
GROUP BY shift
ORDER BY defect_rate DESC;
