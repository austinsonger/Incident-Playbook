



### Azure Microsoft Authorization API



| METHOD                                                       | SHORT DESCRIPTION                                         | ACCESS LEVEL | DESCRIPTION                                                  | ORIGINS |
| ------------------------------------------------------------ | --------------------------------------------------------- | ------------ | ------------------------------------------------------------ | ------- |
| `Microsoft.Authorization/elevateAccess/action`| Assigns the caller to User Access Administrator role      | Write        | Grants the caller User Access Administrator access at the tenant scope. |         |
| `Microsoft.Authorization/classicAdministrators/read`| Get administrator                                         | Read         | Reads the administrators for the subscription.               |         |
| `Microsoft.Authorization/classicAdministrators/write`| Set administrator                                         | Write        | Add or modify administrator to a subscription.               |         |
| `Microsoft.Authorization/classicAdministrators/delete`| Delete administrator                                      | Write        | Removes the administrator from the subscription.             |         |
| `Microsoft.Authorization/roleAssignments/read`| Get role assignment                                       | Read         | Get information about a role assignment.                     |         |
| `Microsoft.Authorization/roleAssignments/write`| Create role assignment                                    | Write        | Create a role assignment at the specified scope.             |         |
| Microsoft.Authorization/roleAssignments/delete| Delete role assignment                                    | Write        | Delete a role assignment at the specified scope.             |         |
| Microsoft.Authorization/permissions/read| List permissions                                          | Read         | Lists all the permissions the caller has at a given scope.   |         |
| Microsoft.Authorization/locks/read| Get management locks                                      | Read         | Gets locks at the specified scope.                           |         |
| Microsoft.Authorization/locks/write| Add management locks                                      | Write        | Add locks at the specified scope.                            |         |
| Microsoft.Authorization/locks/delete| Delete management locks                                   | Write        | Delete locks at the specified scope.                         |         |
| Microsoft.Authorization/roleDefinitions/read| Get role definition                                       | Read         | Get information about a role definition.                     |         |
| Microsoft.Authorization/roleDefinitions/write| Create or update custom role definition                   | Write        | Create or update a custom role definition with specified permissions and assignable scopes. |         |
| Microsoft.Authorization/roleDefinitions/delete| Delete custom role definition                             | Write        | Delete the specified custom role definition.                 |         |
| Microsoft.Authorization/providerOperations/read| Get operations for resource providers                     | Read         | Get operations for all resource providers which can be used in role definitions. |         |
| Microsoft.Authorization/policySetDefinitions/read| Get policy set definition                                 | Read         | Get information about a policy set definition.               |         |
| Microsoft.Authorization/policySetDefinitions/write| Create policy set definition                              | Write        | Create a custom policy set definition.                       |         |
| Microsoft.Authorization/policySetDefinitions/delete| Delete policy set definition                              | Write        | Delete a policy set definition.                              |         |
| Microsoft.Authorization/policyDefinitions/read| Get policy definition                                     | Read         | Get information about a policy definition.                   |         |
| Microsoft.Authorization/policyDefinitions/write| Create policy definition                                  | Write        | Create a custom policy definition.                           |         |
| Microsoft.Authorization/policyDefinitions/delete| Delete policy definition                                  | Write        | Delete a policy definition.                                  |         |
| Microsoft.Authorization/policyAssignments/read| Get policy assignment                                     | Read         | Get information about a policy assignment.                   |         |
| Microsoft.Authorization/policyAssignments/write              | Create policy assignment                                  | Write        | Create a policy assignment at the specified scope.           |         |
| Microsoft.Authorization/policyAssignments/delete             | Delete policy assignment                                  | Write        | Delete a policy assignment at the specified scope.           |         |
| Microsoft.Authorization/policyAssignments/exempt/action      | Exempt policy assignment                                  | Write        | Exempt a policy assignment at the specified scope.           |         |
| Microsoft.Authorization/operations/read                      | Get operations                                            | Read         | Gets the list of operations.                                 |         |
| Microsoft.Authorization/classicAdministrators/operationstatuses/read | Get administrator operation statuses                      | Read         | Gets the administrator opreation statuses of the subscription. |         |
| Microsoft.Authorization/denyAssignments/read                 | Get deny assignment                                       | Read         | Get information about a deny assignment.                     |         |
| Microsoft.Authorization/denyAssignments/write                | Create deny assignment                                    | Write        | Create a deny assignment at the specified scope.             |         |
| Microsoft.Authorization/denyAssignments/delete               | Delete deny assignment                                    | Write        | Delete a deny assignment at the specified scope.             |         |
| Microsoft.Authorization/policies/audit/action                | 'audit' Policy action                                     | Write        | Action taken as a result of evaluation of Azure Policy with 'audit' effect. | System  |
| Microsoft.Authorization/policies/auditIfNotExists/action     | 'auditIfNotExists' Policy action                          | Write        | Action taken as a result of evaluation of Azure Policy with 'auditIfNotExists' effect. | System  |
| Microsoft.Authorization/policies/deny/action                 | 'deny' Policy action                                      | Write        | Action taken as a result of evaluation of Azure Policy with 'deny' effect. | System  |
| Microsoft.Authorization/policies/deployIfNotExists/action    | 'deployIfNotExists' Policy action                         | Write        | Action taken as a result of evaluation of Azure Policy with 'deployIfNotExists' effect. | System  |
| Microsoft.Authorization/policyAssignments/resourceManagementPrivateLinks/read | Get Resource Management Private Link                      | Read         | Get information about resource management private link.      |         |
| Microsoft.Authorization/policyAssignments/resourceManagementPrivateLinks/write | Write a Resource Management Private Link                  | Write        | Creates or updates a resource management private link.       |         |
| Microsoft.Authorization/policyAssignments/resourceManagementPrivateLinks/delete | Delete a Resource Management Private Link                 | Write        | Deletes a resource management private link.                  |         |
| Microsoft.Authorization/policyAssignments/resourceManagementPrivateLinks/privateEndpointConnectionProxies/read | Get Private Endpoint Connection Proxy                     | Read         | Get information about private endpoint connection proxy.     |         |
| Microsoft.Authorization/policyAssignments/resourceManagementPrivateLinks/privateEndpointConnectionProxies/write | Write a Private Endpoint Connection Proxy                 | Write        | Creates or updates a private endpoint connection proxy.      |         |
| Microsoft.Authorization/policyAssignments/resourceManagementPrivateLinks/privateEndpointConnectionProxies/delete | Delete a Private Endpoint Connection Proxy                | Write        | Deletes a private endpoint connection proxy.                 |         |
| Microsoft.Authorization/policyAssignments/resourceManagementPrivateLinks/privateEndpointConnectionProxies/validate/action | Validate a Private Endpoint Connection Proxy              | Write        | Validates a private endpoint connection proxy.               |         |
| Microsoft.Authorization/policyAssignments/resourceManagementPrivateLinks/privateEndpointConnections/read | Get Private Endpoint Connection                           | Read         | Get information about private endpoint connection.           |         |
| Microsoft.Authorization/policyAssignments/resourceManagementPrivateLinks/privateEndpointConnections/write | Write a Private Endpoint Connection                       | Write        | Creates or updates a private endpoint connection.            |         |
| Microsoft.Authorization/policyAssignments/resourceManagementPrivateLinks/privateEndpointConnections/delete | Delete a Private Endpoint Connection                      | Write        | Deletes a private endpoint connection.                       |         |
| Microsoft.Authorization/policyAssignments/privateLinkAssociations/read | Get Private Link Association                              | Read         | Get information about private link association.              |         |
| Microsoft.Authorization/policyAssignments/privateLinkAssociations/write | Write a Private Link Association                          | Write        | Creates or updates a private link association.               |         |
| Microsoft.Authorization/policyAssignments/privateLinkAssociations/delete | Delete a Private Link Association                         | Write        | Deletes a private link association.                          |         |
| Microsoft.Authorization/policyExemptions/read                | Get policy exemption                                      | Read         | Get information about a policy exemption.                    |         |
| Microsoft.Authorization/policyExemptions/write               | Create policy exemption                                   | Write        | Create a policy exemption at the specified scope.            |         |
| Microsoft.Authorization/policyExemptions/delete              | Delete policy exemption                                   | Write        | Delete a policy exemption at the specified scope.            |         |
| Microsoft.Authorization/roleAssignmentScheduleRequests/read  | Get Role assignment schedule request                      | Read         | Gets the role assignment schedule requests at given scope.   |         |
| Microsoft.Authorization/roleAssignmentScheduleRequests/write | Write Role assignment schedule request                    | Write        | Creates a role assignment schedule request at given scope.   |         |
| Microsoft.Authorization/roleAssignmentScheduleRequests/cancel/action | Cancel Role assignment schedule request                   | Write        | Cancels a pending role assignment schedule request.          |         |
| Microsoft.Authorization/roleEligibilityScheduleRequests/read | Get Role eligibility schedule request                     | Read         | Gets the role eligibility schedule requests at given scope.  |         |
| Microsoft.Authorization/roleEligibilityScheduleRequests/write | Write Role eligibility schedule request                   | Write        | Creates a role eligibility schedule request at given scope.  |         |
| Microsoft.Authorization/roleEligibilityScheduleRequests/cancel/action | Cancel Role eligibility schedule request                  | Write        | Cancels a pending role eligibility schedule request.         |         |
| Microsoft.Authorization/roleAssignmentSchedules/read         | Get Role assignment schedule                              | Read         | Gets the role assignment schedules at given scope.           |         |
| Microsoft.Authorization/roleEligibilitySchedules/read        | Get Role eligibility schedule                             | Read         | Gets the role eligibility schedules at given scope.          |         |
| Microsoft.Authorization/roleAssignmentScheduleInstances/read | Get Role assignment schedule instance                     | Read         | Gets the role assignment schedule instances at given scope.  |         |
| Microsoft.Authorization/roleEligibilityScheduleInstances/read | Get Role eligibility schedule instance                    | Read         | Gets the role eligibility schedule instances at given scope. |         |
| Microsoft.Authorization/roleManagementPolicies/read          | Get Role management policy                                | Read         | Get Role management policies.                                |         |
| Microsoft.Authorization/roleManagementPolicies/write         | Write Role management policy                              | Write        | Update a role management policy.                             |         |
| Microsoft.Authorization/roleManagementPolicyAssignments/read | Get Role management policy assignment                     | Read         | Get role management policy assignments.                      |         |
| Microsoft.Authorization/diagnosticSettings/read              | Get information about diagnostics settings                | Read         | Read the information about diagnostics settings.             |         |
| Microsoft.Authorization/diagnosticSettings/write             | Write to diagnostics settings                             | Write        | Create or update the information of diagnostics settings.    |         |
| Microsoft.Authorization/diagnosticSettings/delete            | Delete a diagnostics setting                              | Write        | Delete diagnostics settings.                                 |         |
| Microsoft.Authorization/diagnosticSettingsCategories/read    | Read the information about diagnostic settings categories | Read         | Get the information about diagnostic settings categories.    |         |


