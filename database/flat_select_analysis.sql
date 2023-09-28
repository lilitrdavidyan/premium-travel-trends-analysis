SELECT 
    t.id as tour_id,
    t.name as tour_name,
    COUNT(DISTINCT tour_option.id) as number_of_tourOptions,
    AVG(lv.latitude) as mean_lat,
    AVG(lv.longitude) as mean_long,
    COUNT(DISTINCT lv.countryCode) as number_of_unique_countries,
    GROUP_CONCAT(DISTINCT lv.countryCode ORDER BY lv.countryCode ASC SEPARATOR ', ') as country_codes,
    COUNT(DISTINCT lv.id) as number_of_locations_visited,
    MIN(o.fullPrice) as full_price_min,
    MAX(o.fullPrice) as full_price_max,
    MIN(d.startDate) as earliest_start_date,
    MAX(d.endDate) as last_end_date,
    CONCAT('https://luxuryescapes.com/de/tour/', t.id) as tour_link,
    MAX(CASE WHEN MONTH(d.startDate) = 1 OR MONTH(d.endDate) = 1 THEN 1 ELSE 0 END) as Jan,
    MAX(CASE WHEN MONTH(d.startDate) = 2 OR MONTH(d.endDate) = 2 THEN 1 ELSE 0 END) as Feb,
    MAX(CASE WHEN MONTH(d.startDate) = 3 OR MONTH(d.endDate) = 3 THEN 1 ELSE 0 END) as Mar,
    MAX(CASE WHEN MONTH(d.startDate) = 4 OR MONTH(d.endDate) = 4 THEN 1 ELSE 0 END) as Apr,
    MAX(CASE WHEN MONTH(d.startDate) = 5 OR MONTH(d.endDate) = 5 THEN 1 ELSE 0 END) as May,
    MAX(CASE WHEN MONTH(d.startDate) = 6 OR MONTH(d.endDate) = 6 THEN 1 ELSE 0 END) as Jun,
    MAX(CASE WHEN MONTH(d.startDate) = 7 OR MONTH(d.endDate) = 7 THEN 1 ELSE 0 END) as Jul,
    MAX(CASE WHEN MONTH(d.startDate) = 8 OR MONTH(d.endDate) = 8 THEN 1 ELSE 0 END) as Aug,
    MAX(CASE WHEN MONTH(d.startDate) = 9 OR MONTH(d.endDate) = 9 THEN 1 ELSE 0 END) as Sep,
    MAX(CASE WHEN MONTH(d.startDate) = 10 OR MONTH(d.endDate) = 10 THEN 1 ELSE 0 END) as Oct,
    MAX(CASE WHEN MONTH(d.startDate) = 11 OR MONTH(d.endDate) = 11 THEN 1 ELSE 0 END) as Nov,
    MAX(CASE WHEN MONTH(d.startDate) = 12 OR MONTH(d.endDate) = 12 THEN 1 ELSE 0 END) as Dece
FROM 
    tours t
LEFT JOIN 
    tour_options tour_option ON t.id = tour_option.tour_id
LEFT JOIN 
    locations_visited lv ON t.id = lv.tour_id
LEFT JOIN 
    options o ON t.id = o.tour_id
LEFT JOIN 
    departures d ON tour_option.id = d.fkTourOptionId
GROUP BY 
    t.id
