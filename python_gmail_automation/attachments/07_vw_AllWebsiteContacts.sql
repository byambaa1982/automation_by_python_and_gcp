/****** Object:  View [ALAS].[vw_AllWebsiteContacts]    Script Date: 5/9/2023 1:03:09 PM ******/
CREATE   VIEW [ALAS].[vw_AllWebsiteContacts]
AS

with cte_address as(
select 
ADDRESS_KEY,
case when firm_key is null then branch_office_key else firm_key end office_key,
case when firm_key is null then 'Branch' 
     when firm_key is not null then 'Main' 
     end office_type,

address_line_1,
address_line_2,
address_line_3,
city,
state_or_province,
zip_or_postal_code,
country
from
alas.firm_address)

 

SELECT distinct
p.UserId 
,s.SalutationBasic
,p.Preferred_Name 
,p.First_Name 
,p.MiddleName 
,p.Last_Name 
,m.Email
,p.Suffix
,p.Esquire
,p.JobTitle
,vw_ct.contact_types
,m.IsApproved
,f.Firm_Number
,f.firm_key
,f.Full_Firm_Name
,f.Short_Firm_Name
,f.Firm_Status
,cte_address.ADDRESS_LINE_1
,cte_address.ADDRESS_LINE_2
,cte_address.ADDRESS_LINE_3
,cte_address.CITY
,cte_address.state_or_province
,cte_address.zip_or_postal_code
,cte_address.country
,cte_address.office_type
FROM        alas.user_profile as p
INNER JOIN    alas.firm as f
    ON p.Firm_Key = f.Firm_Key 
INNER JOIN  alas.aspnet_Membership as m
    ON p.UserId = m.UserId
LEFT JOIN alas.Salutation as s 
ON p.SaluteId=s.saluteid
LEFT JOIN cte_address 
ON cte_address.ADDRESS_KEY = p.BranchAddressId
LEFT JOIN ALAS.vw_AllWebContactTypes as vw_ct
ON vw_ct.userid	= p.UserId
GO