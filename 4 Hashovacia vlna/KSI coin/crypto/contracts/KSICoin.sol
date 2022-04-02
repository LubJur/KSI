
contract KSICoin {
    string  public name;
    string  public symbol;
    string  public standard;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    // add cutom variables if needed


    // DO NOT REMOVE/CHANGE THIS EVENTS DEFINITION 
    event Transfer(
        address indexed _from,
        address indexed _to,
        uint256 _value
    );

    event Approval(
        address indexed _owner,
        address indexed _spender,
        uint256 _value
    );


    constructor (uint256 _initialSupply) public {
        // TODO initialize contract
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        // TODO transfer
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        // TODO approve
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        // TODO transfer from
    }

    // add more functions if needed
}
