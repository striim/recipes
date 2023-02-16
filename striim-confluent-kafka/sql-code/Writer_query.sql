SELECT
TO_STRING(data.get("_id")) as id,
TO_STRING(data.get("name")) as name,
TO_STRING(data.get("property_type")) as property_type,
TO_STRING(data.get("room_type")) as room_type,
TO_STRING(data.get("bed_type")) as bed_type,
TO_STRING(data.get("minimum_nights")) as minimum_nights,
TO_STRING(data.get("cancellation_policy")) as cancellation_policy,
TO_STRING(data.get("accommodates")) as accommodates,
TO_STRING(data.get("bedrooms")) as no_of_bedrooms,
TO_STRING(data.get("beds")) as no_of_beds,
TO_STRING(data.get("number_of_reviews")) as no_of_reviews
FROM mongoOutputStream l;