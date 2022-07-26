// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

/// @title Delegatecall test
/// @dev deploy contract B first, then deploy contract C
/// This is to avoid the anoyance of the 24kb limit
/// Question, is this architecture secure?

contract A {
    uint public a;
    uint public b;
    address public DAI;
    address public USD;
}

contract B is A {

    function getNum() public view returns (uint) {
        return A.a;
    }

    function setA(uint _num) public returns (uint) {
        a = _num;
        return a;
    }

    function setB(uint _num) public returns (uint) {
        b = _num;
        return b;
    }

    function setDAI(address _address) public returns (address) {
        DAI = _address;
        return DAI;
    }

    function setUSD(address _address) public returns (address) {
        USD = _address;
        return USD;
    }
}

contract C is A {

    address public contractB;

    constructor (address _B) {
        contractB = _B;
    }

    function setA(uint _num) public returns (uint) {
        // A's storage is set, B is not modified.
        bytes memory data = abi.encodeWithSignature("setA(uint256)", _num);
        (bool success, bytes memory returnData) = contractB.delegatecall(data);
        require(success);
        return abi.decode(returnData, (uint));
    }

    function setB(uint _num) public returns (uint) {
        // A's storage is set, B is not modified.
        bytes memory data = abi.encodeWithSignature("setB(uint256)", _num);
        (bool success, bytes memory returnData) = contractB.delegatecall(data);
        require(success);
        return abi.decode(returnData, (uint));
    }

    function setDAI(address _address) public returns (uint) {
        // A's storage is set, B is not modified.
        bytes memory data = abi.encodeWithSignature("setDAI(address)", _address);
        (bool success, bytes memory returnData) = contractB.delegatecall(data);
        require(success);
        return abi.decode(returnData, (uint));
    }

    function setUSD(address _address) public returns (uint) {
        // A's storage is set, B is not modified.
        bytes memory data = abi.encodeWithSignature("setUSD(address)", _address);
        (bool success, bytes memory returnData) = contractB.delegatecall(data);
        require(success);
        return abi.decode(returnData, (uint));
    }
}
