const forge = require("node-forge");

function encryptMessage(message, publicKey) {
  const key = forge.random.getBytesSync(32);
  const iv = forge.random.getBytesSync(16);

  const cipher = forge.cipher.createCipher("AES-CBC", key);
  cipher.start({ iv });
  cipher.update(forge.util.createBuffer(message));
  cipher.finish();
  const encrypted = cipher.output;

  return {
    encrypted: encrypted.getBytes(),
    key: publicKey.encrypt(key),
    iv: iv,
  };
}

function decryptMessage(message, privateKey) {
  const key = privateKey.decrypt(message.key);
  const { encrypted, iv } = message;

  const decipher = forge.cipher.createDecipher("AES-CBC", key);
  decipher.start({ iv });
  decipher.update(forge.util.createBuffer(encrypted));
  decipher.finish();

  const decrypted = decipher.output.toString();
  return decrypted;
}

module.exports = {
  encryptMessage,
  decryptMessage,
};
