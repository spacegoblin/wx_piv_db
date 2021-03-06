/*

DROP VIEW public.qry_crm;
DROP VIEW public.qry_susa_fcst_c;
DROP VIEW public.qry_susa_fcst;
DROP VIEW public.qry_susa_plan;
DROP VIEW public.qry_susa;


*/

/* Base view for the SUSA */

CREATE OR REPLACE VIEW public.qry_susa (
    id,
    account_datev,
    hgb_acc_sort_code,
    soll,
    haben,
    period,
    name_datev,
    zuordnung_bwa,
    bwa_titel,
    accounts_ssc,
    acc_description_ssc,
    amount,
    year,
    gegenkonto,
    buchungstext,
    comment,
    comment_2,
    kost1,
    project_code,
    z_type,
    base_table,
    company,
    foreign_amount,
    customer,
    internal_ext,
    business_unit,
    p_description,
    datum,
    partner_name,
    
    stapel_nr,
    belegfeld1,
    
    kontobezeichnung_not_mdata,
    cf_acc_sort_code,
    i_comp,
    ssc_cost_centre,
    cc_ssc_function,
    p_mgr,
    rpt_acc_sort_code,
    pers_code,
    first_name,
    last_name,
    cf_direct)
AS
SELECT tbl_susa.id, 
	tbl_susa.account_datev,
    tbl_chart_of_accounts.hgb_acc_sort_code, 
    tbl_susa.soll, 
    tbl_susa.haben, tbl_susa.period, tbl_chart_of_accounts.name_datev, tbl_chart_of_accounts.zuordnung_bwa, 
    tbl_chart_of_accounts.bwa_titel, tbl_chart_of_accounts.accounts_ssc, tbl_chart_of_accounts.acc_description_ssc, 
    tbl_susa.soll - tbl_susa.haben AS amount, "left"(tbl_susa.period::text, 4) AS year, tbl_susa.gegenkonto, 
    tbl_susa.buchungstext, tbl_susa.comment, tbl_susa.comment_2, tbl_susa.kost1, tbl_cost_centers.project_code::text AS project_code, 'Actual'::text AS z_type, 
    'tbl_susa'::text AS base_table, tbl_susa.company, tbl_susa.foreign_amount, tbl_cost_centers.customer, tbl_cost_centers.internal_ext, tbl_cost_centers.business_unit, 
    tbl_cost_centers.description AS p_description, tbl_susa.datum, 
    
    partner_int_ext_v02(tbl_susa.gegenkonto)::text AS partner_name, 
     
    
    tbl_susa.stapel_nr, 
    tbl_susa.belegfeld1, 
    tbl_susa.kontobezeichnung_not_mdata,
    tbl_chart_of_accounts.cf_acc_sort_code, 
    tbl_chart_of_accounts.i_comp, tbl_chart_of_accounts.ssc_cost_centre, 
    tbl_cost_centers.cc_ssc_function, tbl_cost_centers.p_mgr::text AS p_mgr, tbl_chart_of_accounts.rpt_acc_sort_code, 
    tbl_susa.pers_code, tbl_person_stand.first_name, tbl_person_stand.last_name,
    tbl_susa.cf_direct
FROM tbl_susa
   LEFT JOIN tbl_chart_of_accounts ON tbl_susa.account_datev::text =
       tbl_chart_of_accounts.account_datev::text
   LEFT JOIN tbl_cost_centers ON tbl_susa.kost1::text =
       tbl_cost_centers.costcenternr::text
   LEFT JOIN tbl_person_stand ON tbl_susa.pers_code::text = tbl_person_stand.code::text;

GRANT SELECT ON public.qry_susa TO db_read;
  


/* View for the plan */

CREATE OR REPLACE VIEW public.qry_susa_plan (
    id,
    account_datev,
    hgb_acc_sort_code,
    soll,
    haben,
    period,
    name_datev,
    zuordnung_bwa,
    bwa_titel,
    accounts_ssc,
    acc_description_ssc,
    amount,
    year,
    gegenkonto,
    buchungstext,
    comment,
    comment_2,
    kost1,
    project_code,
    z_type,
    base_table,
    company,
    foreign_amount,
    customer,
    internal_ext,
    business_unit,
    p_description,
    datum,
    partner_name,
    
    stapel_nr,
    belegfeld1,
    
    kontobezeichnung_not_mdata,
    cf_acc_sort_code,
    i_comp,
    ssc_cost_centre,
    cc_ssc_function,
    p_mgr,
    rpt_acc_sort_code,
    pers_code,
    first_name,
    last_name,
    cf_direct
    )
AS
SELECT tbl_susa_plan.id, 
	tbl_susa_plan.account_datev,
    tbl_chart_of_accounts.hgb_acc_sort_code,
    tbl_susa_plan.soll, 
    tbl_susa_plan.haben, tbl_susa_plan.period, tbl_chart_of_accounts.name_datev, 
    tbl_chart_of_accounts.zuordnung_bwa, tbl_chart_of_accounts.bwa_titel, 
    tbl_chart_of_accounts.accounts_ssc, 
    tbl_chart_of_accounts.acc_description_ssc, tbl_susa_plan.soll - tbl_susa_plan.haben AS amount, "left"(tbl_susa_plan.period::text, 4) AS year, 
    tbl_susa_plan.gegenkonto, tbl_susa_plan.buchungstext, tbl_susa_plan.comment, tbl_susa_plan.comment_2, ''::character varying(255) AS kost1, 
    tbl_susa_plan.project_code, tbl_susa_plan.z_type, 'tbl_susa_plan'::text AS base_table, tbl_susa_plan.company, tbl_susa_plan.foreign_amount, 
    tbl_cost_centers.customer, tbl_cost_centers.internal_ext, tbl_cost_centers.business_unit, tbl_cost_centers.description AS p_description, NULL::date AS datum, 
    
    partner_int_ext_v02(tbl_susa_plan.gegenkonto)::text AS partner_name, 
    
    tbl_susa_plan.stapel_nr, ''::character varying(255) AS belegfeld1,
    
    tbl_susa_plan.kontobezeichnung_not_mdata, 
    tbl_chart_of_accounts.cf_acc_sort_code,
    tbl_chart_of_accounts.i_comp,
    tbl_chart_of_accounts.ssc_cost_centre::text,
    tbl_cost_centers.cc_ssc_function::text,
    tbl_cost_centers.p_mgr::text,
    tbl_chart_of_accounts.rpt_acc_sort_code,
    tbl_susa_plan.pers_code, tbl_person_stand.first_name, 
    tbl_person_stand.last_name,
    tbl_susa_plan.cf_direct
FROM tbl_susa_plan
   LEFT JOIN tbl_chart_of_accounts ON tbl_susa_plan.account_datev::text =
       tbl_chart_of_accounts.account_datev::text
   LEFT JOIN tbl_cost_centers ON tbl_susa_plan.project_code::text =
       tbl_cost_centers.project_code::text
   LEFT JOIN tbl_person_stand ON tbl_susa_plan.pers_code::text = tbl_person_stand.code::text;

GRANT SELECT ON public.qry_susa_plan TO db_read;
    



       
/* View for the forecast  */


CREATE OR REPLACE VIEW public.qry_susa_fcst (
    id,
    account_datev,
    hgb_acc_sort_code,
    soll,
    haben,
    period,
    name_datev,
    zuordnung_bwa,
    bwa_titel,
    accounts_ssc,
    acc_description_ssc,
    amount,
    year,
    gegenkonto,
    buchungstext,
    comment,
    comment_2,
    kost1,
    project_code,
    z_type,
    base_table,
    company,
    foreign_amount,
    customer,
    internal_ext,
    business_unit,
    p_description,
    datum,
    partner_name,
    
    stapel_nr,
    belegfeld1,
    
    kontobezeichnung_not_mdata,
    cf_acc_sort_code,
    i_comp,
    ssc_cost_centre,
    cc_ssc_function,
    p_mgr,
    rpt_acc_sort_code,
    pers_code,
    first_name,
    last_name,
    cf_direct
    )
    
AS
SELECT qry_susa.id, 
	qry_susa.account_datev,
    qry_susa.hgb_acc_sort_code,
    qry_susa.soll, 
    qry_susa.haben, qry_susa.period, qry_susa.name_datev, qry_susa.zuordnung_bwa, 
    qry_susa.bwa_titel,  
    qry_susa.accounts_ssc, qry_susa.acc_description_ssc, 
    qry_susa.amount, qry_susa.year, qry_susa.gegenkonto, qry_susa.buchungstext, 
    qry_susa.comment, qry_susa.comment_2, qry_susa.kost1, qry_susa.project_code, qry_susa.z_type, 
    'tbl_susa' as base_table, 
    qry_susa.company, qry_susa.foreign_amount, 
    qry_susa.customer, qry_susa.internal_ext, qry_susa.business_unit, qry_susa.p_description, qry_susa.datum, qry_susa.partner_name, 
    
     
    qry_susa.stapel_nr, 
    qry_susa.belegfeld1,
    
    qry_susa.kontobezeichnung_not_mdata,
    qry_susa.cf_acc_sort_code,
    qry_susa.i_comp,
    qry_susa.ssc_cost_centre,
    qry_susa.cc_ssc_function,
    qry_susa.p_mgr,
    qry_susa.rpt_acc_sort_code,
    qry_susa.pers_code,
    qry_susa.first_name,
    qry_susa.last_name,
    qry_susa.cf_direct
    
FROM qry_susa
UNION
SELECT qry_susa_plan.id, 
	qry_susa_plan.account_datev,
    qry_susa_plan.hgb_acc_sort_code,
    qry_susa_plan.soll, qry_susa_plan.haben, qry_susa_plan.period, qry_susa_plan.name_datev, qry_susa_plan.zuordnung_bwa, 
    qry_susa_plan.bwa_titel,  
    qry_susa_plan.accounts_ssc, qry_susa_plan.acc_description_ssc, qry_susa_plan.amount, qry_susa_plan.year, qry_susa_plan.gegenkonto, 
    qry_susa_plan.buchungstext, qry_susa_plan.comment, qry_susa_plan.comment_2, qry_susa_plan.kost1, qry_susa_plan.project_code, qry_susa_plan.z_type, qry_susa_plan.base_table, 
    qry_susa_plan.company, qry_susa_plan.foreign_amount, qry_susa_plan.customer, qry_susa_plan.internal_ext, qry_susa_plan.business_unit, qry_susa_plan.p_description, 
    qry_susa_plan.datum, qry_susa_plan.partner_name, 
     
    qry_susa_plan.stapel_nr, 
    qry_susa_plan.belegfeld1,
    
    qry_susa_plan.kontobezeichnung_not_mdata, 
    qry_susa_plan.cf_acc_sort_code,
    qry_susa_plan.i_comp,
    qry_susa_plan.ssc_cost_centre,
    qry_susa_plan.cc_ssc_function,
    qry_susa_plan.p_mgr,
    qry_susa_plan.rpt_acc_sort_code,
    qry_susa_plan.pers_code,
    qry_susa_plan.first_name,
    qry_susa_plan.last_name,
    qry_susa_plan.cf_direct
        
FROM qry_susa_plan
WHERE qry_susa_plan.period >= 201312 AND (qry_susa_plan.z_type::text =
    'P_14_02'::text 
    OR qry_susa_plan.z_type::text = 'FC_13'::text
    OR qry_susa_plan.z_type::text = 'FC_F14v1'::text
    OR qry_susa_plan.z_type::text = 'PB_15v1'::text
    );

GRANT SELECT ON public.qry_susa_fcst TO db_read;


/* View for the union plan actuals */
/* ***************** NOT NEEDED
CREATE OR REPLACE VIEW public.qry_susa_union (
    id,
    account_datev,
    hgb_acc_sort_code,
    soll,
    haben,
    period,
    name_datev,
    zuordnung_bwa,
    bwa_titel,
    accounts_ssc,
    acc_description_ssc,
    amount,
    year,
    gegenkonto,
    buchungstext,
    comment,
    comment_2,
    kost1,
    project_code,
    z_type,
    base_table,
    company,
    foreign_amount,
    customer,
    internal_ext,
    business_unit,
    p_description,
    datum,
    partner_name,
    
    stapel_nr,
    belegfeld1,
    
    kontobezeichnung_not_mdata,
    cf_acc_sort_code,
    i_comp,
    ssc_cost_centre,
    cc_ssc_function,
    p_mgr,
    rpt_acc_sort_code,
    pers_code,
    first_name,
    last_name
    )
AS
SELECT qry_susa.id, qry_susa.account_datev,
    qry_susa.hgb_acc_sort_code,
    qry_susa.soll, 
    qry_susa.haben, qry_susa.period, qry_susa.name_datev, qry_susa.zuordnung_bwa, qry_susa.bwa_titel, 
    qry_susa.accounts_ssc, qry_susa.acc_description_ssc, qry_susa.amount, qry_susa.year, qry_susa.gegenkonto, 
    qry_susa.buchungstext, qry_susa.comment, qry_susa.comment_2, qry_susa.kost1, qry_susa.project_code, qry_susa.z_type, qry_susa.base_table, 
    qry_susa.company, qry_susa.foreign_amount, qry_susa.customer, qry_susa.internal_ext, qry_susa.business_unit, qry_susa.p_description, 
    qry_susa.datum, 
    qry_susa.partner_name, 
    
    qry_susa.stapel_nr, 
    qry_susa.belegfeld1,
    qry_susa.kontobezeichnung_not_mdata, 
    
    qry_susa.cf_acc_sort_code,
    qry_susa.i_comp,
    qry_susa.ssc_cost_centre,
    qry_susa.cc_ssc_function,
    qry_susa.p_mgr,
    qry_susa.rpt_acc_sort_code,
    qry_susa.pers_code,
    qry_susa.first_name,
    qry_susa.last_name
    
FROM qry_susa
UNION
SELECT qry_susa_plan.id, 
	qry_susa_plan.account_datev,
    qry_susa_plan.hgb_acc_sort_code,
    qry_susa_plan.soll, qry_susa_plan.haben, qry_susa_plan.period, qry_susa_plan.name_datev, 
    qry_susa_plan.zuordnung_bwa, qry_susa_plan.bwa_titel, 
    qry_susa_plan.accounts_ssc, qry_susa_plan.acc_description_ssc, qry_susa_plan.amount, qry_susa_plan.year, 
    qry_susa_plan.gegenkonto, qry_susa_plan.buchungstext, qry_susa_plan.comment, qry_susa_plan.comment_2, qry_susa_plan.kost1, qry_susa_plan.project_code, 
    qry_susa_plan.z_type, qry_susa_plan.base_table, qry_susa_plan.company, qry_susa_plan.foreign_amount, qry_susa_plan.customer, qry_susa_plan.internal_ext, 
    qry_susa_plan.business_unit, qry_susa_plan.p_description, qry_susa_plan.datum, 
    qry_susa_plan.partner_name, 
     
    qry_susa_plan.stapel_nr, 
    qry_susa_plan.belegfeld1,
    
    qry_susa_plan.kontobezeichnung_not_mdata, 
    qry_susa_plan.cf_acc_sort_code,
    qry_susa_plan.i_comp,
    qry_susa_plan.ssc_cost_centre,
    qry_susa_plan.cc_ssc_function,
    qry_susa_plan.p_mgr,
    qry_susa_plan.rpt_acc_sort_code,
    qry_susa_plan.pers_code,
    qry_susa_plan.first_name,
    qry_susa_plan.last_name
        
FROM qry_susa_plan;

GRANT SELECT ON public.qry_susa_union TO db_read;

****************************/

/* View for the qry_susa_fcst_c */

CREATE OR REPLACE VIEW public.qry_susa_fcst_c (
    id,
    account_datev,
    hgb_acc_sort_code,
    soll,
    haben,
    period,
    name_datev,
    zuordnung_bwa,
    bwa_titel,
    accounts_ssc,
    acc_description_ssc,
    amount,
    year,
    
    buchungstext,
    comment,
    comment_2,
    kost1,
    project_code,
    z_type,
    base_table,
    company,
    foreign_amount,
    customer,
    internal_ext,
    business_unit,
    p_description,
    datum,
    gegenkonto,
    partner_name,
    
    stapel_nr,
    belegfeld1,
    kontobezeichnung_not_mdata,
    cf_acc_sort_code,
    i_comp,
    costfunc_choice,

    p_mgr,
    rpt_acc_sort_code,
    pers_code,
    first_name,
    last_name,
    fcst_choice,
    company_grouped,
    cf_direct,
    ksek,
    ksekfix)
AS
SELECT qry_susa_fcst.id,
    qry_susa_fcst.account_datev,
    qry_susa_fcst.hgb_acc_sort_code,
    qry_susa_fcst.soll,
    qry_susa_fcst.haben,
    qry_susa_fcst.period,
    qry_susa_fcst.name_datev,
    qry_susa_fcst.zuordnung_bwa,
    qry_susa_fcst.bwa_titel,
    qry_susa_fcst.accounts_ssc,
    qry_susa_fcst.acc_description_ssc,
    qry_susa_fcst.amount,
    qry_susa_fcst.year,
    
    qry_susa_fcst.buchungstext,
    qry_susa_fcst.comment,
    qry_susa_fcst.comment_2,
    qry_susa_fcst.kost1,
    qry_susa_fcst.project_code,
    qry_susa_fcst.z_type,
    qry_susa_fcst.base_table,
    qry_susa_fcst.company,
    qry_susa_fcst.foreign_amount,
    qry_susa_fcst.customer,
    qry_susa_fcst.internal_ext,
    qry_susa_fcst.business_unit,
    qry_susa_fcst.p_description,
    qry_susa_fcst.datum,
    qry_susa_fcst.gegenkonto,
    qry_susa_fcst.partner_name,
    
    qry_susa_fcst.stapel_nr,
    qry_susa_fcst.belegfeld1,
    qry_susa_fcst.kontobezeichnung_not_mdata,
    qry_susa_fcst.cf_acc_sort_code,
    qry_susa_fcst.i_comp,
    costfunc_choice(qry_susa_fcst.account_datev,
        qry_susa_fcst.project_code::character varying) AS costfunc_choice,

    qry_susa_fcst.p_mgr,
    qry_susa_fcst.rpt_acc_sort_code,
    qry_susa_fcst.pers_code,
    qry_susa_fcst.first_name,
    qry_susa_fcst.last_name,
    fcst_choice(func_thismonth(), qry_susa_fcst.period,
        qry_susa_fcst.z_type::character varying) AS fcst_choice,
    company_grouped(qry_susa_fcst.company::text::character varying) AS company_grouped,
    qry_susa_fcst.cf_direct,
    fx_rates_v01(qry_susa_fcst.amount / 1000::numeric, qry_susa_fcst.period,
        'OCRA'::character varying) AS ksek,
    qry_susa_fcst.amount * 0.0090413 AS ksekfix
FROM qry_susa_fcst
   LEFT JOIN tbl_chart_of_accounts ON qry_susa_fcst.account_datev::text =
       tbl_chart_of_accounts.account_datev::text;
       
GRANT SELECT ON public.qry_susa_fcst_c TO db_read;

/* View for updated */

CREATE OR REPLACE VIEW public.qry_susa_fcst_d (
    id,
    account_datev,
    name_datev,
    period,
    amount,
    hgb_acc_sort_code,
    soll,
    haben,
    zuordnung_bwa,
    bwa_titel,
    accounts_ssc,
    acc_description_ssc,
    ssc_acc_zeroend,
    ssc_account_class,
    i_comp,
    year,
    buchungstext,
    comment,
    comment_2,
    kost1,
    project_code,
    p_description,
    customer,
    p_mgr,
    z_type,
    fcst_choice,
    base_table,
    company,
    company_grouped,
    foreign_amount,
    gegenkonto,
    partner_name,
    datum,
    stapel_nr,
    belegfeld1,
    kontobezeichnung_not_mdata,
    cf_acc_sort_code,
    costfunc_choice,
    rpt_acc_sort_code,
    cf_direct,
    pers_code,
    first_name,
    last_name,
    ksek,
    ksekfix)
AS
SELECT qry_susa_fcst.id, qry_susa_fcst.account_datev, qry_susa_fcst.name_datev,
    qry_susa_fcst.period, qry_susa_fcst.amount, qry_susa_fcst.hgb_acc_sort_code, 
    qry_susa_fcst.soll, qry_susa_fcst.haben, qry_susa_fcst.zuordnung_bwa, 
    qry_susa_fcst.bwa_titel, qry_susa_fcst.accounts_ssc, 
    qry_susa_fcst.acc_description_ssc,
    tbl_chart_of_accounts.ssc_acc_zeroend,
    tbl_chart_of_accounts.ssc_account_class,
     
    qry_susa_fcst.i_comp, qry_susa_fcst.year, qry_susa_fcst.buchungstext, 
    qry_susa_fcst.comment, qry_susa_fcst.comment_2, qry_susa_fcst.kost1, 
    qry_susa_fcst.project_code, qry_susa_fcst.p_description, qry_susa_fcst.customer, 
    qry_susa_fcst.p_mgr, qry_susa_fcst.z_type, fcst_choice(func_thismonth(), qry_susa_fcst.period, qry_susa_fcst.z_type::character varying) AS fcst_choice, 
    qry_susa_fcst.base_table, qry_susa_fcst.company, company_grouped(qry_susa_fcst.company::text::character varying) AS company_grouped, 
    qry_susa_fcst.foreign_amount, qry_susa_fcst.gegenkonto, qry_susa_fcst.partner_name, qry_susa_fcst.datum, qry_susa_fcst.stapel_nr, qry_susa_fcst.belegfeld1, 
    qry_susa_fcst.kontobezeichnung_not_mdata, 
    qry_susa_fcst.cf_acc_sort_code, costfunc_choice(qry_susa_fcst.account_datev, qry_susa_fcst.project_code::character varying) AS costfunc_choice, 
    qry_susa_fcst.rpt_acc_sort_code, qry_susa_fcst.cf_direct, qry_susa_fcst.pers_code, 
    qry_susa_fcst.first_name, qry_susa_fcst.last_name, fx_rates_v01(qry_susa_fcst.amount / 1000::numeric, qry_susa_fcst.period, 'OCRA'::character varying) AS ksek, 
    qry_susa_fcst.amount * 0.0090558 AS ksekfix
FROM qry_susa_fcst
   LEFT JOIN tbl_chart_of_accounts ON qry_susa_fcst.account_datev::text =
       tbl_chart_of_accounts.account_datev::text;
 
 
GRANT SELECT ON public.qry_susa_fcst_d TO db_read;
  
  
CREATE OR REPLACE VIEW public.qry_crm (
    id,
    project_id,
    stage,
    text,
    z_partner_adj,
    ssc_main_party,
    z_year,
    z_amount,
    z_comment,
    zz_type,
    z_history,
    base_table)
AS
SELECT tbl_ssccrm.id, tbl_ssccrm.project_id, tbl_ssccrm.stage, tbl_ssccrm.text,
    tbl_ssccrm.z_partner_adj, tbl_ssccrm.ssc_main_party, 
    tbl_ssccrm.z_year, tbl_ssccrm.z_amount, tbl_ssccrm.z_comment, 
    'CRM'::text AS zz_type, tbl_ssccrm.z_history, 'tbl_ssccrm'::text AS base_table
FROM tbl_ssccrm tbl_ssccrm
UNION
SELECT qry_susa_fcst_c.id, qry_susa_fcst_c.project_code AS project_id,
    qry_susa_fcst_c.z_type AS stage, ''::character varying AS text, 
    qry_susa_fcst_c.partner_name AS z_partner_adj, 'ES - LSE Space GmbH'::character varying AS ssc_main_party, 
    2014 AS z_year, qry_susa_fcst_c.amount AS z_amount, ''::character varying AS z_comment, 
    'Forecast'::text AS zz_type, 'Actual'::text AS z_history, 'n.a.'::text AS base_table
FROM qry_susa_fcst_c
WHERE qry_susa_fcst_c.period >= 201401 AND qry_susa_fcst_c.period <= 201412 AND
    qry_susa_fcst_c.zuordnung_bwa::text = 'GuV'::text 
    AND (qry_susa_fcst_c.z_type = 'Actual'::text OR qry_susa_fcst_c.z_type = 'FC_F14v1'::text) 
    AND (qry_susa_fcst_c.company::text = 'LSE IFRS'::text OR qry_susa_fcst_c.company::text = 'LSE HGB'::text OR qry_susa_fcst_c.company::text = 'LSE'::text) 
    AND qry_susa_fcst_c.fcst_choice = 'Fcst'::text AND qry_susa_fcst_c.rpt_acc_sort_code::text = '00-Revenues'::text;

GRANT SELECT ON public.qry_crm TO db_read;