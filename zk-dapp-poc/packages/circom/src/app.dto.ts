import { IsString } from 'class-validator'

export class GetProofDto {
  @IsString()
  validFrom: string

  @IsString()
  validTo: string
}

export class GetProofResDto {
  proof: string[]
  publicSignals: string[]
}
