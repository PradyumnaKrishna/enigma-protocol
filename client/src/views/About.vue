<template>
  <div class="container about w-50 mx-auto">
    <h1>This is an about page</h1>
    <br />
    <p>
      Hello Friends, I am trying to build an end to end encrypted messenger
      using Flask, SocketIO, and Vue.js. So, Here is my roadmap to achive it.
    </p>
  </div>

  <div class="container mx-auto w-50 text-start">
    <h4>Build a Person to Person Chat messenger</h4>
    <li>Generate Hash for each user, whoever opened the client using flask.</li>
    <li>Store that Hash into database and on client session.</li>
    <li>Connect other user using Hash.</li>
    <li>Create a 2 person session on frontend</li>
  </div>

  <div class="container mx-auto w-50 text-start">
    <h4>Add encryption to those messages</h4>
    <li>Create 2 SocketIO, one for send another for recieve.</li>
    <li>
      Encrypt Those messages using node-forge (nodejs crypto not working
      currently).
    </li>
    <li>
      While Creating 2 person session exchange the public keys of the users
    </li>
    <li>
      Encrypt using publicKey, decrypt using privateKey and these keys are going
      to store in frontend session.
    </li>
    <li>
      <strong>
        NOTE: If privateKey or user hash removed from the session then no one
        can restore those messages.
      </strong>
    </li>
  </div>

  <div class="container mx-auto w-50 text-start">
    <h4>DataBase Storing Facility</h4>
    <li>
      Store every message to the database (with session id that is going to be
      another Hash) while send and recieve messages.
    </li>
    <li>Session is removed after 15 min of last activity (initially)</li>
    <li>One button deletion of encrypted messages and user from database.</li>
    <li>
      <strong>
        NOTE: Only Recieved Messages can be decrypted, You can't decrypt sent
        messages because you have don't have privateKey for sent one.
      </strong>
    </li>
  </div>

  <div class="container mx-auto w-50 text-start">
    <h4>...</h4>
  </div>
</template>
