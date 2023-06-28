const CryptoJS = require("crypto-js");

function encrypt(message, key) {
  return CryptoJS.AES.encrypt(message, key).toString();
}

function decrypt(ciphertext, key) {
  const bytes  = CryptoJS.AES.decrypt(ciphertext, key);
  return bytes.toString(CryptoJS.enc.Utf8);
}

module.exports = {
  encrypt,
  decrypt,
}

