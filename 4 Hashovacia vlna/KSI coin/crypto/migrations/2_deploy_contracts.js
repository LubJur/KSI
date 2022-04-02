var KSICoin = artifacts.require("./KSICoin.sol");
var KSICoinSale = artifacts.require("./KSICoinSale.sol");

module.exports = function(deployer) {
  deployer.deploy(KSICoin, 1000000).then(function() {
    // Token price is 0.001 Ether
    var tokenPrice = 1000000000000000;
    return deployer.deploy(KSICoinSale, KSICoin.address, tokenPrice);
  });
};