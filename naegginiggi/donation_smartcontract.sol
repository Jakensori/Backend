/// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract NaeggiDonation {
    // 초기 비즈니스 로직
    // safe remote purchase와 비슷
    // 기부자 측에서 캠페인 모금금고에 입금 시, 트랜젝션 발생 (기부자 포인트 차감 -> 나눔단체 계약서의 balance 증가) - donate 함수
    // 기부자, 나눔단체 사이에는 포인트로만 거래함
    // 1. 나눔단체는 캠페인에서 설정한 목표기부금액에 도달했을 때 abort 함수를 통해 출금 가능 (트랜젝션 발생)
    // 2. 누구든지 언제 누적기부금액 확인 가능 (check 함수)
    address payable public hlogName;
    uint public donationAmount;
    uint256 public current;

    event Finished();
    event Donation(uint val);

    constructor(address payable _hlogName, uint _donationAmount) payable {
        hlogName = _hlogName;
        donationAmount = _donationAmount;
        current = current + msg.value;
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
        require(address(this).balance <= current, "Donation amount is not reached.");
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
    }

    receive() external payable {
        require(msg.sender == tx.origin, "Donation amount does not match.");
    }
}