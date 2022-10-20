select
	pd.raw_data_json,
	coalesce(a.output->>'I.A_ave', '0')::numeric fom
from
    process_data pd
join process_data_analysis pda on
	pda.process_data_id = pd.id
join analysis a on
	pda.analysis_id = a.id
where
	a.analysis_name = 'CA_FOMS_standard'
