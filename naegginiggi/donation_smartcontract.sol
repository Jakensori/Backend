/// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract NaeggiDonation {
    address payable public hlogName;
    uint public donationAmount;
    uint256 public current;

    event Finished();
    event Donation(uint val);

    constructor(address payable _hlogName, uint _donationAmount) payable {
        hlogName = _hlogName;
        donationAmount = _donationAmount;
        current = 0;
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
    {
        require(address(this).balance <= donationAmount, "Donation amount is not reached.");
        emit Finished();
        payable(hlogName).transfer(address(this).balance);
    }
    
    function check() public view returns (uint256){
        return current;
    }

    function donate()
        public
        onlyDonator
        payable 
    {
        emit Donation(msg.value);
        current = current + msg.value;
        payable(msg.sender).transfer(msg.value);
    }

    receive() external payable {
        require(msg.sender == tx.origin, "Donation amount does not match.");
    }
}