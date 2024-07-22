import forge, { util } from 'node-forge'

function encryptMessage(message, publicKey) {
  const key = forge.random.getBytesSync(32)
  const iv = forge.random.getBytesSync(16)

  const cipher = forge.cipher.createCipher('AES-CBC', key)
  cipher.start({ iv })
  cipher.update(util.createBuffer(message))
  cipher.finish()

  return btoa(
    JSON.stringify({
      encrypted: cipher.output.getBytes(),
      key: publicKey.encrypt(key),
      iv: iv,
    }),
  )
}

function decryptMessage(message, privateKey) {
  message = JSON.parse(atob(message))
  const key = privateKey.decrypt(message.key)
  const { encrypted, iv } = message

  const decipher = forge.cipher.createDecipher('AES-CBC', key)
  decipher.start({ iv })
  decipher.update(util.createBuffer(encrypted))
  decipher.finish()

  return decipher.output.toString()
}

function generateKeypair() {
  const keypair = forge.pki.rsa.generateKeyPair({ bits: 2048, workers: 2 })
  return {
    publicKey: btoa(forge.pki.publicKeyToPem(keypair.publicKey)),
    privateKey: btoa(forge.pki.privateKeyToPem(keypair.privateKey)),
  }
}

function publicKeyFromBase64(key) {
  let publicKey = atob(key, 'base64')
  publicKey = forge.pki.publicKeyFromPem(publicKey)

  return publicKey
}

function privateKeyFromBase64(key) {
  let privateKey = atob(key, 'base64')
  privateKey = forge.pki.privateKeyFromPem(privateKey)

  return privateKey
}

export default {
  encryptMessage,
  decryptMessage,
  generateKeypair,
  publicKeyFromBase64,
  privateKeyFromBase64,
}
