# Application Insights
## Azure Log Analytics Workspace and Azure Application Insights resources are created.
![ai rg](submission-screenshots/application-insights/ai_rg.png)

## Application Insight Events that show the results of clicking vote for each Dogs & Cats
![events votes](submission-screenshots/application-insights/events_votes.png)

## The output of the traces query in Azure Log Analytics
![traces](submission-screenshots/application-insights/traces_votes_result.png)

## The chart created from the output of the traces query
![traces pie](submission-screenshots/application-insights/traces_votes_pie.png)


# Kubernetes Cluster
## The output of the Horizontal Pod Autoscaler, showing an increase in the number of pods
![aks autoscale](submission-screenshots/kubernetes-cluster/aks_autoscale.png)

## The Application Insights metrics which show the increase in the number of pods.
![aks ai](submission-screenshots/kubernetes-cluster/aks_insights.png)

## The alert I created.
![aks alert portal](submission-screenshots/kubernetes-cluster/aks_alert_portal.png)

## The email I received from the alert when the pod count increased.
![aks alert email](submission-screenshots/kubernetes-cluster/aks_alert_email.png)

# Autoscaling VMSS
Successful deployment via Azure Pipeline:
![vmss pipeline](submission-screenshots/autoscaling-vmss/vmss-autoscale-pipeline.png)

# Initial instance.
![vmss initial](submission-screenshots/autoscaling-vmss/vmss-autoscale-instance.png)

## The conditions for which autoscaling will be triggered (found in the 'Scaling' item in the VM Scale Set).
I used the 'Network Out Total' as the scaling metric.
![vmss settings](submission-screenshots/autoscaling-vmss/vmss-autoscale-settings.png)

## The Activity log of the VM scale set which shows that it scaled up with timestamp.
![vmss scaleup activitylog](submission-screenshots/autoscaling-vmss/vmss-autoscale-activitylog-scaleup.png)

## The new instances being created.
![vmss scaleup instances](submission-screenshots/autoscaling-vmss/vmss-autoscale-instances-scaleup.png)

## The metrics which show the load increasing, then decreasing once scaled up with timestamp.
![vmss metrics](submission-screenshots/autoscaling-vmss/vmss-autoscale-load.png)


# Runbook
I created a runbook that starts the VMSS. The alert gets triggered when the VMSS gets delocated.

## The alert configuration in Azure Monitor which shows the resource, condition, action group, and alert rule details.
![runbook alert1](submission-screenshots/runbook/runbook-alert-rule1.png)
![runbook alert2](submission-screenshots/runbook/runbook-alert-rule2.png)
![runbook alert3](submission-screenshots/runbook/runbook-alert-rule3.png)
![runbook alert4](submission-screenshots/runbook/runbook-alert-rule4.png)

## The email I received from the alert when the Runbook was executed.
![runbook email](submission-screenshots/runbook/runbook-alert-email.png)

## The summary of the alert which shows 'why did this alert fire?', timestamps, and the criterion in which it fired.
![runbook alert triggered](submission-screenshots/runbook/runbook-alert-triggered.png)
![runbook alert triggered2](submission-screenshots/runbook/runbook-alert-triggered2.png)

Runbook history with input and output:
![runbook job input](submission-screenshots/runbook/runbook-job-input.png)
![runbook job output](submission-screenshots/runbook/runbook-job-output.png)

VMSS activity log showing that the VMSS was stopped by me and started by the runbook:
![runbook activitylog](submission-screenshots/runbook/runbook-activitylog.png)