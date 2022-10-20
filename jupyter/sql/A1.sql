select
	collection.type,
	collection.label,
	count(*)
from
	collection
join collection_sample on
	collection_sample.collection_id = collection.id
group by
	collection.type,
	collection.label
order by
	count(*) desc;
