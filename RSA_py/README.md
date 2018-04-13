##  RSA Encryption 
========================
     
   Implements RSA 2048 bit - asymmetric key cryptography in python2

   Intended to understand and experiment on encryption methods, not for real use cases 

### Requirements:-
 - python-sympy   -- to generate random 1024 bit prime numbers
 - sage  -- to do power_mod on big primes 


### Usage:-

 -  Install sage in linux using official repos and python-sympy using pip 

 - **`generate_keys.rsa_keys`** will returns and also saves public and private keys 
    in local folder

 - **`encryption.encrypt_message`** takes message and public_key  and returns cipher_text

 - **`decryption.decrypt_message`** takes cipher_text and private_key  and returns message




##### To do:-
 - *Remove* sympy and sage dependency 
    * Use **CRT / fast exponentiation** to do power mod 
    * Generate Random prime 
 - Implement OAEP (Optimal asymmetric encryption padding)
 - Represent keys and cipher_text in pgp standard 

