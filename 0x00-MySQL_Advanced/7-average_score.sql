-- creates a stored procedure ComputeAverageScoreForUser.

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_corrections INT;
    DECLARE avg_score FLOAT;

    SELECT SUM(score), COUNT(*) 
    INTO total_score, total_corrections
    FROM corrections
    WHERE user_id = user_id;

    IF total_corrections > 0 THEN
        SET avg_score = total_score / total_corrections;
    ELSE
        SET avg_score = 0;
    END IF;

    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END $$

DELIMITER ;
