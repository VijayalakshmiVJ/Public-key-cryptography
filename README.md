# Public-key-cryptography
Client Server application (TCP) where message exchange is done using Public key (Asymmetric) cryptography.

**Requirement** <br />

• Server --- sends ---> encrypted message "Hi, who is this?" using clients public key.
 
• Client -- responds -> encrypted message "Hi, this is ID!" using servers public key.
 
**Bonus** <br />
Added further communication between server and client with sleeps/delays introduced randomly.

• Server --- sends ---> encrypted message "Its me Server, sending further random message -> Blah!" using clients public key.

• Client -- responds -> encrypted message "Here's my client random message -> Blah!" using servers public key.

• Server --- sends ---> encrypted message "Its me Server, sending further random message -> Blah!" using clients public key.

• Client -- responds -> encrypted message "Just receiving random messages from server, Exiting..." using servers public key.

• Client exits

• Server exits
