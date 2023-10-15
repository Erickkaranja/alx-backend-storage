DELIMITER //

-- Create a stored procedure to compute and store the average score for a user
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE average DECIMAL(10, 2);
    
    -- Compute the average score for the user
    SELECT AVG(score) INTO average
    FROM scores
    WHERE user_id = user_id;

    -- Update the user's average score in the users table
    UPDATE users
    SET average_score = average
    WHERE id = user_id;
END;
//
DELIMITER ;

