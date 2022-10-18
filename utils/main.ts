import { getUniStats, getVolume24H } from './uniswap'
import { writeFileSync, readFileSync } from 'fs'

const ETH_USDC_003: string = '0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8'
const lastVolumes = 100

function arrayToCsv(data: any) {
  return data
    .map(
      (row: any) =>
        row
          .map(String) // convert every value to String
          .map((v: any) => v.replaceAll('"', '""')) // escape double colons
          .map((v: any) => `"${v}"`) // quote it
          .join(','), // comma-separated
    )
    .join('\r\n') // rows starting on new lines
}

const writeUniStats = () => {
  getUniStats(ETH_USDC_003, 500).then((res) => {
    console.log(res)
    let titles: string[] = ['unix date', 'volume', 'fees']
  
    writeFileSync('../data/uniStats.csv', titles + '\n' + arrayToCsv(res))
  })
}


