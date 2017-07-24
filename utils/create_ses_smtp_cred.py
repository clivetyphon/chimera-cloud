import hmac
import hashlib
import base64
import sys


def get_args():
    """
    get AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    from terminal arguments
    return tuple
    
    """
    if len(sys.argv) < 2:
        print('Not enough arguments')
        return (None, None)
    elif len(sys.argv) == 2:
        AWS_ACCESS_KEY_ID = None
        AWS_SECRET_ACCESS_KEY = sys.argv[1]
    elif len(sys.argv) == 3:
        AWS_ACCESS_KEY_ID = sys.argv[1]
        AWS_SECRET_ACCESS_KEY = sys.argv[2]
    else:
        print('Too many arguments')
        return (None, None)
    
    return (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)



class IAM_user(object):

    def __init__(self, keystore):
        """
        this class is intended to model an IAM user.

        so far, it just takes an IAM user SecretAccessKey and hashes it into an SMTP server password
        """
        self.secret_access_key = keystore[1]
        self.smtp_password = None

    def set_secret_access_key(self, SecretAccessKey):
        self.secret_access_key = SecretAccessKey

    def hash_smtp_password(self):

        # only hash if SecretAccessKey has been set
        if self.secret_access_key is None:
            print("Failed: No Secret Access Key, use set_secret_access_key()")

        else:

            # http://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html

            # pseudocode:
            # message = "SendRawEmail";
            # versionInBytes = 0x02;
            # signatureInBytes = HmacSha256(message, key);
            # signatureAndVer = Concatenate(versionInBytes, signatureInBytes);
            # smtpPassword = Base64(signatureAndVer);

            #private static final String KEY = "AWS SECRET ACCESS KEY";
            AWS_SECRET_ACCESS_KEY = self.secret_access_key

            # private static final String MESSAGE = "SendRawEmail";
            AWS_MESSAGE = "SendRawEmail"
            #in Python 2, str are bytes
            signature = hmac.new(
                key=AWS_SECRET_ACCESS_KEY.encode('utf-8'),
                #byte[] rawSignature = mac.doFinal(MESSAGE.getBytes());
                msg=AWS_MESSAGE.encode('utf-8'),
                digestmod=hashlib.sha256
            ).digest()

            # Prepend the version number to the signature.
            signature = chr(2).encode('utf-8') + signature

            # To get the final SMTP password, convert the HMAC signature to base 64.
            signature = base64.b64encode(signature)

            self.smtp_password = signature

if __name__ == '__main__':
	
	keystore = get_args()

	iam_user = IAM_user(keystore)
	iam_user.hash_smtp_password()
	print(iam_user.smtp_password)
	
