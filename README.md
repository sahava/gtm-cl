# gtm-cl
Google Tag Manager Command Line Tools

## gtm_permissions_to_csv.py

Generate CSV files that list all email addresses with access to the given account (or all accounts if no `-a` argument is given). 

**Usage**:

`python gtm_permissions_to_csv.py [-a accountId1,accountId2,accountId3] path_to_client_secrets`

The `-a` flag is optional. If you don't provide it, the tool will fetch permissions for all accounts you have access to. The flag takes a list of GTM accountIds, separated by a comma, as its value.

`path_to_client_secrets` is the path to where your Client Secrets JSON is stored.

Once run, the tool creates a directory `csv/` in the folder where you run the script, and populates this directory with CSV files that list all the email addresses with access to the GTM account.
