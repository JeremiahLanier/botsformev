// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Utilities {
    function checkGreaterThan(uint256 _a, uint256 _b) external pure returns (bool) {
        return _a > _b;
    }

    // Example of a utility function to convert token amounts
    function convertAmount(
        uint256 _amount,
        uint256 _fromDecimals,
        uint256 _toDecimals
    ) external pure returns (uint256) {
        if (_fromDecimals > _toDecimals) {
            return _amount / (10**(_fromDecimals - _toDecimals));
        } else if (_fromDecimals < _toDecimals) {
            return _amount * (10**(_toDecimals - _fromDecimals));
        }
        return _amount;
    }
}

