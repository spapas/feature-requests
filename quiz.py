# This is for python 3
# Add the following dependency and run it with python quiz.py:
# cryptography==2.3.1

# it will output
# b'https://engineering-application.britecore.com/e/t6e118s10t/ImplementationEngineer'
from cryptography import fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABb4bQtDKu6jj-zlCnuGydCpxUX09tZH_nFbKKMQn6N3pSQhfoJ_2No6u9reCstnMIvAzFhQME7c-wq0NtAZg-12OemNqmLG6Kds1gch5h91sKAcsYcDgEvMSCGI2UHXbsHisWHUcxMeBkqIGxDbaNu9yuPrdGq5Hf_L2CjKqf0xzQt8u9_rWEcra6RWLHvtXRWGliY'

def main():
    f = fernet.Fernet(key)
    print(f.decrypt(message))


main()
