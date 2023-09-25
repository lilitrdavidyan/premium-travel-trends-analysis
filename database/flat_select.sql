SELECT 
        t.id AS tour_id,
        t.productType,
        t.name AS tour_name,
        t.brand,
        t.activityLevel,
        t.reviewsRating,
        t.reviewsTotal,
        t.lowestOptionRoomType,
        t.lowestOptionPrice,
        t.lowestOptionFullPrice,
        t.fkSeasonId,

        o.id AS tour_option_id,
        o.tour_id,
        o.sourceTourOptionName,
        o.isPrivateRequest,
        o.maxPax,
        o.name AS tour_option_name,
        o.description,
        o.travelInclusions,
        o.diningInclusions,
        o.startLocationName,
        o.startLocationCountryCode,
        o.startLocationLongitude,
        o.startLocationLatitude,
        o.endLocationName,
        o.endLocationCountryCode,
        o.endLocationLongitude,
        o.endLocationLatitude,
        o.countries_visited,
        o.minChildPriceAge,
        o.maxChildPriceAge,
        i1.title AS day_1_title,
		 i1.description AS day_1_description,
		 i1.accommodation AS day_1_accommodation,
		 i1.meals AS day_1_meals,
		 i2.title AS day_2_title,
		 i2.description AS day_2_description,
		 i2.accommodation AS day_2_accommodation,
		 i2.meals AS day_2_meals,
		 i3.title AS day_3_title,
		 i3.description AS day_3_description,
		 i3.accommodation AS day_3_accommodation,
		 i3.meals AS day_3_meals,
		 i4.title AS day_4_title,
		 i4.description AS day_4_description,
		 i4.accommodation AS day_4_accommodation,
		 i4.meals AS day_4_meals,
		 i5.title AS day_5_title,
		 i5.description AS day_5_description,
		 i5.accommodation AS day_5_accommodation,
		 i5.meals AS day_5_meals,
		 i6.title AS day_6_title,
		 i6.description AS day_6_description,
		 i6.accommodation AS day_6_accommodation,
		 i6.meals AS day_6_meals,
		 i7.title AS day_7_title,
		 i7.description AS day_7_description,
		 i7.accommodation AS day_7_accommodation,
		 i7.meals AS day_7_meals,
		 i8.title AS day_8_title,
		 i8.description AS day_8_description,
		 i8.accommodation AS day_8_accommodation,
		 i8.meals AS day_8_meals,
		 i9.title AS day_9_title,
		 i9.description AS day_9_description,
		 i9.accommodation AS day_9_accommodation,
		 i9.meals AS day_9_meals,
		 i10.title AS day_10_title,
		 i10.description AS day_10_description,
		 i10.accommodation AS day_10_accommodation,
		 i10.meals AS day_10_meals,
		 i11.title AS day_11_title,
		 i11.description AS day_11_description,
		 i11.accommodation AS day_11_accommodation,
		 i11.meals AS day_11_meals,
		 i12.title AS day_12_title,
		 i12.description AS day_12_description,
		 i12.accommodation AS day_12_accommodation,
		 i12.meals AS day_12_meals,
		 i13.title AS day_13_title,
		 i13.description AS day_13_description,
		 i13.accommodation AS day_13_accommodation,
		 i13.meals AS day_13_meals,
		 i14.title AS day_14_title,
		 i14.description AS day_14_description,
		 i14.accommodation AS day_14_accommodation,
		 i14.meals AS day_14_meals,
		 i15.title AS day_15_title,
		 i15.description AS day_15_description,
		 i15.accommodation AS day_15_accommodation,
		 i15.meals AS day_15_meals,
		 i16.title AS day_16_title,
		 i16.description AS day_16_description,
		 i16.accommodation AS day_16_accommodation,
		 i16.meals AS day_16_meals,
		 i17.title AS day_17_title,
		 i17.description AS day_17_description,
		 i17.accommodation AS day_17_accommodation,
		 i17.meals AS day_17_meals,
		 i18.title AS day_18_title,
		 i18.description AS day_18_description,
		 i18.accommodation AS day_18_accommodation,
		 i18.meals AS day_18_meals,
		 i19.title AS day_19_title,
		 i19.description AS day_19_description,
		 i19.accommodation AS day_19_accommodation,
		 i19.meals AS day_19_meals,
		 i20.title AS day_20_title,
		 i20.description AS day_20_description,
		 i20.accommodation AS day_20_accommodation,
		 i20.meals AS day_20_meals,
		 i21.title AS day_21_title,
		 i21.description AS day_21_description,
		 i21.accommodation AS day_21_accommodation,
		 i21.meals AS day_21_meals,
		 i22.title AS day_22_title,
		 i22.description AS day_22_description,
		 i22.accommodation AS day_22_accommodation,
		 i22.meals AS day_22_meals,
		 i23.title AS day_23_title,
		 i23.description AS day_23_description,
		 i23.accommodation AS day_23_accommodation,
		 i23.meals AS day_23_meals,
		 i24.title AS day_24_title,
		 i24.description AS day_24_description,
		 i24.accommodation AS day_24_accommodation,
		 i24.meals AS day_24_meals,
		 i25.title AS day_25_title,
		 i25.description AS day_25_description,
		 i25.accommodation AS day_25_accommodation,
		 i25.meals AS day_25_meals,
		 i26.title AS day_26_title,
		 i26.description AS day_26_description,
		 i26.accommodation AS day_26_accommodation,
		 i26.meals AS day_26_meals,
		 i27.title AS day_27_title,
		 i27.description AS day_27_description,
		 i27.accommodation AS day_27_accommodation,
		 i27.meals AS day_27_meals,
		 i28.title AS day_28_title,
		 i28.description AS day_28_description,
		 i28.accommodation AS day_28_accommodation,
		 i28.meals AS day_28_meals
    FROM tours t
    INNER JOIN tour_options o ON t.id = o.tour_id
    
    LEFT JOIN itineraries i1 ON o.id = i1.tour_option_id AND i1.startDay = 1
 LEFT JOIN itineraries i2 ON o.id = i2.tour_option_id AND i2.startDay = 2
 LEFT JOIN itineraries i3 ON o.id = i3.tour_option_id AND i3.startDay = 3
 LEFT JOIN itineraries i4 ON o.id = i4.tour_option_id AND i4.startDay = 4
 LEFT JOIN itineraries i5 ON o.id = i5.tour_option_id AND i5.startDay = 5
 LEFT JOIN itineraries i6 ON o.id = i6.tour_option_id AND i6.startDay = 6
 LEFT JOIN itineraries i7 ON o.id = i7.tour_option_id AND i7.startDay = 7
 LEFT JOIN itineraries i8 ON o.id = i8.tour_option_id AND i8.startDay = 8
 LEFT JOIN itineraries i9 ON o.id = i9.tour_option_id AND i9.startDay = 9
 LEFT JOIN itineraries i10 ON o.id = i10.tour_option_id AND i10.startDay = 10
 LEFT JOIN itineraries i11 ON o.id = i11.tour_option_id AND i11.startDay = 11
 LEFT JOIN itineraries i12 ON o.id = i12.tour_option_id AND i12.startDay = 12
 LEFT JOIN itineraries i13 ON o.id = i13.tour_option_id AND i13.startDay = 13
 LEFT JOIN itineraries i14 ON o.id = i14.tour_option_id AND i14.startDay = 14
 LEFT JOIN itineraries i15 ON o.id = i15.tour_option_id AND i15.startDay = 15
 LEFT JOIN itineraries i16 ON o.id = i16.tour_option_id AND i16.startDay = 16
 LEFT JOIN itineraries i17 ON o.id = i17.tour_option_id AND i17.startDay = 17
 LEFT JOIN itineraries i18 ON o.id = i18.tour_option_id AND i18.startDay = 18
 LEFT JOIN itineraries i19 ON o.id = i19.tour_option_id AND i19.startDay = 19
 LEFT JOIN itineraries i20 ON o.id = i20.tour_option_id AND i20.startDay = 20
 LEFT JOIN itineraries i21 ON o.id = i21.tour_option_id AND i21.startDay = 21
 LEFT JOIN itineraries i22 ON o.id = i22.tour_option_id AND i22.startDay = 22
 LEFT JOIN itineraries i23 ON o.id = i23.tour_option_id AND i23.startDay = 23
 LEFT JOIN itineraries i24 ON o.id = i24.tour_option_id AND i24.startDay = 24
 LEFT JOIN itineraries i25 ON o.id = i25.tour_option_id AND i25.startDay = 25
 LEFT JOIN itineraries i26 ON o.id = i26.tour_option_id AND i26.startDay = 26
 LEFT JOIN itineraries i27 ON o.id = i27.tour_option_id AND i27.startDay = 27
 LEFT JOIN itineraries i28 ON o.id = i28.tour_option_id AND i28.startDay = 28

;