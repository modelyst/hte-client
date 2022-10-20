select
	analysis_name,
	count(*)
from
	analysis a
group by
	analysis_name
order by
	count(*) desc
