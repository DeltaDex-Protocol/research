import axios from 'axios'
import { number } from 'echarts'
// const {axios} = require('axios')
// import { Network, NETWORKS } from "../common/types";
// import { getTokenLogoURL, sortToken } from "../utils/helper";
// import lscache from "../utils/lscache";

// export let currentNetwork = NETWORKS[0];

// export const updateNetwork = (network: Network) => {
//   currentNetwork = network;
// };

export interface Tick {
  tickIdx: string
  liquidityNet: string
  price0: string
  price1: string
}

const _getPoolTicksByPage = async (
  poolAddress: string,
  page: number,
): Promise<Tick[]> => {
  const res = await queryUniswap(`{
    ticks(first: 1000, skip: ${
      page * 1000
    }, where: { poolAddress: "${poolAddress}" }, orderBy: tickIdx) {
      tickIdx
      liquidityNet
      price0
      price1
    }
  }`)

  return res.ticks
}

export const getPoolTicks = async (poolAddress: string): Promise<Tick[]> => {
  const PAGE_SIZE = 3
  let result: Tick[] = []
  let page = 0
  while (true) {
    const [pool1, pool2, pool3] = await Promise.all([
      _getPoolTicksByPage(poolAddress, page),
      _getPoolTicksByPage(poolAddress, page + 1),
      _getPoolTicksByPage(poolAddress, page + 2),
    ])

    result = [...result, ...pool1, ...pool2, ...pool3]
    if (pool1.length === 0 || pool2.length === 0 || pool3.length === 0) {
      break
    }
    page += PAGE_SIZE
  }
  return result
}

export const queryUniswap = async (query: string): Promise<any> => {
  const { data } = await axios({
    url: 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3',
    method: 'post',
    data: {
      query,
    },
  })

  return data.data
}

export const getVolume24H = async (
  poolAddress: string,
  amount: number = 1,
): Promise<number> => {
  const { poolDayDatas } = await queryUniswap(`{
    poolDayDatas(skip: 1, first: ${amount}, orderBy: date, orderDirection: desc, where:{pool: "${poolAddress}"}) {
      volumeUSD
    }
  }`)

  const data = poolDayDatas.map((d: { volumeUSD: string }) =>
    Number(d.volumeUSD),
  )

  return (
    data.reduce((result: number, curr: number) => result + curr, 0) /
    data.length
  )
  //   console.log()
  // return data
}

export const getUniStats = async (
  poolAddress: string,
  amount: number,
): Promise<[]> => {
  const { poolDayDatas } = await queryUniswap(`{
      poolDayDatas(skip: 1, first: ${amount}, orderBy: date, orderDirection: desc, where:{pool: "${poolAddress}"}) {
        date
        volumeUSD
        feesUSD
      }
    }`)

  const data = poolDayDatas.map(
    (d: { date: string; volumeUSD: string; feesUSD: string }) => [
      Number(d.date),
      Number(d.volumeUSD),
      Number(d.feesUSD),
    ],
  )

  return data
}

const main = async () => {
  // console.log(await getPoolTicks('0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8'))
}

main().then(() => {})
