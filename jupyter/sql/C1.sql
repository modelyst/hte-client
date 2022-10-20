select
	ad.id,
	ad.analysis_name,
	count(*)
from
	analysis a
join analysis_detail ad on
	a.analysis_detail_id = ad.id
group by
	ad.id,
	ad.analysis_name
having
	count(*) > 1
order by
	count(*) desc
