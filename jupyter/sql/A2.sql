select
	count(*)
from
	(
	select
		count(*)
	from
		collection_sample
	group by
		collection_sample.sample_id
	having
		count(*) > 1) as temp;
