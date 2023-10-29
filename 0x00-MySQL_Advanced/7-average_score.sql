-- creates a stored procedure ComputeAverageScoreForUser.

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_corrections INT;
    DECLARE avg_score FLOAT;

    -- Calculate the total score and the total number of corrections for the user
    SELECT SUM(score), COUNT(*) 
    INTO total_score, total_corrections
    FROM corrections
    WHERE user_id = user_id;

    -- Calculate the average score (handle division by zero)
    IF total_corrections > 0 THEN
        SET avg_score = total_score / total_corrections;
    ELSE
        SET avg_score = 0;
    END IF;

    -- Update the user's average score in the users table
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END $$

DELIMITER ;
