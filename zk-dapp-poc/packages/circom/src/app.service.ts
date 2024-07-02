import path from 'path'
import { BadRequestException, Injectable } from '@nestjs/common'
import { plonk } from 'snarkjs'
import { ConfigService } from '@nestjs/config'
import { GetProofDto, GetProofResDto } from './app.dto'
import { IConfig } from './config/config'

const circuitName = 'timestamps_between'

@Injectable()
export class AppService {
  constructor(private configService: ConfigService<IConfig>) {}

  async getProof(params: GetProofDto) {
    const sourceTimestamps = [
      new Date(
        this.configService.get<IConfig['SOURCE_FROM']>('SOURCE_FROM'),
      ).getTime(),
      new Date(
        this.configService.get<IConfig['SOURCE_TO']>('SOURCE_TO'),
      ).getTime(),
    ]

    const inputs = {
      sourceTimestamps,
      testedTimestamps: [parseInt(params.validFrom), parseInt(params.validTo)],
    }

    const wasmPath = path.join(
      process.cwd(),
      `circuits/${circuitName}/build/${circuitName}_js/${circuitName}.wasm`,
    )
    const provingKeyPath = path.join(
      process.cwd(),
      `circuits/${circuitName}/build/proving_key.zkey`,
    )

    let response: GetProofResDto = {
      proof: [],
      publicSignals: [],
    }

    try {
      const { proof, publicSignals } = await plonk.fullProve(
        inputs,
        wasmPath,
        provingKeyPath,
      )
      // '[...][...]'
      const calldataBlob = await plonk.exportSolidityCallData(
        proof,
        publicSignals,
      )

      const calldata = calldataBlob.replace('][', ']::[').split('::')

      response = {
        proof: await JSON.parse(calldata[0]),
        publicSignals: await JSON.parse(calldata[1]),
      }
      return response
    } catch (e) {
      throw new BadRequestException(e.message)
    }
  }
}
