import { Wallet, ethers } from 'ethers'
import { Consumer__factory, PlonkVerifier__factory } from '../typechain'

interface GanacheConfig {
  mnemonic: string
  rpcUrl: string
}

const GANACHE_CONFIG: GanacheConfig = {
  mnemonic: process.env.MNEMONIC,
  rpcUrl: `http://ganache:8545`,
}

const createWallets = async () => {
  const provider = new ethers.JsonRpcProvider(GANACHE_CONFIG.rpcUrl)
  const owner = Wallet.fromPhrase(GANACHE_CONFIG.mnemonic, provider)
  const client = Wallet.createRandom(provider)

  const tx = await owner.sendTransaction({
    value: ethers.parseEther('1'),
    to: client.address,
  })

  await tx.wait()

  return { owner, client }
}

export const runFixture = async () => {
  const wallets = await createWallets()

  const plonkVerifierContract = await new PlonkVerifier__factory(
    wallets.owner,
  ).deploy()

  await plonkVerifierContract.waitForDeployment()

  const consumerContract = await new Consumer__factory(wallets.owner).deploy(
    await plonkVerifierContract.getAddress(),
  )

  await consumerContract.waitForDeployment()

  return { wallets, plonkVerifierContract, consumerContract }
}
