export interface IConfig {
  MNEMONIC: string
  SOURCE_FROM: string
  SOURCE_TO: string
}

export const config = (): IConfig => ({
  MNEMONIC: process.env.MNEMONIC,
  SOURCE_FROM: process.env.SOURCE_FROM,
  SOURCE_TO: process.env.SOURCE_TO,
})
