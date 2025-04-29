# Address Information

The comparison between the databases wos_b_202307, scopus_b_202307 and openalex_b_082023 using a sample of 5,000 different Digital Object Identifiers (DOI) and the corresponding address-document combinations has shown that no ‘Address_Full-String’ exists in the OpenAlex bibliometric database (BDB) and that it cannot be developed from several fields (organisation name, city, postcode, etc.). This is due to the pre-coding carried out by OpenAlex, which leads to a smaller number of different address-document combinations compared to the Web of Science (WoS) and Scopus.
Particularly with regard to these unassigned address strings, added value could be expected from curation with the help of institutional coding. Due to the address strings not found in the BDB, it was necessary to deviate from the planned procedure and use the raw data from OpenAlex for the comparison instead of the BDB. An institutional coding was carried out on the address strings of the raw data from OpenAlex and compared with the allocation rates of the current coding for the Web of Science (WoS_b_202307) and Scopus (Scopus_b_202307). 
There are major differences with the maximum number of characters in the address string. The longest string at the time of execution is 239 characters for WoS and 1,690 characters for Scopus, whereas the string in OpenAlex has a maximum of more than 24,000 characters. However, very long strings with more than 2,000 characters are only found in a few cases. As the institutional coding can handle strings up to a maximum length of 2,000 characters, the longer strings were shortened for the first OpenAlex instiutional coding.
Based on the long duration of the institutional coding on OpenAlex, a database comparison was carried out with publications from 2019 to date in order to reduce the duration and to be able to compare the affiliations and assignment results of the coding carried out. 
For the comparison, all existing ‘distinct’ DOIs with the corresponding affiliations in the comparative period were selected for German institutions.

```sql
select count(distinct doi) from datenbankvergleich.db_cutequals_oa_wos_scp_wos_scp; --- 4.014.277

select count(distinct doi) from datenbankvergleich.db_cutequals_oa_wos_scp_wos_scp where id_wos =1; -- 2.391.920

select count(distinct doi) from datenbankvergleich.db_cutequals_oa_wos_scp_wos_scp where id_scp =1; -- 2.353.696


select * from datenbankvergleich.db_cutequals_oa_wos_scp_wos_scp 
where in_openalex =1; -- 5.779.560 Affilliations

select * from datenbankvergleich.db_cutequals_oa_wos_scp_wos_scp 
where in_openalex =1 and id_wos=1; -- 3.478.676 Affilliations


select * from datenbankvergleich.db_cutequals_oa_wos_scp_wos_scp 
where in_openalex =1 and id_scp=1; -- 3.434.161 Affilliations


select * from datenbankvergleich.db_cutequals_oa_wos_scp_wos_scp 
where id_wos =1 and id_scp=1; -- 2.822.772 Affilliations


select * from datenbankvergleich.db_cutequals_oa_wos_scp_wos_scp 
where in_openalex =1 and id_wos=1 and id_scp=1; -- 2.822.772 Affilliations

select count(distinct doi) from datenbankvergleich.db_cutequals_oa_wos_scp_wos_scp where id_scp =1 and in_openalex =1 and id_wos=1; -- 1.912.986
```

-	The intersection between OpenAlex, the Web of Science and Scopus in the compared period is 1,912,986 distinct DOIs for 2,822,772 matched address-document combinations. The comparison includes the databases wos_b_202307 , scp_b_202307 and openalex_rep_202308.


Fundamental changes have been made to the address string for the new OpenAlex encodings to improve the runtime. The address strings now only contain one affiliation. This means that instead of one string with, for example, five different affiliations for the corresponding publication, five strings with one affiliation are created.
