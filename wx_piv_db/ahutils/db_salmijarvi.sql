/* To create table for Salmijarvi from Agresso */

CREATE TABLE public.tbl_salmijarvi_agresso (
  id SERIAL NOT NULL,
  t VARCHAR(255),
  vt VARCHAR(255),
  ver_nr VARCHAR(255),
  nr VARCHAR(255),
  ver_datum DATE,
  period INTEGER,
  konto VARCHAR(255),
  konto_t VARCHAR(255),
  kst VARCHAR(255),
  projekt VARCHAR(255),
  projekt_t VARCHAR(255),
  mk VARCHAR(255),
  p_text VARCHAR(255),
  amount NUMERIC(20,2) DEFAULT 0 NOT NULL,
  resk_nr VARCHAR(255),
  resk_nr_t VARCHAR(255),
  company VARCHAR(255),
  imp_str VARCHAR(255),
  PRIMARY KEY(id)
) ;