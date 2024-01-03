SITUATION:
The client's AWS Autoscaling group constantly scales up and down depending on workloads. It is configured so that EBS volumes from terminated instances remain for possible troubleshooting.

Within a few months, the client's account had accumulated a significant number of EBS volumes, resulting in a steep increase in bills.

TASK:
We need a solution where detached volumes are retained for less than 5 days, and the rest are permanently deleted. This check must be performed daily.

SOLUTION:
1. Set up EventBridge to trigger a Lambda function with a Python script.
2. Create an IAM Role with permissions to check and delete EBS volumes, then assign this Role to the Lambda function.