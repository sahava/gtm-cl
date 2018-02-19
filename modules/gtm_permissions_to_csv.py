import sys
import auth
import argparse
import os
import csv
import re


def get_accounts(service, accounts):
    print('Fetching account details...')
    account_list_from_api = service.accounts().list(fields='account(accountId,name)').execute()

    if accounts == 'all':
        return account_list_from_api.get('account', [])

    accounts_as_list = accounts.split(',')

    def check_if_account_in_args(account):
        return account['accountId'] in accounts_as_list

    return list(filter(check_if_account_in_args, account_list_from_api.get('account', [])))


def get_permissions(service, aid):
    permissions = service.accounts().user_permissions().list(parent='accounts/%s' % aid, fields='userPermission(emailAddress)').execute()
    return permissions.get('userPermission')


def get_valid_filename(s):
    """
    Adapted from https://github.com/django/django/blob/master/django/utils/text.py
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s).lower()


def build_csv(permissions, account):
    with open('csv/%s_%s.csv' % (get_valid_filename(account['name']), account['accountId']), 'wb') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(['Account name', account['name']])
        wr.writerow(['Account ID', account['accountId']])
        wr.writerow([])
        for permission in permissions:
            wr.writerow([permission['emailAddress']])


def main(argv):
    scope = ['https://www.googleapis.com/auth/tagmanager.readonly',
             'https://www.googleapis.com/auth/tagmanager.manage.users']

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--accounts', default='all', metavar='accounts', help='comma-separated list of account IDs to pull permissions for')
    parser.add_argument('path_to_client_secrets', help='path to your client_secrets file')
    args = parser.parse_args()

    accounts = args.accounts
    client_secrets_path = args.path_to_client_secrets

    service = auth.auth('tagmanager', 'v2', scope, client_secrets_path)

    account_list = get_accounts(service, accounts)

    if len(account_list) == 0:
        if accounts == 'all':
            print('Your Google ID doesn\'t have access to any GTM accounts!')
        else:
            print('You don\'t have permissions to access any of the accountIds you listed in the arguments!')

    for account in account_list:
        print('\nFetching permissions for account "%s" (%s)...' % (account['name'], account['accountId']))
        permissions = get_permissions(service, account['accountId'])
        print('Building "csv/%s_%s.csv"...' % (get_valid_filename(account['name']), account['accountId']))
        if not os.path.exists('csv'):
            os.makedirs('csv')
        build_csv(permissions, account)


if __name__ == '__main__':
    main(sys.argv[1:])
