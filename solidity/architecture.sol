// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;


// storage contract
contract param_storage {

    struct map {
        uint a;
        uint b;
    }

    mapping(address => map) public parameters;

    address public immutable deployer;

    // addresses of contracts
    address public coreAddr;
    address public peripheryAddr;

    modifier onlyTrusted {
        address sender = msg.sender;
        require(sender == coreAddr || sender == peripheryAddr, "not trusted");
        _;
    }

    modifier onlyDeployer {
        address sender = msg.sender;
        require(sender == deployer, "not deployer");
        _;
    }

    constructor () {
        deployer = msg.sender;
    }

    function setAddresses(address _core, address _periphery) public onlyDeployer {
        coreAddr = _core;
        peripheryAddr = _periphery;
    }

    function setParams(address account, uint a, uint b) public onlyTrusted {
        parameters[account].a = a;
        parameters[account].b = b;
    }
}

// core contract
contract core {
    param_storage public storageContract;
    periphery public peripheryContract;

    address public immutable deployer;

    modifier onlyDeployer {
        address sender = msg.sender;
        require(sender == deployer, "not deployer");
        _;
    }

    constructor () {
        deployer = msg.sender;
    }

    function setStorageAddr(param_storage _storage) public onlyDeployer {
        storageContract = _storage;
    }

    function setPeripheryAddr(periphery _periphery) public onlyDeployer {
        peripheryContract = _periphery;
    }

    function calculateUsingPeriphery(uint a, uint b) public {
        peripheryContract.addParams(a, b);
    }

}

// periphery contract
contract periphery {

    param_storage public storageContract;
    core public coreContract;

    address public immutable deployer;

    modifier onlyDeployer {
        address sender = msg.sender;
        require(sender == deployer, "not deployer");
        _;
    }

    modifier onlyCore {
        address sender = msg.sender;
        require(sender == address(coreContract), "not core");
        _;
    }

    constructor () {
        deployer = msg.sender;
    }

    function setStorageAddr(param_storage _storage) public onlyDeployer{
        storageContract = _storage;
    }

    function setCoreAddr(core _core) public onlyDeployer {
        coreContract = _core;
    }

    function calculateParams(uint a, uint b) internal pure returns (uint,uint) {
        uint c = a + 1;
        uint d = b + 2;

        return(c,d);
    }

    function writeParams(uint a, uint b) internal returns(uint,uint) {
        storageContract.setParams(tx.origin, a, b);

        return (a,b);
    }

    function addParams(uint a, uint b) public onlyCore returns(uint,uint) {
        (a,b) = calculateParams(a, b);
        writeParams(a, b);
        
        return (a,b);
    }

}
