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
  amount: number,
): Promise<number[]> => {
  const { poolDayDatas } = await queryUniswap(`{
    poolDayDatas(skip: 1, first: ${amount}, orderBy: date, orderDirection: desc, where:{pool: "${poolAddress}"}) {
      volumeUSD
    }
  }`)

  const data = poolDayDatas.map((d: { volumeUSD: string }) =>
    Number(d.volumeUSD),
  )

  //   return (
  //     data.reduce((result: number, curr: number) => result + curr, 0) /
  //     data.length
  //   );
  //   console.log()
  return data
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
