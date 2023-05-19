/// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract NaeggiDonation {
    address payable public hlogName;
    uint public donationAmount;

    event Finished();
    event Donation(uint val);

    constructor(address payable _hlogName, uint _donationAmount) payable {
        hlogName = _hlogName;
        donationAmount = _donationAmount;
    }

    modifier onlyDonator() {
        require(msg.sender == tx.origin);
        require(msg.sender != hlogName, "Access denied.");
        _;
    }
    modifier onlyFoundation() {
        require(msg.sender == hlogName, "Access denied.");
        _;
    }

    function abort()
        public
        onlyFoundation
    {
        require(address(this).balance >= donationAmount, "Donation amount is not reached.");
        emit Finished();
        payable (address(msg.sender)).transfer(address(this).balance);
    }
    
    function check() public view returns (uint256){
        return address(this).balance;
    }

    function donate()
        public
        onlyDonator
        payable 
    {
        emit Donation(msg.value);
    }

    
    // 계약으로 직접 이더를 전송
    function transferEtherToContract() external payable {
    }

}