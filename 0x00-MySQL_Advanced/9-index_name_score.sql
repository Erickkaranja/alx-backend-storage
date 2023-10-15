-- Add a computed column to store the first letter of the name
CREATE INDEX idx_name_first_score ON names (first_letter, score);
