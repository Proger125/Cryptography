# Cryptography
## Lab_01
### Task:
* Implement a software tool that performs cryptanalysis of text encrypted by the Vigenère method. For cryptanalysis, use the Kasiski test.
* Conduct an experimental study of the dependence of the probability of a successful Kasiska attack on the length of the ciphertext. Build charts.
* Conduct an experimental study of the dependence of the probability of a successful Kasiska attack on the length of the keyword used in encryption. Build charts.
## Lab_02
### Task:
Write a "Protected Notepad" program that implements encryption, viewing, adding, updating and deleting of encrypted text files using the IDEA algorithm. 
Program has support of many users and password authentication. Also session key has expiration date.
Server part functionality:
* Stores text files.
* Generates random session key by client request.
* Sends encrypted with ECDSA public key session key to the client.
* Sends encrypted with session key text file to the client.
Client part functionality:
* Generates and sends ECDSA public key to the server.
* Sends request with filename to the server.
* Decrypts session key with ECDSA private key.
* Decrypts and shows text file with the session key.
* Stores ECDSA key
Man-in-the-middle functionality:
* Intercepts client-server requests
* Decrypts and shows text files
