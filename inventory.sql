CREATE OR REPLACE TABLE inventory_daily (
    location STRING,
    item STRING,
    opening_stock INT,
    received INT,
    issued INT,
    closing_stock INT,
    lead_time_days INT
);

-- Insert sample data
INSERT INTO inventory_daily VALUES
('City Hospital', 'Paracetamol', 500, 100, 120, 480, 5),
('City Hospital', 'Antibiotics', 300, 50, 90, 260, 7),
('District Clinic', 'Paracetamol', 200, 40, 80, 160, 5),
('District Clinic', 'Insulin', 150, 20, 60, 110, 4),
('Rural Health Center', 'Paracetamol', 100, 10, 50, 60, 6),
('Rural Health Center', 'Insulin', 80, 10, 40, 50, 5);

-- Create view for risk analysis
CREATE OR REPLACE VIEW inventory_risk_view AS
SELECT
    location,
    item,
    closing_stock,
    lead_time_days,
    issued AS daily_usage,
    
    CASE
        WHEN closing_stock <= issued * lead_time_days THEN 'CRITICAL'
        WHEN closing_stock <= issued * (lead_time_days * 2) THEN 'LOW'
        ELSE 'SAFE'
    END AS risk_level,
    
    (issued * (lead_time_days * 2)) AS suggested_reorder_qty
FROM inventory_daily;
