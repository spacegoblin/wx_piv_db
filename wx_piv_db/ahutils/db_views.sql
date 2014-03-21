/*

DROP VIEW public.qry_susa_union;
DROP VIEW public.qry_susa_fcst_aurora;
DROP VIEW public.qry_susa_fcst_c;
DROP VIEW public.qry_susa_fcst;
DROP VIEW public.qry_susa_plan;
DROP VIEW public.qry_susa_act_group;
DROP VIEW public.qry_susa_aurora_act;
DROP VIEW public.qry_susa;


*/

/* Base view for the SUSA */

CREATE OR REPLACE VIEW public.qry_susa (
    id,
    account_datev,
    kontobezeichnung_not_mdata,
    soll,
    haben,
    period,
    name_datev,
    zuordnung_bwa,
    bwa_titel,
    /* ifrs_accounts, */
    ifrs_acc_sort_code,
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
    partner_int_ext,
    stapel_nr,
    belegfeld1,
    hgb_acc_sort_code,
    cf_acc_sort_code,
    i_comp,
    ssc_cost_centre,
    cc_ssc_function,
    p_mgr
     )
AS
SELECT tbl_susa.id, tbl_susa.account_datev,
    tbl_susa.kontobezeichnung_not_mdata, tbl_susa.soll, tbl_susa.haben, tbl_susa.period, tbl_chart_of_accounts.name_datev, tbl_chart_of_accounts.zuordnung_bwa, 
    tbl_chart_of_accounts.bwa_titel, 
    /* tbl_chart_of_accounts.ifrs_accounts, */ 
    tbl_chart_of_accounts.ifrs_acc_sort_code, tbl_chart_of_accounts.accounts_ssc, tbl_chart_of_accounts.acc_description_ssc, 
    tbl_susa.soll - tbl_susa.haben AS amount, "left"(tbl_susa.period::text, 4) AS year, 
    tbl_susa.gegenkonto, tbl_susa.buchungstext, tbl_susa.comment, 
    tbl_susa.comment_2, tbl_susa.kost1, 
    tbl_cost_centers.project_code::text AS project_code, 'Actual'::text AS z_type, 
    'tbl_susa'::text AS base_table, tbl_susa.company, tbl_susa.foreign_amount, tbl_cost_centers.customer, 
    tbl_cost_centers.internal_ext, tbl_cost_centers.business_unit, tbl_cost_centers.description AS p_description, 
    tbl_susa.datum, partner_name_v01(tbl_susa.gegenkonto)::text AS partner_name, 
    partner_int_ext_v01(tbl_susa.gegenkonto)::text AS partner_int_ext, tbl_susa.stapel_nr, 
    tbl_susa.belegfeld1,
    tbl_chart_of_accounts.hgb_acc_sort_code,
    tbl_chart_of_accounts.cf_acc_sort_code,
    tbl_chart_of_accounts.i_comp,
    tbl_chart_of_accounts.ssc_cost_centre,
    tbl_cost_centers.cc_ssc_function,
    tbl_cost_centers.p_mgr::text
FROM tbl_susa
   LEFT JOIN tbl_chart_of_accounts ON tbl_susa.account_datev::text =
       tbl_chart_of_accounts.account_datev::text
   LEFT JOIN tbl_cost_centers ON tbl_susa.kost1::text =
       tbl_cost_centers.costcenternr::text;

/* Base view for the SUSA Aurora (extra table) */  
     
CREATE OR REPLACE VIEW public.qry_susa_aurora_act (
    id,
    account_datev,
    kontobezeichnung_not_mdata,
    soll,
    haben,
    period,
    name_datev,
    zuordnung_bwa,
    bwa_titel,
    /* ifrs_accounts, */
    ifrs_acc_sort_code,
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
    partner_int_ext,
    stapel_nr,
    belegfeld1,
    hgb_acc_sort_code,
    cf_acc_sort_code,
    i_comp,
    ssc_cost_centre,
    cc_ssc_function,
    p_mgr
    )
AS
SELECT tbl_susa_aurora.id, tbl_susa_aurora.account_datev,
    tbl_susa_aurora.kontobezeichnung_not_mdata, tbl_susa_aurora.soll, tbl_susa_aurora.haben, tbl_susa_aurora.period, 
    tbl_chart_of_accounts.name_datev, tbl_chart_of_accounts.zuordnung_bwa, tbl_chart_of_accounts.bwa_titel, 
    /* tbl_chart_of_accounts.ifrs_accounts, */ 
    tbl_chart_of_accounts.ifrs_acc_sort_code, tbl_chart_of_accounts.accounts_ssc, tbl_chart_of_accounts.acc_description_ssc, 
    tbl_susa_aurora.soll - tbl_susa_aurora.haben AS amount, "left"(tbl_susa_aurora.period::text, 4) AS year, tbl_susa_aurora.gegenkonto, 
    tbl_susa_aurora.buchungstext, tbl_susa_aurora.comment, tbl_susa_aurora.comment_2, tbl_susa_aurora.kost1, ''::text AS project_code, 'Actual'::text AS z_type, 
    'tbl_susa_aurora'::text AS base_table, tbl_susa_aurora.company, tbl_susa_aurora.foreign_amount, '' AS customer, '' AS internal_ext, '' AS business_unit, 
    '' AS p_description, tbl_susa_aurora.datum, '' AS partner_name, ''::text AS partner_int_ext, tbl_susa_aurora.stapel_nr, 
    tbl_susa_aurora.belegfeld1,
    tbl_chart_of_accounts.hgb_acc_sort_code,
    tbl_chart_of_accounts.cf_acc_sort_code,
    tbl_chart_of_accounts.i_comp,
    tbl_chart_of_accounts.ssc_cost_centre,
    ''::text as tbl_cost_centers,
    ''::text as p_mgr
FROM tbl_susa_aurora
   LEFT JOIN tbl_chart_of_accounts ON tbl_susa_aurora.account_datev::text =
       tbl_chart_of_accounts.account_datev::text;   


/* View for the plan */

CREATE OR REPLACE VIEW public.qry_susa_plan (
    id,
    account_datev,
    kontobezeichnung_not_mdata,
    soll,
    haben,
    period,
    name_datev,
    zuordnung_bwa,
    bwa_titel,
    /* ifrs_accounts, */
    ifrs_acc_sort_code,
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
    partner_int_ext,
    stapel_nr,
    belegfeld1,
    hgb_acc_sort_code,
    cf_acc_sort_code,
    i_comp,
    ssc_cost_centre,
    cc_ssc_function,
    p_mgr
    )
AS
SELECT tbl_susa_plan.id, tbl_susa_plan.account_datev,
    tbl_susa_plan.kontobezeichnung_not_mdata, tbl_susa_plan.soll, tbl_susa_plan.haben, tbl_susa_plan.period, tbl_chart_of_accounts.name_datev, 
    tbl_chart_of_accounts.zuordnung_bwa, tbl_chart_of_accounts.bwa_titel, 
    /* tbl_chart_of_accounts.ifrs_accounts, */ 
    tbl_chart_of_accounts.ifrs_acc_sort_code, tbl_chart_of_accounts.accounts_ssc, 
    tbl_chart_of_accounts.acc_description_ssc, tbl_susa_plan.soll - tbl_susa_plan.haben AS amount, "left"(tbl_susa_plan.period::text, 4) AS year, 
    tbl_susa_plan.gegenkonto, tbl_susa_plan.buchungstext, tbl_susa_plan.comment, tbl_susa_plan.comment_2, ''::character varying(255) AS kost1, 
    tbl_susa_plan.project_code, tbl_susa_plan.z_type, 'tbl_susa_plan'::text AS base_table, tbl_susa_plan.company, tbl_susa_plan.foreign_amount, 
    tbl_cost_centers.customer, tbl_cost_centers.internal_ext, tbl_cost_centers.business_unit, tbl_cost_centers.description AS p_description, NULL::date AS datum, 
    partner_name_v01(tbl_susa_plan.gegenkonto)::text AS partner_name, partner_int_ext_v01(tbl_susa_plan.gegenkonto)::text AS partner_int_ext, 
    tbl_susa_plan.stapel_nr, ''::character varying(255) AS belegfeld1,
    tbl_chart_of_accounts.hgb_acc_sort_code,
    tbl_chart_of_accounts.cf_acc_sort_code,
    tbl_chart_of_accounts.i_comp,
    tbl_chart_of_accounts.ssc_cost_centre::text,
    tbl_cost_centers.cc_ssc_function::text,
    tbl_cost_centers.p_mgr::text
FROM tbl_susa_plan
   LEFT JOIN tbl_chart_of_accounts ON tbl_susa_plan.account_datev::text =
       tbl_chart_of_accounts.account_datev::text
   LEFT JOIN tbl_cost_centers ON tbl_susa_plan.project_code::text =
       tbl_cost_centers.project_code::text;

    
/* Group view for the SUSA */

CREATE OR REPLACE VIEW public.qry_susa_act_group (
    id,
    account_datev,
    kontobezeichnung_not_mdata,
    soll,
    haben,
    period,
    name_datev,
    zuordnung_bwa,
    bwa_titel,
    /* ifrs_accounts, */
    ifrs_acc_sort_code,
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
    partner_int_ext,
    stapel_nr,
    belegfeld1,
    hgb_acc_sort_code,
    cf_acc_sort_code,
    i_comp,
    ssc_cost_centre,
    cc_ssc_function,
    p_mgr
    )
AS
SELECT qry_susa.id, qry_susa.account_datev,
    qry_susa.kontobezeichnung_not_mdata, qry_susa.soll, qry_susa.haben, qry_susa.period, qry_susa.name_datev, 
    qry_susa.zuordnung_bwa, qry_susa.bwa_titel, 
    /* qry_susa.ifrs_accounts, */ 
    qry_susa.ifrs_acc_sort_code, 
    qry_susa.accounts_ssc, qry_susa.acc_description_ssc, qry_susa.amount, qry_susa.year, 
    qry_susa.gegenkonto, qry_susa.buchungstext, qry_susa.comment, qry_susa.comment_2, 
    qry_susa.kost1, qry_susa.project_code, qry_susa.z_type, qry_susa.base_table, qry_susa.company, 
    qry_susa.foreign_amount, qry_susa.customer, qry_susa.internal_ext, qry_susa.business_unit, 
    qry_susa.p_description, qry_susa.datum, qry_susa.partner_name, qry_susa.partner_int_ext, qry_susa.stapel_nr, 
    qry_susa.belegfeld1,
    qry_susa.hgb_acc_sort_code, 
    qry_susa.cf_acc_sort_code,
    qry_susa.i_comp,
    qry_susa.ssc_cost_centre,
    qry_susa.cc_ssc_function,
    qry_susa.p_mgr
FROM qry_susa
UNION
SELECT qry_susa_aurora_act.id, qry_susa_aurora_act.account_datev,
    qry_susa_aurora_act.kontobezeichnung_not_mdata, qry_susa_aurora_act.soll, qry_susa_aurora_act.haben, 
    qry_susa_aurora_act.period, qry_susa_aurora_act.name_datev, qry_susa_aurora_act.zuordnung_bwa, 
    qry_susa_aurora_act.bwa_titel, 
    /* qry_susa_aurora_act.ifrs_accounts, */ 
    qry_susa_aurora_act.ifrs_acc_sort_code, 
    qry_susa_aurora_act.accounts_ssc, qry_susa_aurora_act.acc_description_ssc, qry_susa_aurora_act.amount, 
    qry_susa_aurora_act.year, qry_susa_aurora_act.gegenkonto, qry_susa_aurora_act.buchungstext, qry_susa_aurora_act.comment, 
    qry_susa_aurora_act.comment_2, qry_susa_aurora_act.kost1, qry_susa_aurora_act.project_code, qry_susa_aurora_act.z_type, 
    qry_susa_aurora_act.base_table, qry_susa_aurora_act.company, qry_susa_aurora_act.foreign_amount, qry_susa_aurora_act.customer, 
    qry_susa_aurora_act.internal_ext, qry_susa_aurora_act.business_unit, qry_susa_aurora_act.p_description, qry_susa_aurora_act.datum, 
    qry_susa_aurora_act.partner_name, qry_susa_aurora_act.partner_int_ext, qry_susa_aurora_act.stapel_nr, qry_susa_aurora_act.belegfeld1,
    qry_susa_aurora_act.hgb_acc_sort_code, 
    qry_susa_aurora_act.cf_acc_sort_code,
    qry_susa_aurora_act.i_comp,
    qry_susa_aurora_act.ssc_cost_centre,
    qry_susa_aurora_act.cc_ssc_function,
    qry_susa_aurora_act.p_mgr
FROM qry_susa_aurora_act;

  

       
/* View for the plan  */

CREATE OR REPLACE VIEW public.qry_susa_fcst (
    id,
    account_datev,
    kontobezeichnung_not_mdata,
    soll,
    haben,
    period,
    name_datev,
    zuordnung_bwa,
    bwa_titel,
    /* ifrs_accounts, */
    ifrs_acc_sort_code,
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
    partner_int_ext,
    stapel_nr,
    belegfeld1,
    hgb_acc_sort_code,
    cf_acc_sort_code,
    i_comp,
    ssc_cost_centre,
    cc_ssc_function,
    p_mgr
    )
    
AS
SELECT qry_susa.id, qry_susa.account_datev,
    qry_susa.kontobezeichnung_not_mdata, qry_susa.soll, qry_susa.haben, qry_susa.period, qry_susa.name_datev, qry_susa.zuordnung_bwa, qry_susa.bwa_titel, 
    /* qry_susa.ifrs_accounts, */ 
    qry_susa.ifrs_acc_sort_code, qry_susa.accounts_ssc, qry_susa.acc_description_ssc, qry_susa.amount, qry_susa.year, qry_susa.gegenkonto, qry_susa.buchungstext, 
    qry_susa.comment, qry_susa.comment_2, qry_susa.kost1, qry_susa.project_code, qry_susa.z_type, 
    'tbl_susa' as base_table, 
    qry_susa.company, qry_susa.foreign_amount, 
    qry_susa.customer, qry_susa.internal_ext, qry_susa.business_unit, qry_susa.p_description, qry_susa.datum, qry_susa.partner_name, qry_susa.partner_int_ext, 
    qry_susa.stapel_nr, 
    qry_susa.belegfeld1,
    qry_susa.hgb_acc_sort_code,
    qry_susa.cf_acc_sort_code,
    qry_susa.i_comp,
    qry_susa.ssc_cost_centre,
    qry_susa.cc_ssc_function,
    qry_susa.p_mgr
    
FROM qry_susa
UNION
SELECT qry_susa_plan.id, qry_susa_plan.account_datev,
    qry_susa_plan.kontobezeichnung_not_mdata, qry_susa_plan.soll, qry_susa_plan.haben, qry_susa_plan.period, qry_susa_plan.name_datev, qry_susa_plan.zuordnung_bwa, qry_susa_plan.bwa_titel, 
    /* qry_susa_plan.ifrs_accounts, */ 
    qry_susa_plan.ifrs_acc_sort_code, qry_susa_plan.accounts_ssc, qry_susa_plan.acc_description_ssc, qry_susa_plan.amount, qry_susa_plan.year, qry_susa_plan.gegenkonto, 
    qry_susa_plan.buchungstext, qry_susa_plan.comment, qry_susa_plan.comment_2, qry_susa_plan.kost1, qry_susa_plan.project_code, qry_susa_plan.z_type, qry_susa_plan.base_table, 
    qry_susa_plan.company, qry_susa_plan.foreign_amount, qry_susa_plan.customer, qry_susa_plan.internal_ext, qry_susa_plan.business_unit, qry_susa_plan.p_description, 
    qry_susa_plan.datum, qry_susa_plan.partner_name, qry_susa_plan.partner_int_ext, qry_susa_plan.stapel_nr, 
    qry_susa_plan.belegfeld1,
    qry_susa_plan.hgb_acc_sort_code,
    qry_susa_plan.cf_acc_sort_code,
    qry_susa_plan.i_comp,
    qry_susa_plan.ssc_cost_centre,
    qry_susa_plan.cc_ssc_function,
    qry_susa_plan.p_mgr
    
FROM qry_susa_plan
WHERE qry_susa_plan.period >= 201312 AND (qry_susa_plan.z_type::text =
    'P_14_02'::text 
    OR qry_susa_plan.z_type::text = 'FC_13'::text
    OR qry_susa_plan.z_type::text = 'FC_F14v1'::text
    );
    

/* View for the union plan aurora */

CREATE OR REPLACE VIEW public.qry_susa_fcst_aurora (
    id,
    account_datev,
    kontobezeichnung_not_mdata,
    soll,
    haben,
    period,
    name_datev,
    zuordnung_bwa,
    bwa_titel,
    /* ifrs_accounts, */
    ifrs_acc_sort_code,
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
    partner_int_ext,
    stapel_nr,
    belegfeld1,
    hgb_acc_sort_code,
    cf_acc_sort_code,
    i_comp,
    ssc_cost_centre,
    cc_ssc_function,
    p_mgr
)
AS
SELECT qry_susa_aurora_act.id, qry_susa_aurora_act.account_datev,
    qry_susa_aurora_act.kontobezeichnung_not_mdata, qry_susa_aurora_act.soll, qry_susa_aurora_act.haben, qry_susa_aurora_act.period, 
    qry_susa_aurora_act.name_datev, qry_susa_aurora_act.zuordnung_bwa, qry_susa_aurora_act.bwa_titel, 
    /* qry_susa_aurora_act.ifrs_accounts, */ 
    qry_susa_aurora_act.ifrs_acc_sort_code, qry_susa_aurora_act.accounts_ssc, qry_susa_aurora_act.acc_description_ssc, qry_susa_aurora_act.amount, 
    qry_susa_aurora_act.year, qry_susa_aurora_act.gegenkonto, qry_susa_aurora_act.buchungstext, qry_susa_aurora_act.comment, 
    qry_susa_aurora_act.comment_2, qry_susa_aurora_act.kost1, qry_susa_aurora_act.project_code, qry_susa_aurora_act.z_type, 
    qry_susa_aurora_act.base_table, qry_susa_aurora_act.company, qry_susa_aurora_act.foreign_amount, qry_susa_aurora_act.customer, 
    qry_susa_aurora_act.internal_ext, 
    qry_susa_aurora_act.business_unit,
    qry_susa_aurora_act.p_description, qry_susa_aurora_act.datum, qry_susa_aurora_act.partner_name, 
    qry_susa_aurora_act.partner_int_ext, qry_susa_aurora_act.stapel_nr, 
    qry_susa_aurora_act.belegfeld1,
    qry_susa_aurora_act.hgb_acc_sort_code,
    qry_susa_aurora_act.cf_acc_sort_code,
    qry_susa_aurora_act.i_comp,
    qry_susa_aurora_act.ssc_cost_centre,
    qry_susa_aurora_act.cc_ssc_function,
    qry_susa_aurora_act.p_mgr
    
FROM qry_susa_aurora_act
UNION
SELECT qry_susa_plan.id, qry_susa_plan.account_datev,
    qry_susa_plan.kontobezeichnung_not_mdata, qry_susa_plan.soll, qry_susa_plan.haben, qry_susa_plan.period, qry_susa_plan.name_datev, 
    qry_susa_plan.zuordnung_bwa, qry_susa_plan.bwa_titel, 
    /* qry_susa_plan.ifrs_accounts, */ 
    qry_susa_plan.ifrs_acc_sort_code, qry_susa_plan.accounts_ssc, 
    qry_susa_plan.acc_description_ssc, qry_susa_plan.amount, qry_susa_plan.year, qry_susa_plan.gegenkonto, qry_susa_plan.buchungstext, qry_susa_plan.comment, 
    qry_susa_plan.comment_2, qry_susa_plan.kost1, qry_susa_plan.project_code, qry_susa_plan.z_type, qry_susa_plan.base_table, qry_susa_plan.company, 
    qry_susa_plan.foreign_amount, qry_susa_plan.customer, 
    qry_susa_plan.internal_ext, 
    qry_susa_plan.business_unit,
    qry_susa_plan.p_description, qry_susa_plan.datum, 
    qry_susa_plan.partner_name, qry_susa_plan.partner_int_ext, qry_susa_plan.stapel_nr, 
    qry_susa_plan.belegfeld1,
    qry_susa_plan.hgb_acc_sort_code,
    qry_susa_plan.cf_acc_sort_code,
    qry_susa_plan.i_comp,
    qry_susa_plan.ssc_cost_centre,
    qry_susa_plan.cc_ssc_function,
    qry_susa_plan.p_mgr
    
FROM qry_susa_plan
WHERE qry_susa_plan.period >= 201312 AND (qry_susa_plan.z_type::text =
    'P_14_02'::text 
   /* OR qry_susa_plan.z_type::text = 'FC_13'::text */
    OR qry_susa_plan.z_type::text = 'FC_F14v1'::text) AND qry_susa_plan.company::text = 'Aurora'::text;
    



/* View for the union plan actuals */

CREATE OR REPLACE VIEW public.qry_susa_union (
    id,
    account_datev,
    kontobezeichnung_not_mdata,
    soll,
    haben,
    period,
    name_datev,
    zuordnung_bwa,
    bwa_titel,
    /* ifrs_accounts, */
    ifrs_acc_sort_code,
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
    partner_int_ext,
    stapel_nr,
    belegfeld1,
    hgb_acc_sort_code,
    cf_acc_sort_code,
    i_comp,
    ssc_cost_centre,
    cc_ssc_function,
    p_mgr
    )
AS
SELECT qry_susa.id, qry_susa.account_datev,
    qry_susa.kontobezeichnung_not_mdata, qry_susa.soll, qry_susa.haben, qry_susa.period, qry_susa.name_datev, qry_susa.zuordnung_bwa, qry_susa.bwa_titel, 
    /* qry_susa.ifrs_accounts, */ 
    qry_susa.ifrs_acc_sort_code, qry_susa.accounts_ssc, qry_susa.acc_description_ssc, qry_susa.amount, qry_susa.year, qry_susa.gegenkonto, 
    qry_susa.buchungstext, qry_susa.comment, qry_susa.comment_2, qry_susa.kost1, qry_susa.project_code, qry_susa.z_type, qry_susa.base_table, 
    qry_susa.company, qry_susa.foreign_amount, qry_susa.customer, qry_susa.internal_ext, qry_susa.business_unit, qry_susa.p_description, 
    qry_susa.datum, qry_susa.partner_name, qry_susa.partner_int_ext, qry_susa.stapel_nr, 
    qry_susa.belegfeld1,
    qry_susa.hgb_acc_sort_code,
    qry_susa.cf_acc_sort_code,
    qry_susa.i_comp,
    qry_susa.ssc_cost_centre,
    qry_susa.cc_ssc_function,
    qry_susa.p_mgr
    
FROM qry_susa
UNION
SELECT qry_susa_plan.id, qry_susa_plan.account_datev,
    qry_susa_plan.kontobezeichnung_not_mdata, qry_susa_plan.soll, qry_susa_plan.haben, qry_susa_plan.period, qry_susa_plan.name_datev, 
    qry_susa_plan.zuordnung_bwa, qry_susa_plan.bwa_titel, 
    /* qry_susa_plan.ifrs_accounts, */ 
    qry_susa_plan.ifrs_acc_sort_code, qry_susa_plan.accounts_ssc, qry_susa_plan.acc_description_ssc, qry_susa_plan.amount, qry_susa_plan.year, 
    qry_susa_plan.gegenkonto, qry_susa_plan.buchungstext, qry_susa_plan.comment, qry_susa_plan.comment_2, qry_susa_plan.kost1, qry_susa_plan.project_code, 
    qry_susa_plan.z_type, qry_susa_plan.base_table, qry_susa_plan.company, qry_susa_plan.foreign_amount, qry_susa_plan.customer, qry_susa_plan.internal_ext, 
    qry_susa_plan.business_unit, qry_susa_plan.p_description, qry_susa_plan.datum, qry_susa_plan.partner_name, qry_susa_plan.partner_int_ext, qry_susa_plan.stapel_nr, 
    qry_susa_plan.belegfeld1,
    qry_susa_plan.hgb_acc_sort_code,
    qry_susa_plan.cf_acc_sort_code,
    qry_susa_plan.i_comp,
    qry_susa_plan.ssc_cost_centre,
    qry_susa_plan.cc_ssc_function,
    qry_susa_plan.p_mgr
    
FROM qry_susa_plan;

/* View for the qry_susa_fcst_c */

CREATE OR REPLACE VIEW public.qry_susa_fcst_c (
    id,
    account_datev,
    kontobezeichnung_not_mdata,
    soll,
    haben,
    period,
    name_datev,
    zuordnung_bwa,
    bwa_titel,
    ifrs_acc_sort_code,
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
    partner_int_ext,
    stapel_nr,
    belegfeld1,
    hgb_acc_sort_code,
    cf_acc_sort_code,
    i_comp,
    ssc_cost_centre,
    cc_ssc_function,
    p_mgr,
    fcst_choice)
AS
SELECT qry_susa_fcst.id, qry_susa_fcst.account_datev,
    qry_susa_fcst.kontobezeichnung_not_mdata, qry_susa_fcst.soll, qry_susa_fcst.haben, qry_susa_fcst.period, 
    qry_susa_fcst.name_datev, qry_susa_fcst.zuordnung_bwa, qry_susa_fcst.bwa_titel, 
    qry_susa_fcst.ifrs_acc_sort_code, 
    
    qry_susa_fcst.accounts_ssc, qry_susa_fcst.acc_description_ssc, qry_susa_fcst.amount, qry_susa_fcst.year, 
    qry_susa_fcst.gegenkonto, qry_susa_fcst.buchungstext, qry_susa_fcst.comment, qry_susa_fcst.comment_2, qry_susa_fcst.kost1, 
    qry_susa_fcst.project_code, qry_susa_fcst.z_type, qry_susa_fcst.base_table, qry_susa_fcst.company, qry_susa_fcst.foreign_amount, 
    qry_susa_fcst.customer, qry_susa_fcst.internal_ext, qry_susa_fcst.business_unit, qry_susa_fcst.p_description, 
    qry_susa_fcst.datum, qry_susa_fcst.partner_name, qry_susa_fcst.partner_int_ext, qry_susa_fcst.stapel_nr, qry_susa_fcst.belegfeld1, 
    qry_susa_fcst.hgb_acc_sort_code, 
    qry_susa_fcst.cf_acc_sort_code, 
    qry_susa_fcst.i_comp, 
    qry_susa_fcst.ssc_cost_centre,
    qry_susa_fcst.cc_ssc_function,
    qry_susa_fcst.p_mgr,
    fcst_choice(201402, qry_susa_fcst.period, qry_susa_fcst.z_type::character varying) AS fcst_choice
FROM qry_susa_fcst
   LEFT JOIN tbl_chart_of_accounts ON qry_susa_fcst.account_datev::text =
       tbl_chart_of_accounts.account_datev::text;