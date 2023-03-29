// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract NaeggiDonation {
    // 초기 비즈니스 로직
    // safe remote purchase와 비슷
    // 기부자 측에서 캠페인 모금금고에 입금 시, 트렌젝션 2번 발생 (기부자 포인트 차감, 나눔단체 포인트 증가)
    // 기부자, 나눔단체 사이에는 포인트로만 거래함 -> 우리(기부 중계 업체인 회사)는 포인트를 회수(redeem)할 때만 원화로 정산해주면 되는 것임. 
    address payable public hlogName;
    address public donator;
    uint public donation_amount;
    enum State { Created, Locked, Inactive }
    State public state;

    constructor() payable {
        donator = msg.sender;
        donation_amount = msg.value;
    }

    event Finished();
    event Donation();
    event DonationReceived();

    modifier onlyDonator() {
        require(msg.sender == donator);
        _;
    }
    modifier onlyFoundation() {
        require(msg.sender == hlogName);
        _;
    }
    modifier inState(State _state) {
        require(state == _state);
        _;
    }

    /// 구매를 중단하고 이더를 회수합니다.
    /// 콘트렉트가 잠기기 전에 판매자에 의해서만
    /// 호출 되어 질 수 있습니다.
    function abort()
        public
        onlyDonator
        inState(State.Created)
    {
        emit Finished();
        state = State.Inactive;
    }

    /// 구매자로서 구매를 확정합니다.
    /// 이 이더는 confirmReceived()가 호출 될때까지
    /// 잠길것입니다.
    function donate()
        public
        inState(State.Created)
        payable 
    {
        emit Donation();
        donator = msg.sender;
        state = State.Locked;
    }

    /// 구매자가 아이템을 받았다고 확인.
    /// 이것은 잠긴 이더를 풀어줄것입니다.
    function confirmReceived()
        public
        onlyFoundation
        inState(State.Locked)
    {
        emit DonationReceived();
        // It is important to change the state first because
        // otherwise, the contracts called using `send` below
        // can call in again here.
        // 먼저 상태를 변경하는 것이 중요합니다.
        // 그렇지 않으면, `send`를 사용하며 호출된 콘트렉트는
        // 다시 여기를 호출할 수 있기 때문입니다.
        state = State.Inactive;

        // NOTE: 이것은 실제로 구매자와 판매자 둘다 환급 하는 것을 막을 수
        // 있도록 합니다. - 출금 패턴이 사용되어야만 합니다.

        hlogName.transfer(donation_amount);
    }

}