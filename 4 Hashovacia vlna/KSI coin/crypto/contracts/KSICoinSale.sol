import "./KSICoin.sol";

// THIS FILE IS ONLY FOR CREATING A TEST TOKENS SALE ON LOCAL PLATFORM AND IS NOT RELEVANT FOR THE TASK 

contract KSICoinSale {
    address public admin;
    KSICoin public tokenContract;
    uint256 public tokenPrice;
    uint256 public tokensSold;

    event Sell(address _buyer, uint256 _amount);

    constructor(KSICoin _tokenContract, uint256 _tokenPrice) public {
        admin = msg.sender;
        tokenContract = _tokenContract;
        tokenPrice = _tokenPrice;
    }

    function multiply(uint x, uint y) internal pure returns (uint z) {
        require(y == 0 || (z = x * y) / y == x);
    }

    function buyTokens(uint256 _numberOfTokens) public payable {
        require(msg.value == multiply(_numberOfTokens, tokenPrice));
        require(tokenContract.balanceOf(admin) >= _numberOfTokens);
        require(tokenContract.transferFrom(admin, msg.sender, _numberOfTokens));

        tokensSold += _numberOfTokens;

        emit Sell(msg.sender, _numberOfTokens);
    }

    function endSale() public {
        require(msg.sender == admin);
        // require(tokenContract.transfer(admin, tokenContract.balanceOf(admin)));
    }
}
