jest.setTimeout(1000000)
import { Test } from '@nestjs/testing'
import { INestApplication, ValidationPipe } from '@nestjs/common'
import request from 'supertest'
import { runFixture } from '../tests/fixture'
import { AppModule } from './app.module'

describe('AppController', () => {
  let app: INestApplication
  let fixture: Awaited<ReturnType<typeof runFixture>>

  beforeAll(async () => {
    const module = await Test.createTestingModule({
      imports: [AppModule],
    }).compile()

    app = module.createNestApplication()

    app.useGlobalPipes(
      new ValidationPipe({
        whitelist: true,
        forbidNonWhitelisted: true,
      }),
    )

    await app.init()

    fixture = await runFixture()
  })

  afterAll(async () => {
    await app.close()
  })

  describe('Circom PoC', () => {
    const sourceFrom = new Date(process.env.SOURCE_FROM).getTime()
    const sourceTo = new Date(process.env.SOURCE_TO).getTime()

    let testedFrom
    let testedTo

    const getProof = async (from, to) => {
      const res = await request(app.getHttpServer())
        .get(`/proof?validFrom=${from}&validTo=${to}`)
        .set('Content-Type', 'application/json')
        .send()

      return res
    }

    describe('proof generation', () => {
      it('generates valid proof', async () => {
        testedFrom = sourceFrom
        testedTo = sourceTo

        const { body } = await getProof(testedFrom, testedTo)
        expect(body.proof?.length).toBeGreaterThan(0)
        expect(body.publicSignals?.length).toBeGreaterThan(0)
      })

      it('fails: tested "from" timestamp > tested "to" timestamp', async () => {
        testedFrom = sourceTo
        testedTo = sourceFrom

        const res = await getProof(testedFrom, testedTo)

        expect(res.text).toMatchInlineSnapshot(
          `"{"message":"Error: Assert Failed. Error in template TimestampsBetween_4 line: 21\\n","error":"Bad Request","statusCode":400}"`,
        )
      })

      it('fails: tested "from" timestamp < source "from" timestamp', async () => {
        testedFrom = new Date('01/01/2023').getTime()
        testedTo = new Date('06/30/2024').getTime()

        const res = await getProof(testedFrom, testedTo)

        expect(res.text).toMatchInlineSnapshot(
          `"{"message":"Error: Assert Failed. Error in template TimestampsBetween_4 line: 27\\n","error":"Bad Request","statusCode":400}"`,
        )
      })

      it('fails: tested "to" timestamp > source "to" timestamp', async () => {
        testedFrom = new Date('01/01/2024').getTime()
        testedTo = new Date('07/01/2024').getTime()

        const res = await getProof(testedFrom, testedTo)

        expect(res.text).toMatchInlineSnapshot(
          `"{"message":"Error: Assert Failed. Error in template TimestampsBetween_4 line: 33\\n","error":"Bad Request","statusCode":400}"`,
        )
      })
    })

    describe('proof verification', () => {
      it('succeeds', async () => {
        const oneDay = 60 * 60 * 24
        testedFrom = sourceFrom
        testedTo = testedFrom + oneDay

        const { body } = await getProof(testedFrom, testedTo)

        expect(body.proof?.length).toBeGreaterThan(0)
        expect(body.publicSignals?.length).toBeGreaterThan(0)

        const consumerContractVerification =
          await fixture.consumerContract.dateInRange(
            body.proof,
            body.publicSignals,
          )
        expect(consumerContractVerification).toBeTruthy()
      })

      it('fails: malformed proof', async () => {
        const oneDay = 60 * 60 * 24
        testedFrom = sourceFrom
        testedTo = testedFrom + oneDay

        const { body } = await getProof(testedFrom, testedTo)

        expect(body.proof?.length).toBeGreaterThan(0)
        expect(body.publicSignals?.length).toBeGreaterThan(0)

        const malformedProof = [...body.proof]
        malformedProof[0] =
          '0x02e7449692fe025e3aae35ee56c78831cb88d96312d1c620533137af55be063f'

        const consumerContractVerification =
          await fixture.consumerContract.dateInRange(
            malformedProof,
            body.publicSignals,
          )
        expect(consumerContractVerification).toBeFalsy()
      })
    })
  })
})
