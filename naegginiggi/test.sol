// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract test {
    // 초기 비즈니스 로직
    // 기부자 측에서 캠페인 모금금고에 입금 시, 트렌젝션 2번 발생 (기부자 포인트 차감, 나눔단체 포인트 증가)
    // 기부자, 나눔단체 사이에는 포인트로만 거래함 -> 우리(기부 중계 업체인 회사)는 포인트를 회수(redeem)할 때만 원화로 정산해주면 되는 것임. 
    address public hlogName;
    address public donator;
    uint public donation_amount;
    address public owner;

    event Donation(address donator, uint donation_amount);

    constructor () {
        owner = msg.sender;
    }

    function bid() public
}