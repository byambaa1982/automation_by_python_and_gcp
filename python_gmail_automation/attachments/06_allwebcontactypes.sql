/****** Object:  View [ALAS].[vwAllWebContactTypes]    Script Date: 5/5/2023 11:18:49 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE   VIEW [ALAS].[vw_AllWebContactTypes]
AS

SELECT alas.user_profile .UserId, 
       STUFF((SELECT ', ' + alas.aspnet_Roles.RoleName 
              FROM   alas.aspnet_UsersInRoles
                     JOIN alas.aspnet_Roles
                       ON alas.aspnet_UsersInRoles.RoleId = alas.aspnet_Roles.RoleId
              WHERE  alas.aspnet_UsersInRoles.UserId = alas.user_profile.UserId 
			  ORDER BY alas.aspnet_Roles.RoleName
              FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, '') AS Contact_Types
FROM   alas.user_profile  
GROUP BY alas.user_profile.userid
GO


