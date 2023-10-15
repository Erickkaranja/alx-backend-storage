-- Add a computed column to store the first letter of the name
ALTER TABLE names
ADD COLUMN first_letter CHAR(1) AS (LEFT(name, 1));

-- Create an index on the computed first_letter column
CREATE INDEX idx_name_first ON names (first_letter);
