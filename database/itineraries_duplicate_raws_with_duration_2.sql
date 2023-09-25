SELECT * from itineraries where duration = 2;

INSERT INTO itineraries (tour_id, tour_option_id, title, description, startDay, duration, accommodation, meals, created_at, updated_at)
SELECT tour_id, tour_option_id, title, description, startDay + 1, duration, accommodation, meals, NOW(), NOW()
FROM itineraries
WHERE duration = 2;
