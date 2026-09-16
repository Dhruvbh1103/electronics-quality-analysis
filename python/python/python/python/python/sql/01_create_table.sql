CREATE TABLE manufacturing_quality (
    Unit_ID VARCHAR(50),
    Production_Date DATE,
    Production_Line VARCHAR(50),
    Component_Type VARCHAR(50),
    Temperature DECIMAL(10,2),
    Humidity DECIMAL(10,2),
    Voltage DECIMAL(10,2),
    Current DECIMAL(10,2),
    Machine_Age INT,
    Inspection_Score DECIMAL(10,2),
    Shift VARCHAR(30),
    Defect_Type VARCHAR(50),
    Defect INT,
    Downtime DECIMAL(10,2)
);
