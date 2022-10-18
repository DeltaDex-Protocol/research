import {
  calculateFee,
  getLiquidityForAmounts,
  getSqrtPriceX96,
  getTickFromPrice,
  getPriceFromTick,
  getTokenAmountsFromDepositAmounts,
} from './liquidityMath'
import bn from 'bignumber.js'
import { getPoolTicks, getVolume24H, getUniStats } from './uniswap'
import { getFeeTierPercentage } from './helper'

const calculateLiquidity = (ticks: any, currentTick: number): bn => {
  if (ticks.length <= 1) return new bn(0)
  let liquidity: bn = new bn(0)
  for (let i = 0; i < ticks.length - 1; ++i) {
    liquidity = liquidity.plus(new bn(ticks[i].liquidityNet))

    let lowerTick = Number(ticks[i].tickIdx)
    let upperTick = Number(ticks[i + 1].tickIdx)

    if (lowerTick <= currentTick && currentTick <= upperTick) {
      break
    }
  }

  return liquidity
}

type EstimateFeesQueryType = {
  pool: string
  deposit: number
  token0_decimals?: string
  token1_decimals?: string
  //   volume24HNotAveraged?: boolean
  priceRange: [number, number]
  initialPrice: number
  period?: number
}

const estimateFees24H = async (feesQuery: EstimateFeesQueryType) => {
  const feeTier = '3000'
  const DEFAULT_AVG = 7 // days
  const state = {
    isSwap: false,
    pool: feesQuery.pool,
    poolTicks: await getPoolTicks(feesQuery.pool),
    token0: { decimals: feesQuery.token0_decimals || '18' },
    token1: { decimals: feesQuery.token1_decimals || '18' },
    volume24H: await getVolume24H(
      feesQuery.pool,
      feesQuery?.period || DEFAULT_AVG,
    ),
    depositAmountValue: feesQuery.deposit,
    priceRangeValue: feesQuery.priceRange,
    priceAssumptionValue: feesQuery.initialPrice, /// idk
  }

  const P = state.priceAssumptionValue
  const Pl = state.priceRangeValue[0]
  const Pu = state.priceRangeValue[1]
  const priceUSDX = feesQuery.initialPrice
  const priceUSDY = 1
  const targetAmounts = state.depositAmountValue

  const { amount0, amount1 } = getTokenAmountsFromDepositAmounts(
    P,
    Pl,
    Pu,
    priceUSDX,
    priceUSDY,
    targetAmounts,
  )

  const sqrtRatioX96 = getSqrtPriceX96(
    P,
    state.token0?.decimals || '18',
    state.token1?.decimals || '18',
  )
  const sqrtRatioAX96 = getSqrtPriceX96(
    Pl,
    state.token0?.decimals || '18',
    state.token1?.decimals || '18',
  )
  const sqrtRatioBX96 = getSqrtPriceX96(
    Pu,
    state.token0?.decimals || '18',
    state.token1?.decimals || '18',
  )

  const deltaL = getLiquidityForAmounts(
    sqrtRatioX96,
    sqrtRatioAX96,
    sqrtRatioBX96,
    amount0,
    Number(state.token1?.decimals || 18),
    amount1,
    Number(state.token0?.decimals || 18),
  )

  let currentTick = getTickFromPrice(
    P,
    state.token0?.decimals || '18',
    state.token1?.decimals || '18',
  )

  if (state.isSwap) currentTick = -currentTick

  const L = calculateLiquidity(state.poolTicks || [], currentTick)
  const volume24H = state.volume24H

  let fee = calculateFee(deltaL, L, volume24H, feeTier)
  if (P < Pl || P > Pu) fee = 0

  let liquidity_percentage = fee / volume24H / getFeeTierPercentage(feeTier)
  //@ts-ignore
  return {
    liquidity_percentage: liquidity_percentage,
    averageVolume24H: volume24H,
    collectedFees24H: fee,
  }
}

estimateFees24H({
  pool: '0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8',
  deposit: 1000,
  token0_decimals: '6',
  token1_decimals: '18',
  priceRange: [1215, 1395],
  initialPrice: 1312,
  period: 100,
}).then((res) => console.log(res))
