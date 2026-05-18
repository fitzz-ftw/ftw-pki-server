Sequenz Diagramm Gesamt
========================


.. mermaid:: 
    :align: center

    sequenceDiagram

        participant CA as Root CA <br/> (Offline)
        participant S1 as Intermediate <br/> Level 1
        participant S2 as Intermediate <br/> Level 0
        %% participant C@{ "type" : "collections" } as Client <br/> Server <br/> Client-Server <br/> (End Entity)
        %% actor C as Client <br/> (End Entity)
        box green C Active
        actor C as Server <br/> (End Entity)
        end
        %% actor C as Client-Server <br/> (End Entity)
        participant U as User <br/> (End Entity)
        
        %%note over CA, S1, S2: ftwpkipassword programm
        par Setup CA and Intermediate CAs
            note over CA: ftwpkipassword <br/> programm
            CA->>CA: Generate Key Pair
            note over CA: ftwpkicaroot <BR/> programm
            CA->>CA: Generate CA Root Certificate (Self-Signed)
        and 
            note over S1: ftwpkipassword <br/> programm
            S1->>S1: Generate Intermediate Key Pair
        and
            note over S2: ftwpkipassword <br/> programm
            S2->>S2: Generate Intermediate Key Pair
        end
        par Create certificates requests
        note over S1: ftwpkiintermedcsr <br/> programm
        S1->>S1: Create Intermediate CSR 
        and
        note over S2: ftwpkiintermedcsr <br/> programm
        S2->>S2: Create Intermediate CSR
        end

        S1-->>CA: Request Intermediate Certificate
        note over CA: ftwpkicarootsigner <br/> programm
        CA->>CA: Sign Intermediate Certificate (Offline)
        CA-->>S1: Deliver Intermediate Certificate encrypted.
        %% destroy CA
        note over S1: ftwpkiunpacker <br/> programm
        S1->>S1: Decrypt Intermediate Certificate with Intermediate PrivKey
        S2->>S1: Request Intermediate Certificate
        note over S1: ftwpkiintermedsigner <br/> programm
        S1->>S1: Sign Intermediate Certificate for S2
        S1->>S2: Deliver Intermediate Certificate encrypted.
        note over S2: ftwpkiunpacker <br/> programm
        S2->>S2: Decrypt Intermediate Certificate with Intermediate PrivKey   

        %% create participant C as Client (End Entity)
        
        activate C
        C->>C: Generate Key Pair (unencrypted) and CSR
        C->>S2: Request End Entity Certificate
        deactivate C

        activate S2
        S2->>S2: Sign End Entity Certificate
        note over S2: ftwpkiintermedsigner <br/> programm
        S2->>C: Deliver End Entity Certificate encrypted.
        deactivate S2

        activate C
        note over C: ftwpkiunpacker <br/> programm
        C->>C: Decrypt End Entity Certificate with End Entity PrivKey
        deactivate C

        %% create participant U as User (End Entity)
        
        activate U
        U->>U: Generate Key Pair (encrypted)
        U->>U:  Generate CSR
        U->>S2: Request End Entity Certificate
        deactivate U
        activate S2
        S2->>S2: Sign End Entity Certificate
        S2->>U: Deliver End Entity Certificate encrypted.
        deactivate S2
        activate U
        note over U: ftwpkiunpacker <br/> programm
        U->>U: Decrypt End Entity Certificate with End Entity PrivKey
        deactivate U
    

.. mermaid:: 
    :align: center

    sequenceDiagram
        participant S2 as Intermediate <br/> Level 0
        %% participant C@{ "type" : "collections" } as Client <br/> Server <br/> Client-Server <br/> (End Entity)
        %% actor C as Client <br/> (End Entity)
        box green  Active
        actor C as Server <br/> (End Entity)
        end
        %% actor C as Client-Server <br/> (End Entity)
        note right of C: ftwpkiservercsr <br/> programm
        activate C
        C->>C: Generate Key Pair <br/> (unencrypted) <br/> and<br/> CSR
        C->>S2: Request End Entity Certificate
        deactivate C

        activate S2
        S2->>S2: Sign End Entity Certificate
        %%note over S2: ftwpkiintermedsigner <br/> programm
        S2->>C: Deliver End Entity Certificate encrypted.
        deactivate S2

        activate C
        note over C: ftwpkiunpacker <br/> programm
        C->>C: Decrypt End Entity Certificate with End Entity PrivKey
        deactivate C

