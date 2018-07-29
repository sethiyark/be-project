import ast

from Crypto.PublicKey import RSA

'''
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)  # generate pub and priv key

public_key = private_key.publickey()  # pub key export for exchange


privkey = private_key.exportKey(format='DER')
pubkey = public_key.exportKey(format='DER')

prv_file = open("private.pem", "w")
prv_file.write(privkey)
prv_file.close()
pub_file = open("public.pem", "w")
pub_file.write(pubkey)
pub_file.close()

'''
prv_file = open("private.pem", "r")
privkey = prv_file.read()
prv_file.close()
pub_file = open("public.pem", "r")
pubkey = pub_file.read()
pub_file.close()
private_key = RSA.importKey(privkey)
public_key = RSA.importKey(pubkey)

encrypted = public_key.encrypt('encrypt this message', 32)
# message to encrypt is in the above line 'encrypt this message'

print
'encrypted message:', encrypted  # ciphertext
f = open('encryption.txt', 'w')
f.write(str(encrypted))  # write ciphertext to file
f.close()

# decrypted code below

f = open('encryption.txt', 'r')
message = f.read()

decrypted = private_key.decrypt(ast.literal_eval(str(message)))

print
'decrypted', decrypted

# f = open ('encryption.txt', 'w')
# f.write(str(message))
# f.write(str(decrypted))
f.close()
