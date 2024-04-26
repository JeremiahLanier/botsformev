// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "./Utilities.sol";

contract Arbitrage {
    using SafeERC20 for IERC20;

    Utilities utilities;

    constructor(address _utilities) {
        utilities = Utilities(_utilities);
    }

    function simpleArbitrage(
        address token,
        uint256 buyAmount,
        address buyExchange,
        address sellExchange
    ) external {
        uint256 buyPrice = IExchange(buyExchange).getPrice(token);
        uint256 sellPrice = IExchange(sellExchange).getPrice(token);

        if (sellPrice > buyPrice) {
            IERC20(token).safeTransferFrom(msg.sender, address(this), buyAmount);
            IExchange(buyExchange).buy(token, buyAmount);
            uint256 boughtAmount = buyAmount * 10**18 / buyPrice; // Adjust for decimals
            IExchange(sellExchange).sell(token, boughtAmount);
        }
    }

    function triangularArbitrage(
        address tokenA,
        address tokenB,
        address tokenC,
        uint256 initialAmount,
        address exchange
    ) external {
        uint256 amountB = IExchange(exchange).swap(tokenA, tokenB, initialAmount);
        uint256 amountC = IExchange(exchange).swap(tokenB, tokenC, amountB);
        uint256 finalAmountA = IExchange(exchange).swap(tokenC, tokenA, amountC);

        if (finalAmountA > initialAmount) {
            uint256 profit = finalAmountA - initialAmount;
            IERC20(tokenA).safeTransfer(msg.sender, profit); // Send profit to initiator
        }
    }
}

interface IExchange {
    function getPrice(address token) external view returns (uint256);
    function buy(address token, uint256 amount) external;
    function sell(address token, uint256 amount) external;
    function swap(address tokenIn, address tokenOut, uint256 amount) external returns (uint256);
}

