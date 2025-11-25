# mailchimp
repo for mailchip api extract and load

1) Airbyte extract and load. 

created folder in bucket

configured airbyte destination using the kms that we created for airbyte project. 
needed to reconfigure object-level permissions of the policy for the IAM user used. 
In simple terms, we edited the roots of the List, Get and Put actions.

2) Python extract and load

aws config:
create folder in bucket
update python IAM policy used previously for amplitude to include permissions to access new bucket folder

vscode:
create venv
install packages
pip freeze
commit to main

create dev branch
create .env





