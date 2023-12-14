# Client_Server_SQL

Simple Client-Server API with database support and multi-threading.

The application allows you to register, log in, check the list of users, send messages between users, and check your inbox etc.

An own connection pool was created for the application, which assumes:
- at the start, the application creates 3 connections so that they are ready whenever they are needed
- controls the connection limit. can maintain a maximum of 100 connections to the database,
- regularly checks for inactive connections above the initial limit and deletes them
- connections with an error are destroyed

Requirements: 
- dotenv
- psycopg2
- standards modules (threading, socket, queue, os, json, time, multiprocessing)

Link to a video of the application in action: https://www.youtube.com/watch?v=lrm_iI2eZxw
Link to a video with stress test of application: https://www.youtube.com/watch?v=pbvuNGZbpfs
