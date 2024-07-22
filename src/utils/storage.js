function getKeypair() {
  // load key from localStorage
  const _keypair = localStorage.getItem('keypair')

  if (_keypair) {
    const keypair = JSON.parse(_keypair)
    return keypair
  }

  return null
}

function setKeypair(keypair) {
  // save key to localStorage
  localStorage.setItem('keypair', JSON.stringify(keypair))
}

export default {
  getKeypair,
  setKeypair,
}
