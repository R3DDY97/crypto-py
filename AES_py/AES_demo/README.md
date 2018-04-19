
### **Advanced Encryption Standard (AES)** ==  **_Rijndael_**

 1. AES is a symmetric block cipher chosen by the U.S. government to protect classified information to encrypt sensitive data.


2. It is based on `substitution–permutation network`


3. AES performs its computations on bytes and 

arranges the 128 bits of a plaintext block as 16 bytes in 4x4 matrix

----------------------------------------------------------------------
----------------------------------------------------------------------
----------------------------------------------------------------------

#### **_AES algorithm_**:-


![AES STRUCTURE](https://raw.githubusercontent.com/R3DDY97/crypto-py/master/AES_py/pics/aes_en_de.png)

***AES encryption involves four transformations :***

1. Sub Bytes
2. Shift Rows
3. Mix Columns
3. Add Round key


----------------------------------------------------------------------
1. **SubBytes**

*Input from plain text*

![AES state](https://raw.githubusercontent.com/R3DDY97/crypto-py/master/AES_py/pics/state.jpg) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ![AES sub](https://raw.githubusercontent.com/R3DDY97/crypto-py/master/AES_py/pics/state_sbox.jpg)


![AES SubBytes](https://raw.githubusercontent.com/R3DDY97/crypto-py/master/AES_py/pics/AES-SubBytes.svg?sanitize=true)


![AES sbox](https://raw.githubusercontent.com/R3DDY97/crypto-py/master/AES_py/pics/aes_sbox.jpg)



----------------------------------------------------------------------



----------------------------------------------------------------------
2. **ShiftRows**

![AES ShiftRows](https://raw.githubusercontent.com/R3DDY97/crypto-py/master/AES_py/pics/AES-ShiftRows.svg?sanitize=true)
----------------------------------------------------------------------


----------------------------------------------------------------------
3. **MixColumns**


![AES ShiftRows](https://raw.githubusercontent.com/R3DDY97/crypto-py/master/AES_py/pics/AES-MixColumns.svg?sanitize=true)

*Matrix used in MixColumns* &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *Round Constant*

![AES matrix](https://raw.githubusercontent.com/R3DDY97/crypto-py/master/AES_py/pics/matrix.svg?sanitize=true)   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ![AES matrix](https://raw.githubusercontent.com/R3DDY97/crypto-py/master/AES_py/pics/rcon.jpg)
----------------------------------------------------------------------

----------------------------------------------------------------------
4. **AddRoundKey**

![AES AddRoundKey](https://raw.githubusercontent.com/R3DDY97/crypto-py/master/AES_py/pics/AES-AddRoundKey.svg?sanitize=true)

----------------------------------------------------------------------











