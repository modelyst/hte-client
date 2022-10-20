select
	s.label,
	jsd.inkjet_comp,
	a."output"
from
	sample s
join sample_process sp on
	sp.sample_id = s.id
join sample_process_process_data sppd on
	sppd.sample_process_id = sp.id
join process_data pd on
	pd.id = sppd.process_data_id
join process_data_analysis pda on
	pda.process_data_id = pd.id
join analysis a on
	a.id = pda.analysis_id
join jcap_sample_details jsd on
	jsd.id = s.jcap_sample_details_id
where
	a.analysis_name = 'CP_FOMS_standard';
