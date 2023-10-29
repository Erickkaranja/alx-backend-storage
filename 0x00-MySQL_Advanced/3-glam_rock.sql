-- script that lists all bands with glam_rock as their main style.
SELECT band_name,
       CASE
          WHEN split IS NULL THEN 2022 - formed
          ELSE split - formed
       END AS lifespan
FROM metal_bands
WHERE style LIKE '%glam_rock%'
ORDER BY lifespan DESC;
