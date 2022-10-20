select
	c.label plate_label,
	s.label sample_label,
	pd.raw_data_json,
	epd.*,
	coalesce(a.output->>'I.A_ave', '0')::numeric fom
from
	sample s
join sample_process sp on
	sp.sample_id = s.id
join sample_process_process_data sppd on
	sppd.sample_process_id = sp.id
join process_data pd on
	sppd.process_data_id = pd.id
join process_data_analysis pda on
	pda.process_data_id = pd.id
join analysis a on
	pda.analysis_id = a.id
join collection_sample cs on
	cs.sample_id = s.id
join collection c on
	cs.collection_id = c.id
join process p on
	sp.process_id = p.id
join process_detail pdet on
	p.process_detail_id = pdet.id
join eche_process_detail epd on
	pdet.eche_process_detail_id = epd.id
where
	a.analysis_name = 'CA_FOMS_standard'
	and c.label in (
	select
		label
	from
		collection c2
	where
		c.type = 'JCAP_plate'
	limit 5)
