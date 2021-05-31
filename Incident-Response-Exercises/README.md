# Incident Response Exercises


<!--

## 1. Top level Risks
Broad, strategic risks typically expressed by a board or C-Suite when asked by a security team. These may not be measured often, but will set high level vision for a security organization.

- A trust issue has threatened investors (_We don't want to hurt stock price_)
- A trust issue has created a press event. (_Keep us out of the press_)
- A trust issue has begun a regulatory / legal event. (_We don't want to get sued_)
- A trust issue has created a loss in customer activity. (_We want to keep customers happy_)
- A trust issue is exacerbated due to a poorly handled response. (_We should never be caught off guard_)
- An executive is removed do to a mishandled trust issue. (_I want to keep my job_)

> Leadership may call out far more specific risks, and that is OK. ("_A warehouse is offline_")

## 2. Scenarios that influence these risks
Risks can be decomposed from top level risks voiced by leadership. These would calibrate a team toward specific issues. Here is an example:

- A trust issue has created a loss in customer activity.
  - Our application was exploited and customer data was exposed.
    - An IDOR was discovered by an adversary and exploited.
    - An RCE was discovered by an adversary and exploited.
    - Our application retrieved objects from the wrong customer's S3 bucket when exporting data.  

## 3. Tasks that influence these risks
With target risks in mind, a team can pursue OKRs to influence the likelihood of information security scenarios occurring. This is well covered in [better OKR's](https://medium.com/@magoo/how-to-measure-risk-with-a-better-okr-c259bccf359e). This approach heavily relies on forecasting.

---

## Reference Scenarios

### Common scenario modifiers
These are typical additions to help prioritize the most relevant scenarios. They are not typically scenarios themselves, but help focus mitigation efforts to the highest priority problems.

Some scenarios are only important if they are capable of trigger an incident of a certain severity.

> A *P0 incident* has involved...

> A P0 incident has involved an employee who was not off-boarded correctly.

> A P0 incident has resulted because an attacker bypassed rate limiting.

Some bugs might not meet a specific "severity" classification but end up leveraged criminally anyways.

> ...was exploited "*in the wild*"

> An RCE discovered in our software was exploited "in the wild".

> An exploit targeting the configuration of web server we host has been observed in the wild.

The publicity involved with a scenario may be the goal of reduction efforts.

> The *press has disclosed*...

> An employee has leaked confidential data which the press has disclosed.

> We have botched a vulnerability disclosure and the press has disclosed it before we could issue a fix.

A time based scope is always included. Using consistent scopes or calendar based scopes improves everyone's ability to forecast comparable scenarios. "_Next Month_", "_Next Year_", "_Next Quarter_" are all typical.

### IT Management Scenarios 📠
Scenarios that are typically of concern to an IT organization.

- An employee's email has been accessed by an outsider.
- We have opened an incident to deal with a vendor compromise.
- Employee communications were compromised.
- Internal documentation has been exposed to, and indexed by, a search engine.
- Removable storage containing sensitive data has been lost.
- An employee laptop has been stolen and was not encrypted.
- A social engineer has received sensitive documents / data.
- An employee was not off-boarded correctly.

### Employee Scenarios 🧟
Scenarios that involve a "bad employee".

- An employee has decided to abuse their authorization.
- An employee is violating the social media policy.
- An employee is harming another employee.
- An employee has decided to violate security policy.
- An employee has harmed the organization with access retained after termination.

### AWS Risks ☁️
Scenarios typically involving cloud infrastructure.

- An IAM secret key has exposed to the internet.
- An S3 bucket has exposed to the internet.
- Security groups and ACL's have exposed a high risk server.
- An adversary has gained access to our AWS account.
- CloudTrail logs have been deleted or modified.

### Endpoint Risks 💻
Typical risks to desktops / laptops.

- An adversary has implanted malware on an endpoint.
- Endpoint malware is remotely beaconing to a C2.
- An adversary has moved laterally in the environment.
- An adversary has exploited unpatched software on an endpoint.
- An adversary has elevated privilege on an endpoint.

### Application Security Scenarios 📱🌐
Risks involving a product or application being developed by an organization.

- An adversary has remotely executed code through our application.
- An adversary has bypassed our rate limiting capability.
- An adversary has queried our database directly through our application.
- An adversary has exploited an indirect object reference vulnerability.
- An XSS vulnerability has been used against another user on our application.
- A research finding has gone outside of our disclosure process.
- Payment instruments are exposed to an adversary.
- Credentials are exposed to an adversary.

### Incident Response Scenarios 🚒
Meta-Incidents created by poor incident handling.

- An incident has sustained for more than two days.
- We are unable to discover root cause in an incident.
- We have not been able to comment publicly within our communications SLA.

### Physical Security Scenarios 🔫
Physical harm and physical loss.

- A celebrity employee is harassed in person
- An employee is involved in violence on company space (real estate or event)
- Company property over $X has been lost.
- An unauthorized individual has accessed our facility.
- An executive is threatened while traveling.
- An incident was not captured our cameras.

-->
