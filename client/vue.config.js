const REQUIRED_ENV_VARS = [
  'VUE_APP_APIURL',
]
  
if (REQUIRED_ENV_VARS.some(env => typeof process.env[env] === 'undefined')) {
  throw new Error('Required environment variables are missing')
}

module.exports = {
  publicPath: ''
};